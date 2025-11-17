import os
import json
import logging
from typing import Optional, Dict, List
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from config.settings import settings

# Configure logging
logger = logging.getLogger(__name__)


class AIAgent:
    """AI Agent using OpenAI API for research and analysis"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        logger.info(f"AIAgent initialized with model: {self.model}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    async def analyze_topic(self, topic: str, context: Optional[str] = None, depth: int = 3) -> Dict:
        """
        Analyze research topic and generate structured analysis with retry logic
        
        Args:
            topic: Research topic
            context: Additional context from web search
            depth: Analysis depth (1-5, higher = more detailed)
            
        Returns:
            dict with summary, key_findings, detailed_analysis, and metadata
        """
        try:
            logger.info(f"Starting analysis for topic: {topic[:50]}...")
            
            # Adjust prompt based on depth
            depth_instructions = self._get_depth_instructions(depth)
            
            system_prompt = f"""You are a world-class research analyst with expertise across multiple domains.

Your analysis must be:
- Comprehensive and fact-based
- Well-structured with clear sections
- Academic yet accessible
- Backed by the provided sources

{depth_instructions}

Response Format (JSON):
{{
  "summary": "Comprehensive 2-4 paragraph summary",
  "key_findings": ["Finding 1", "Finding 2", "Finding 3", "Finding 4", "Finding 5"],
  "detailed_analysis": {{
    "introduction": "Context and background",
    "main_insights": "Core findings and analysis",
    "implications": "Practical implications and applications",
    "future_outlook": "Trends and future directions"
  }},
  "confidence_score": 0.95,
  "sources_used": 10
}}
"""
            
            # Truncate context if too long (OpenAI token limit consideration)
            max_context_length = 6000
            if context and len(context) > max_context_length:
                logger.warning(f"Context truncated from {len(context)} to {max_context_length} chars")
                context = context[:max_context_length] + "\n\n[Context truncated for length...]"
            
            user_prompt = f"""Research Topic: {topic}

Web Search Context:
{context if context else 'No additional context provided.'}

Provide a comprehensive analysis following the JSON structure specified."""
            
            logger.debug(f"Sending request to OpenAI model: {self.model}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=3000,
                response_format={"type": "json_object"},
                timeout=60
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Validate and enrich response
            result = self._validate_and_enrich_analysis(result, topic)
            
            logger.info(f"Analysis completed successfully for: {topic[:50]}...")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in AI response: {str(e)}")
            raise Exception(f"AI returned invalid JSON: {str(e)}")
        except Exception as e:
            logger.error(f"AI analysis failed: {str(e)}")
            raise Exception(f"AI analysis failed: {str(e)}")
    
    def _get_depth_instructions(self, depth: int) -> str:
        """Get analysis instructions based on depth level"""
        depth_map = {
            1: "Provide a brief, high-level overview.",
            2: "Provide a moderate analysis with main points.",
            3: "Provide a detailed analysis with comprehensive insights.",
            4: "Provide an in-depth analysis with extensive details.",
            5: "Provide an exhaustive, expert-level analysis."
        }
        return depth_map.get(depth, depth_map[3])
    
    def _validate_and_enrich_analysis(self, result: Dict, topic: str) -> Dict:
        """Validate AI response and add metadata"""
        # Ensure required fields exist
        if "summary" not in result:
            result["summary"] = f"Analysis of {topic}"
        if "key_findings" not in result:
            result["key_findings"] = []
        if "detailed_analysis" not in result:
            result["detailed_analysis"] = {"main_content": result.get("summary", "")}
        
        # Ensure key_findings is a list
        if isinstance(result.get("key_findings"), str):
            result["key_findings"] = [result["key_findings"]]
        
        # Add metadata
        result["metadata"] = {
            "topic": topic,
            "model_used": self.model,
            "analysis_version": "1.0"
        }
        
        return result
    
    async def generate_report_structure(self, research_data: dict) -> dict:
        """
        Generate structured report outline
        
        Args:
            research_data: Complete research data
            
        Returns:
            dict with report structure
        """
        try:
            system_prompt = """You are a report structuring expert. Create a professional report outline with:
- Title
- Executive Summary
- Main Sections (3-5 sections with subsections)
- Conclusion
- Key Takeaways

Format as JSON with clear hierarchy."""
            
            user_prompt = f"""Create a report structure for:
Topic: {research_data.get('topic', 'N/A')}
Summary: {research_data.get('summary', 'N/A')}
Key Findings: {research_data.get('key_findings', [])}
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.5,
                max_tokens=1500,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            raise Exception(f"Report structure generation failed: {str(e)}")
    
    async def refine_content(self, content: str, instruction: str) -> str:
        """
        Refine and improve content based on instruction
        
        Args:
            content: Content to refine
            instruction: Refinement instruction
            
        Returns:
            Refined content
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a content refinement expert."},
                    {"role": "user", "content": f"{instruction}\n\nContent:\n{content}"}
                ],
                temperature=0.6,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Content refinement failed: {str(e)}")


# Singleton instance
agent = AIAgent()
