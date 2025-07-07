from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ContentType(str, Enum):
    MAIN_TEXT = "mainText"
    SCRIPTURE = "scripture"
    REFLECTION = "reflection"

class Theme(str, Enum):
    GRAY = "gray"
    WARM = "warm"
    BLUE = "blue"
    GREEN = "green"
    PURPLE = "purple"

class Language(str, Enum):
    TAMIL = "tamil"
    ENGLISH = "english"

# Content block model
class ContentBlock(BaseModel):
    type: ContentType
    value: str

# Title model
class Title(BaseModel):
    tamil: str
    english: str

# Content model
class Content(BaseModel):
    tamil: List[ContentBlock]
    english: List[ContentBlock]

# Article model for database storage
class Article(BaseModel):
    id: str = Field(..., description="Unique article identifier")
    title: Title
    theme: Theme
    content: Content
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# Response model
class ArticleResponse(BaseModel):
    id: str
    title: Title
    theme: Theme
    content: Content
    created_at: datetime
    updated_at: datetime

# Simplified response for listing
class ArticleSummary(BaseModel):
    id: str
    title: Title
    theme: Theme
    created_at: datetime

# Search and filter models
class ArticleFilter(BaseModel):
    theme: Optional[Theme] = None
    language: Optional[Language] = None
    search: Optional[str] = Field(None, max_length=100, description="Search in title and content")

class PaginationParams(BaseModel):
    skip: int = Field(default=0, ge=0, description="Number of articles to skip")
    limit: int = Field(default=10, ge=1, le=50, description="Number of articles to return")

class ArticleListResponse(BaseModel):
    articles: List[ArticleSummary]
    total: int
    skip: int
    limit: int
    has_next: bool
    has_previous: bool