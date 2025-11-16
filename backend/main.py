from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uuid
from datetime import datetime
from typing import List
import os

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


# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for FastAPI app"""
    # Startup
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"📊 ChromaDB path: {settings.CHROMA_DB_PATH}")
    print(f"📄 Reports path: {settings.REPORTS_PATH}")
    
    # Ensure directories exist
    os.makedirs(settings.CHROMA_DB_PATH, exist_ok=True)
    os.makedirs(settings.REPORTS_PATH, exist_ok=True)
    
    yield
    
    # Shutdown
    print("👋 Shutting down AI Research Agent")


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
        
        print(f"🔍 Starting research: {research_id} - {request.topic}")
        
        # Step 1: Web search
        print(f"  └─ Searching web (max {request.max_results} results)...")
        search_results = await search_service.search(
            query=request.topic,
            max_results=request.max_results
        )
        
        # Get context from search results
        context = await search_service.get_context(
            query=request.topic,
            max_results=request.max_results
        )
        
        # Step 2: AI analysis
        print(f"  └─ Analyzing with AI ({settings.OPENAI_MODEL})...")
        analysis = await agent.analyze_topic(
            topic=request.topic,
            context=context
        )
        
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
        print(f"  └─ Storing in vector database...")
        await vector_store.store_research(research_id, research_data)
        
        print(f"✅ Research completed: {research_id}")
        
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
        print(f"❌ Research failed: {str(e)}")
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
        print(f"📄 Generating report for research: {request.research_id}")
        
        # Retrieve research data
        research_data = await vector_store.get_research(request.research_id)
        
        if not research_data:
            raise HTTPException(
                status_code=404,
                detail=f"Research not found: {request.research_id}"
            )
        
        # Generate report ID
        report_id = f"rpt_{uuid.uuid4().hex[:12]}"
        
        # Generate PDF
        print(f"  └─ Generating PDF...")
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
        
        print(f"✅ Report generated: {report_id}")
        
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
        print(f"❌ Report generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")


@app.get("/history")
async def get_research_history(limit: int = 10):
    """
    Get research history
    
    Returns list of recent research with metadata
    """
    try:
        print(f"📜 Retrieving research history (limit: {limit})")
        
        history = await vector_store.get_all_research(limit=limit)
        
        return {
            "count": len(history),
            "limit": limit,
            "research": history
        }
        
    except Exception as e:
        print(f"❌ Failed to retrieve history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve history: {str(e)}")


@app.get("/research/{research_id}")
async def get_research_details(research_id: str):
    """Get detailed information about specific research"""
    try:
        research_data = await vector_store.get_research(research_id)
        
        if not research_data:
            raise HTTPException(
                status_code=404,
                detail=f"Research not found: {research_id}"
            )
        
        return research_data
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve research: {str(e)}")


@app.get("/download/{filename}")
async def download_report(filename: str):
    """Download generated PDF report"""
    try:
        file_path = os.path.join(settings.REPORTS_PATH, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Report not found")
        
        return FileResponse(
            path=file_path,
            media_type="application/pdf",
            filename=filename
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")


@app.get("/search")
async def search_research(query: str, limit: int = 5):
    """Search for similar research by query"""
    try:
        results = await vector_store.search_similar(query, n_results=limit)
        
        return {
            "query": query,
            "count": len(results),
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
