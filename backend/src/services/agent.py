import os
from typing import Optional
from openai import OpenAI
from config.settings import settings


class AIAgent:
    """AI Agent using OpenAI API for research and analysis"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
    
    async def analyze_topic(self, topic: str, context: Optional[str] = None) -> dict:
        """
        Analyze research topic and generate structured analysis
        
        Args:
            topic: Research topic
            context: Additional context from web search
            
        Returns:
            dict with summary, key_findings, and structured analysis
        """
        try:
            system_prompt = """You are an expert research analyst. Your task is to:
1. Analyze the given topic thoroughly
2. Provide a comprehensive summary
3. Extract key findings (3-5 main points)
4. Structure information in a clear, academic manner

Format your response as JSON with these fields:
- summary: A comprehensive summary (2-3 paragraphs)
- key_findings: List of 3-5 key findings
- detailed_analysis: In-depth analysis organized by sections
"""
            
            user_prompt = f"Research Topic: {topic}\n\n"
            if context:
                user_prompt += f"Context from web search:\n{context}\n\n"
            user_prompt += "Provide a detailed analysis of this topic."
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=2000,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            raise Exception(f"AI analysis failed: {str(e)}")
    
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
