import asyncio
from typing import List, Optional
from tavily import TavilyClient
from config.settings import settings
from backend.src.models.schemas import SearchResult


class WebSearchService:
    """Web search service using Tavily API"""
    
    def __init__(self):
        self.client = TavilyClient(api_key=settings.TAVILY_API_KEY)
        self.max_results = settings.MAX_SEARCH_RESULTS
    
    async def search(self, query: str, max_results: Optional[int] = None) -> List[SearchResult]:
        """
        Perform web search
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of SearchResult objects
        """
        try:
            results_limit = max_results or self.max_results
            
            # Tavily search is synchronous, run in executor
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.search(
                    query=query,
                    max_results=results_limit,
                    search_depth="advanced",
                    include_answer=True,
                    include_raw_content=False
                )
            )
            
            search_results = []
            for result in response.get('results', []):
                search_results.append(SearchResult(
                    title=result.get('title', ''),
                    url=result.get('url', ''),
                    snippet=result.get('content', ''),
                    relevance_score=result.get('score')
                ))
            
            return search_results
            
        except Exception as e:
            raise Exception(f"Web search failed: {str(e)}")
    
    async def get_context(self, query: str, max_results: Optional[int] = None) -> str:
        """
        Get combined context from search results
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            Combined context string
        """
        try:
            results = await self.search(query, max_results)
            
            context_parts = []
            for idx, result in enumerate(results, 1):
                context_parts.append(
                    f"[Source {idx}] {result.title}\n"
                    f"URL: {result.url}\n"
                    f"Content: {result.snippet}\n"
                )
            
            return "\n---\n".join(context_parts)
            
        except Exception as e:
            raise Exception(f"Context retrieval failed: {str(e)}")


# Singleton instance
search_service = WebSearchService()
