import asyncio
import logging
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from tavily import TavilyClient
from tenacity import retry, stop_after_attempt, wait_exponential
from config.settings import settings
from backend.src.models.schemas import SearchResult

# Configure logging
logger = logging.getLogger(__name__)


class WebSearchService:
    """Web search service using Tavily API with caching and retry logic"""
    
    def __init__(self):
        self.client = TavilyClient(api_key=settings.TAVILY_API_KEY)
        self.max_results = settings.MAX_SEARCH_RESULTS
        self._cache: Dict[str, Dict] = {}
        self._cache_ttl = timedelta(hours=1)
        logger.info("WebSearchService initialized")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    async def search(self, query: str, max_results: Optional[int] = None, use_cache: bool = True) -> List[SearchResult]:
        """
        Perform web search with caching and retry logic
        
        Args:
            query: Search query
            max_results: Maximum number of results
            use_cache: Whether to use cached results if available
            
        Returns:
            List of SearchResult objects
        """
        try:
            results_limit = max_results or self.max_results
            cache_key = f"{query}_{results_limit}"
            
            # Check cache
            if use_cache and cache_key in self._cache:
                cached_data = self._cache[cache_key]
                if datetime.now() - cached_data['timestamp'] < self._cache_ttl:
                    logger.info(f"Using cached results for query: {query[:50]}...")
                    return cached_data['results']
                else:
                    # Remove expired cache entry
                    del self._cache[cache_key]
            
            logger.info(f"Performing web search: {query[:50]}... (max_results={results_limit})")
            
            # Tavily search is synchronous, run in executor
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.search(
                    query=query,
                    max_results=results_limit,
                    search_depth="advanced",
                    include_answer=True,
                    include_raw_content=False,
                    include_domains=[],
                    exclude_domains=[]
                )
            )
            
            search_results = []
            for idx, result in enumerate(response.get('results', []), 1):
                try:
                    search_results.append(SearchResult(
                        title=result.get('title', f'Result {idx}'),
                        url=result.get('url', ''),
                        snippet=result.get('content', ''),
                        relevance_score=result.get('score', 0.0)
                    ))
                except Exception as e:
                    logger.warning(f"Failed to parse search result {idx}: {str(e)}")
                    continue
            
            # Cache results
            if use_cache and search_results:
                self._cache[cache_key] = {
                    'results': search_results,
                    'timestamp': datetime.now()
                }
            
            logger.info(f"Found {len(search_results)} search results")
            return search_results
            
        except Exception as e:
            logger.error(f"Web search failed: {str(e)}")
            raise Exception(f"Web search failed: {str(e)}")
    
    def clear_cache(self):
        """Clear search cache"""
        self._cache.clear()
        logger.info("Search cache cleared")
    
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
