import os
from datetime import datetime
from typing import Dict, Optional
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from config.settings import settings


class PDFGenerator:
    """PDF report generator using ReportLab"""
    
    def __init__(self):
        # Ensure reports directory exists
        os.makedirs(settings.REPORTS_PATH, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            leading=14
        ))
    
    async def generate_report(
        self,
        research_data: Dict,
        report_id: str,
        include_sources: bool = True
    ) -> str:
        """
        Generate PDF report from research data
        
        Args:
            research_data: Research data dictionary
            report_id: Unique report identifier
            include_sources: Whether to include sources
            
        Returns:
            Path to generated PDF file
        """
        try:
            # Create filename
            filename = f"report_{report_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filepath = os.path.join(settings.REPORTS_PATH, filename)
            
            # Create PDF document
            doc = SimpleDocTemplate(
                filepath,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Build content
            story = []
            
            # Title
            title = research_data.get('topic', 'Research Report')
            story.append(Paragraph(title, self.styles['CustomTitle']))
            story.append(Spacer(1, 0.3*inch))
            
            # Metadata
            created_at = research_data.get('created_at', datetime.now())
            if isinstance(created_at, str):
                created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            
            metadata_text = f"<b>Generated:</b> {created_at.strftime('%B %d, %Y at %I:%M %p')}<br/>"
            metadata_text += f"<b>Research ID:</b> {research_data.get('research_id', 'N/A')}"
            story.append(Paragraph(metadata_text, self.styles['CustomBody']))
            story.append(Spacer(1, 0.3*inch))
            
            # Executive Summary
            story.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
            summary = research_data.get('summary', 'No summary available.')
            story.append(Paragraph(summary, self.styles['CustomBody']))
            story.append(Spacer(1, 0.2*inch))
            
            # Key Findings
            key_findings = research_data.get('key_findings', [])
            if key_findings:
                story.append(Paragraph("Key Findings", self.styles['SectionHeader']))
                for idx, finding in enumerate(key_findings, 1):
                    finding_text = f"<b>{idx}.</b> {finding}"
                    story.append(Paragraph(finding_text, self.styles['CustomBody']))
                story.append(Spacer(1, 0.2*inch))
            
            # Detailed Analysis
            detailed_analysis = research_data.get('detailed_analysis', '')
            if detailed_analysis:
                story.append(Paragraph("Detailed Analysis", self.styles['SectionHeader']))
                
                if isinstance(detailed_analysis, dict):
                    for section_title, section_content in detailed_analysis.items():
                        story.append(Paragraph(f"<b>{section_title}</b>", self.styles['CustomBody']))
                        story.append(Paragraph(str(section_content), self.styles['CustomBody']))
                        story.append(Spacer(1, 0.1*inch))
                else:
                    story.append(Paragraph(str(detailed_analysis), self.styles['CustomBody']))
                
                story.append(Spacer(1, 0.2*inch))
            
            # Sources
            if include_sources:
                sources = research_data.get('sources', [])
                if sources:
                    story.append(PageBreak())
                    story.append(Paragraph("Sources & References", self.styles['SectionHeader']))
                    for idx, source in enumerate(sources, 1):
                        source_text = f"{idx}. {source}"
                        story.append(Paragraph(source_text, self.styles['CustomBody']))
            
            # Build PDF
            doc.build(story)
            
            return filepath
            
        except Exception as e:
            raise Exception(f"PDF generation failed: {str(e)}")


# Singleton instance
pdf_generator = PDFGenerator()
