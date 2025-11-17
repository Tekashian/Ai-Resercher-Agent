import os
import json
import logging
from typing import Optional, Dict, List
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from config.settings import settings

# Configure logging
logger = logging.getLogger(__name__)


class AIAgent:
    """AI Agent using Google Gemini API for research and analysis"""
    
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
        logger.info(f"AIAgent initialized with model: {settings.GEMINI_MODEL}")
    
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
            
            system_prompt = f"""# ROLE & EXPERTISE
You are Dr. Alexandra Chen, Chief Strategy Officer at McKinsey & Company with 20+ years leading Fortune 500 transformations. PhD in Economics (MIT), former Goldman Sachs Managing Director, advisor to 3 unicorn startups. Your reports have guided $50B+ in strategic decisions.

# CONTEXT
Client: C-suite executive team requiring actionable intelligence
Deliverable: Board-level strategic research report
Budget: $2M+ consulting engagement
Timeline: Immediate decision-making required
Stakes: Multi-million dollar implications

# OBJECTIVE
Produce a comprehensive strategic analysis that:
1. Provides executive summary with clear recommendations
2. Identifies 8 critical insights with quantifiable impact
3. Maps competitive landscape and market dynamics
4. Assesses risks with mitigation strategies
5. Delivers implementation roadmap with success metrics
6. Projects financial implications and ROI
7. Forecasts 3-5 year trends and disruption scenarios
8. Analyzes stakeholder impact across the value chain

# CONSTRAINTS
- Output: STRICT JSON only (no markdown, no code blocks)
- Length: Comprehensive yet concise (board attention span)
- Tone: Executive-level (authoritative, data-driven, actionable)
- Quality: McKinsey Quarterly publication standard
- Accuracy: Every claim must be defensible with sources

# OUTPUT FORMAT (STRICT JSON)
{{
  "summary": "4-6 paragraph executive brief covering: (1) Strategic overview and market context, (2) Core value proposition and competitive positioning, (3) Critical risks and opportunities with probability assessment, (4) Key recommendations with expected ROI and timeline",
  "key_findings": [
    "Finding 1: Market size and growth trajectory with TAM/SAM/SOM breakdown",
    "Finding 2: Competitive dynamics showing market share, pricing power, and barriers to entry",
    "Finding 3: Technology trends and innovation cycles affecting the space",
    "Finding 4: Regulatory landscape and compliance requirements",
    "Finding 5: Financial metrics including unit economics and profitability drivers",
    "Finding 6: Customer segments, pain points, and willingness to pay",
    "Finding 7: Supply chain and operational considerations",
    "Finding 8: Strategic partnerships and ecosystem dependencies"
  ],
  "detailed_analysis": {{
    "executive_overview": "Set strategic context in 3-4 paragraphs: macro trends, market structure, key players, regulatory environment, and why this matters now",
    "market_analysis": "Deep dive in 4-5 paragraphs: market sizing (TAM/SAM/SOM), growth drivers, adoption curves, pricing dynamics, customer segments, distribution channels",
    "strategic_insights": "Core findings in 4-5 paragraphs: competitive positioning, differentiation opportunities, value chain analysis, strategic partnerships, M&A landscape",
    "risk_assessment": "Comprehensive risk matrix in 3-4 paragraphs: operational risks, market risks, technology risks, regulatory risks, financial risks - each with probability, impact, and mitigation",
    "implementation_roadmap": "Actionable plan in 3-4 paragraphs: Phase 1 (quick wins 0-6 months), Phase 2 (scale 6-18 months), Phase 3 (optimize 18-36 months) with resources, milestones, KPIs",
    "financial_implications": "Economic analysis in 2-3 paragraphs: investment requirements, cost structure, revenue model, break-even analysis, IRR projections, sensitivity analysis",
    "future_outlook": "Predictive analysis in 4-5 paragraphs: 3-year trend forecast, emerging technologies, disruption scenarios (bull/base/bear cases), strategic pivots, global implications",
    "competitive_intelligence": "Competitive landscape in 3-4 paragraphs: key player profiles, market positioning matrix, SWOT analysis, strategic moves, threats and opportunities"
  }},
  "confidence_score": 0.95,
  "sources_used": 10
}}

{depth_instructions}

# QUALITY STANDARDS
✓ Every paragraph must provide actionable insights
✓ Use specific numbers, percentages, timeframes
✓ Reference concrete examples and case studies
✓ Avoid jargon unless defined
✓ Structure with clear topic sentences
✓ Connect insights to business impact
✓ Anticipate executive questions

# JSON SAFETY
⚠ Use only straight quotes (no curly quotes)
⚠ Escape special characters: \\" \\\\ \\n \\t
⚠ No line breaks within string values
⚠ Keep each paragraph as single continuous text
⚠ Test JSON validity before output"""
            
            # Increase context limit for ultra-detailed reports
            max_context_length = 15000  # Increased from 6000 for world-class analysis
            if context and len(context) > max_context_length:
                logger.warning(f"Context truncated from {len(context)} to {max_context_length} chars")
                context = context[:max_context_length] + "\n\n[Context truncated for length...]"
            
            user_prompt = f"""Research Topic: {topic}

Web Search Context:
{context if context else 'No additional context provided.'}

Provide a comprehensive analysis following the JSON structure specified."""
            
            logger.debug(f"Sending request to Gemini model: {settings.GEMINI_MODEL}")
            
            # Combine prompts for Gemini
            full_prompt = f"""{system_prompt}

{user_prompt}"""
            
            # Generate response using Gemini with higher token limit for detailed reports
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.5,  # Reduced for more stable JSON
                    max_output_tokens=6000,  # Reduced from 8000 for safety
                    response_mime_type="application/json"
                ),
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                }
            )
            
            # Check if response was blocked
            if not response.text or response.text.strip() == "":
                logger.error(f"Empty response from Gemini. Finish reason: {response.candidates[0].finish_reason if response.candidates else 'Unknown'}")
                raise Exception("AI returned empty response. Try reducing context length or simplifying the query.")
            
            # Clean and parse response
            response_text = response.text.strip()
            
            # Try to fix common JSON issues
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            result = json.loads(response_text)
            
            # Validate and enrich response
            result = self._validate_and_enrich_analysis(result, topic)
            
            logger.info(f"Analysis completed successfully for: {topic[:50]}...")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in AI response: {str(e)}")
            logger.error(f"Response preview: {response.text[:500]}...")
            
            # Try alternative parsing - extract JSON from markdown code blocks
            try:
                import re
                json_match = re.search(r'\{[\s\S]*\}', response.text)
                if json_match:
                    logger.info("Attempting to extract JSON from response...")
                    result = json.loads(json_match.group(0))
                    result = self._validate_and_enrich_analysis(result, topic)
                    logger.info(f"Successfully recovered from JSON error for: {topic[:50]}...")
                    return result
            except:
                pass
            
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
            "model_used": settings.GEMINI_MODEL,
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
            prompt = f"""You are a report structuring expert. Create a professional report outline with:
- Title
- Executive Summary
- Main Sections (3-5 sections with subsections)
- Conclusion
- Key Takeaways

Create a report structure for:
Topic: {research_data.get('topic', 'N/A')}
Summary: {research_data.get('summary', 'N/A')}
Key Findings: {research_data.get('key_findings', [])}

Format as JSON with clear hierarchy."""
            
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.5,
                    max_output_tokens=1500,
                    response_mime_type="application/json"
                )
            )
            
            result = json.loads(response.text)
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
            prompt = f"""You are a content refinement expert.

{instruction}

Content:
{content}"""
            
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.6,
                    max_output_tokens=1000
                )
            )
            
            return response.text
            
        except Exception as e:
            raise Exception(f"Content refinement failed: {str(e)}")


# Singleton instance
agent = AIAgent()
