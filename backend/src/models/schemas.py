from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ResearchStatus(str, Enum):
    """Status of research operation"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class ResearchRequest(BaseModel):
    """Request model for research endpoint"""
    topic: str = Field(..., description="Research topic or question", min_length=3, max_length=500)
    depth: Optional[int] = Field(default=3, description="Research depth (1-5)", ge=1, le=5)
    max_results: Optional[int] = Field(default=10, description="Max search results", ge=1, le=20)
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "topic": "Latest developments in quantum computing",
                    "depth": 3,
                    "max_results": 10
                }
            ]
        }
    }


class ResearchResponse(BaseModel):
    """Response model for research endpoint"""
    research_id: str = Field(..., description="Unique research identifier")
    topic: str = Field(..., description="Research topic")
    status: ResearchStatus = Field(..., description="Current status")
    summary: Optional[str] = Field(None, description="Research summary")
    key_findings: Optional[List[str]] = Field(None, description="Key findings from research")
    sources: Optional[List[str]] = Field(None, description="Sources used")
    created_at: datetime = Field(..., description="Creation timestamp")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "research_id": "res_123abc",
                    "topic": "Quantum computing",
                    "status": "completed",
                    "summary": "Quantum computing is evolving rapidly...",
                    "key_findings": ["Finding 1", "Finding 2"],
                    "sources": ["https://example.com/article1"],
                    "created_at": "2025-11-16T12:00:00Z"
                }
            ]
        }
    }


class ReportRequest(BaseModel):
    """Request model for report generation"""
    research_id: str = Field(..., description="Research ID to generate report from")
    format: Optional[str] = Field(default="pdf", description="Report format")
    include_sources: Optional[bool] = Field(default=True, description="Include sources in report")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "research_id": "res_123abc",
                    "format": "pdf",
                    "include_sources": True
                }
            ]
        }
    }


class ReportResponse(BaseModel):
    """Response model for report generation"""
    report_id: str = Field(..., description="Unique report identifier")
    research_id: str = Field(..., description="Associated research ID")
    file_path: str = Field(..., description="Path to generated report")
    download_url: str = Field(..., description="Download URL")
    created_at: datetime = Field(..., description="Creation timestamp")


class SearchResult(BaseModel):
    """Model for search results"""
    title: str
    url: str
    snippet: str
    relevance_score: Optional[float] = None


class ResearchData(BaseModel):
    """Internal model for storing research data"""
    research_id: str
    topic: str
    status: ResearchStatus
    summary: Optional[str] = None
    key_findings: Optional[List[str]] = None
    sources: Optional[List[str]] = None
    raw_content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
