from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uuid
from datetime import datetime
from typing import List
import os
import logging
from logging.handlers import RotatingFileHandler

from backend.src.models.schemas import (
    ResearchRequest,
    ResearchResponse,
    ReportRequest,
    ReportResponse,
    ResearchStatus,
    ResearchData
)
from backend.src.services.agent import agent
from backend.src.services.search import search_service
from backend.src.services.vector_store import vector_store
from backend.src.services.pdf_generator import pdf_generator
from config.settings import settings

# Configure logging
def setup_logging():
    """Setup comprehensive logging"""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Create logs directory
    os.makedirs("logs", exist_ok=True)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_format))
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(log_format))
    
    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    return logging.getLogger(__name__)

logger = setup_logging()


# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for FastAPI app"""
    # Startup
    logger.info("=" * 60)
    logger.info(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"📊 ChromaDB path: {settings.CHROMA_DB_PATH}")
    logger.info(f"📄 Reports path: {settings.REPORTS_PATH}")
    logger.info(f"🤖 OpenAI Model: {settings.OPENAI_MODEL}")
    logger.info(f"🔍 Max Search Results: {settings.MAX_SEARCH_RESULTS}")
    logger.info("=" * 60)
    
    # Ensure directories exist
    os.makedirs(settings.CHROMA_DB_PATH, exist_ok=True)
    os.makedirs(settings.REPORTS_PATH, exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    logger.info("✅ All directories initialized")
    
    yield
    
    # Shutdown
    logger.info("👋 Shutting down AI Research Agent")
    logger.info("=" * 60)


# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered research agent with RAG and PDF generation",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "endpoints": {
            "research": "/research - Conduct research on a topic",
            "report": "/report - Generate PDF report",
            "history": "/history - Get research history",
            "docs": "/docs - API documentation"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": settings.APP_NAME
    }


@app.post("/research", response_model=ResearchResponse)
async def conduct_research(
    request: ResearchRequest,
    background_tasks: BackgroundTasks
):
    """
    Conduct research on a given topic
    
    This endpoint:
    1. Performs web search using Tavily
    2. Analyzes content using OpenAI
    3. Stores results in vector database
    4. Returns structured research data
    """
    try:
        # Generate unique research ID
        research_id = f"res_{uuid.uuid4().hex[:12]}"
        
        logger.info(f"🔍 Starting research: {research_id} - Topic: '{request.topic}' (max_results: {request.max_results})")
        start_time = datetime.now()
        
        # Step 1: Web search
        logger.info(f"  └─ Step 1/3: Searching web (max {request.max_results} results)...")
        search_results = await search_service.search(
            query=request.topic,
            max_results=request.max_results
        )
        logger.info(f"     ✓ Found {len(search_results)} results")
        
        # Get context from search results
        context = await search_service.get_context(
            query=request.topic,
            max_results=request.max_results
        )
        logger.info(f"     ✓ Context extracted: {len(context)} chars")
        
        # Step 2: AI analysis
        logger.info(f"  └─ Step 2/3: Analyzing with AI (model: {settings.OPENAI_MODEL})...")
        analysis = await agent.analyze_topic(
            topic=request.topic,
            context=context
        )
        logger.info(f"     ✓ Analysis complete (confidence: {analysis.get('confidence_score', 'N/A')})")
        
        # Extract sources
        sources = [result.url for result in search_results]
        
        # Prepare research data
        research_data = {
            "research_id": research_id,
            "topic": request.topic,
            "status": ResearchStatus.COMPLETED,
            "summary": analysis.get("summary", ""),
            "key_findings": analysis.get("key_findings", []),
            "detailed_analysis": analysis.get("detailed_analysis", ""),
            "sources": sources,
            "raw_content": context,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Step 3: Store in vector database
        logger.info(f"  └─ Step 3/3: Storing in ChromaDB (ID: {research_id})...")
        await vector_store.store_research(research_id, research_data)
        
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"✅ Research completed successfully: {research_id} (duration: {duration:.2f}s)")
        
        # Return response
        return ResearchResponse(
            research_id=research_id,
            topic=request.topic,
            status=ResearchStatus.COMPLETED,
            summary=analysis.get("summary"),
            key_findings=analysis.get("key_findings"),
            sources=sources,
            created_at=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"❌ Research failed for topic '{request.topic}': {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Research failed: {str(e)}")


@app.post("/report", response_model=ReportResponse)
async def generate_report(request: ReportRequest):
    """
    Generate PDF report from research data
    
    This endpoint:
    1. Retrieves research data from vector store
    2. Generates structured PDF report
    3. Returns download URL
    """
    try:
        logger.info(f"📄 Generating report for research: {request.research_id}")
        start_time = datetime.now()
        
        # Retrieve research data
        logger.info(f"  └─ Retrieving research data from ChromaDB...")
        research_data = await vector_store.get_research(request.research_id)
        
        if not research_data:
            logger.warning(f"  ⚠️ Research not found: {request.research_id}")
            raise HTTPException(
                status_code=404,
                detail=f"Research not found: {request.research_id}"
            )
        
        logger.info(f"     ✓ Research data retrieved")
        
        # Generate report ID
        report_id = f"rpt_{uuid.uuid4().hex[:12]}"
        
        # Generate PDF
        logger.info(f"  └─ Generating PDF with ReportLab (ID: {report_id})...")
        pdf_path = await pdf_generator.generate_report(
            research_data={
                **research_data['metadata'],
                "research_id": research_data['research_id'],
                "summary": research_data['document'].split('Summary: ')[1].split('\n\n')[0] if 'Summary: ' in research_data['document'] else "",
                "key_findings": research_data['metadata'].get('key_findings', []),
                "detailed_analysis": research_data['metadata'].get('detailed_analysis', ''),
                "sources": research_data['metadata'].get('sources', [])
            },
            report_id=report_id,
            include_sources=request.include_sources
        )
        
        # Generate download URL
        filename = os.path.basename(pdf_path)
        download_url = f"/download/{filename}"
        
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"✅ Report generated successfully: {report_id} ({filename}) (duration: {duration:.2f}s)")
        
        return ReportResponse(
            report_id=report_id,
            research_id=request.research_id,
            file_path=pdf_path,
            download_url=download_url,
            created_at=datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Report generation failed for {request.research_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")


@app.get("/history")
async def get_research_history(limit: int = 10):
    """
    Get research history
    
    Returns list of recent research with metadata
    """
    try:
        logger.info(f"📜 Retrieving research history (limit: {limit})")
        
        history = await vector_store.get_all_research(limit=limit)
        
        logger.info(f"✅ Retrieved {len(history)} research items")
        
        return {
            "count": len(history),
            "limit": limit,
            "research": history
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to retrieve history: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve history: {str(e)}")


@app.get("/research/{research_id}")
async def get_research_details(research_id: str):
    """Get detailed information about specific research"""
    try:
        logger.info(f"📖 Retrieving research details for: {research_id}")
        
        research_data = await vector_store.get_research(research_id)
        
        if not research_data:
            logger.warning(f"  ⚠️ Research not found: {research_id}")
            raise HTTPException(
                status_code=404,
                detail=f"Research not found: {research_id}"
            )
        
        logger.info(f"✅ Research details retrieved: {research_id}")
        
        return research_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to retrieve research {research_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve research: {str(e)}")


@app.get("/download/{filename}")
async def download_report(filename: str):
    """Download generated PDF report"""
    try:
        logger.info(f"⬇️ Download requested: {filename}")
        
        file_path = os.path.join(settings.REPORTS_PATH, filename)
        
        if not os.path.exists(file_path):
            logger.warning(f"  ⚠️ File not found: {filename}")
            raise HTTPException(status_code=404, detail="Report not found")
        
        file_size = os.path.getsize(file_path)
        logger.info(f"✅ Serving file: {filename} ({file_size} bytes)")
        
        return FileResponse(
            path=file_path,
            media_type="application/pdf",
            filename=filename
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Download failed for {filename}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")


@app.get("/search")
async def search_research(query: str, limit: int = 5):
    """Search for similar research by query"""
    try:
        logger.info(f"🔎 Searching similar research: '{query}' (limit: {limit})")
        
        results = await vector_store.search_similar(query, n_results=limit)
        
        logger.info(f"✅ Found {len(results)} similar research items")
        
        return {
            "query": query,
            "count": len(results),
            "results": results
        }
        
    except Exception as e:
        logger.error(f"❌ Search failed for query '{query}': {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
