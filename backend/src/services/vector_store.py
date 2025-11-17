import os
import logging
import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Optional
from datetime import datetime
from config.settings import settings

# Initialize logger
logger = logging.getLogger(__name__)


class VectorStore:
    """Vector store using ChromaDB for RAG functionality"""
    
    def __init__(self):
        # Ensure directory exists
        os.makedirs(settings.CHROMA_DB_PATH, exist_ok=True)
        
        logger.info(f"Initializing ChromaDB at: {settings.CHROMA_DB_PATH}")
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_DB_PATH,
            settings=ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="research_data",
            metadata={"description": "AI Research Agent storage"}
        )
        
        logger.info(f"ChromaDB collection 'research_data' initialized (count: {self.collection.count()})")
    
    async def store_research(self, research_id: str, research_data: dict) -> bool:
        """
        Store research data in vector database
        
        Args:
            research_id: Unique research identifier
            research_data: Research data to store
            
        Returns:
            Success boolean
        """
        try:
            logger.debug(f"Storing research: {research_id}")
            
            # Prepare document for storage
            document = self._prepare_document(research_data)
            
            # Store in ChromaDB
            self.collection.add(
                documents=[document],
                ids=[research_id],
                metadatas=[{
                    "research_id": research_id,
                    "topic": research_data.get("topic", ""),
                    "created_at": datetime.now().isoformat(),
                    "status": research_data.get("status", "completed")
                }]
            )
            
            logger.info(f"Successfully stored research: {research_id} (collection size: {self.collection.count()})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store research {research_id}: {str(e)}", exc_info=True)
            raise Exception(f"Failed to store research: {str(e)}")
    
    async def get_research(self, research_id: str) -> Optional[Dict]:
        """
        Retrieve research data by ID
        
        Args:
            research_id: Research identifier
            
        Returns:
            Research data dict or None
        """
        try:
            results = self.collection.get(
                ids=[research_id],
                include=["documents", "metadatas"]
            )
            
            if not results['ids']:
                return None
            
            return {
                "research_id": results['ids'][0],
                "document": results['documents'][0],
                "metadata": results['metadatas'][0]
            }
            
        except Exception as e:
            raise Exception(f"Failed to retrieve research: {str(e)}")
    
    async def search_similar(self, query: str, n_results: int = 5) -> List[Dict]:
        """
        Search for similar research by query
        
        Args:
            query: Search query
            n_results: Number of results to return
            
        Returns:
            List of similar research results
        """
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
            
            similar_results = []
            if results['ids'] and results['ids'][0]:
                for idx in range(len(results['ids'][0])):
                    similar_results.append({
                        "research_id": results['ids'][0][idx],
                        "document": results['documents'][0][idx],
                        "metadata": results['metadatas'][0][idx],
                        "distance": results['distances'][0][idx]
                    })
            
            return similar_results
            
        except Exception as e:
            raise Exception(f"Failed to search similar research: {str(e)}")
    
    async def get_all_research(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Get all stored research
        
        Args:
            limit: Optional limit on number of results
            
        Returns:
            List of all research data
        """
        try:
            results = self.collection.get(
                include=["documents", "metadatas"]
            )
            
            all_research = []
            for idx in range(len(results['ids'])):
                all_research.append({
                    "research_id": results['ids'][idx],
                    "metadata": results['metadatas'][idx]
                })
            
            # Sort by created_at descending
            all_research.sort(
                key=lambda x: x['metadata'].get('created_at', ''),
                reverse=True
            )
            
            if limit:
                all_research = all_research[:limit]
            
            return all_research
            
        except Exception as e:
            raise Exception(f"Failed to get all research: {str(e)}")
    
    def _prepare_document(self, research_data: dict) -> str:
        """
        Prepare research data as document string
        
        Args:
            research_data: Research data
            
        Returns:
            Document string
        """
        parts = [
            f"Topic: {research_data.get('topic', '')}",
            f"Summary: {research_data.get('summary', '')}",
        ]
        
        if research_data.get('key_findings'):
            parts.append(f"Key Findings: {', '.join(research_data['key_findings'])}")
        
        if research_data.get('raw_content'):
            parts.append(f"Content: {research_data['raw_content']}")
        
        return "\n\n".join(parts)


# Singleton instance
vector_store = VectorStore()
