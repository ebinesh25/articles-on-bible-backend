from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

# Enums for better data validation
class ItemCategory(str, Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    BOOKS = "books"
    HOME = "home"
    SPORTS = "sports"
    OTHER = "other"

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"

# Enhanced Item model
class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Item name")
    description: Optional[str] = Field(None, max_length=500, description="Item description")
    price: float = Field(..., gt=0, description="Item price must be greater than 0")
    quantity: int = Field(..., ge=0, description="Item quantity must be 0 or greater")
    category: ItemCategory = Field(default=ItemCategory.OTHER, description="Item category")
    tags: List[str] = Field(default=[], description="Item tags for search")
    is_active: bool = Field(default=True, description="Whether item is active")

class ItemResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    price: float
    quantity: int
    category: ItemCategory
    tags: List[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=0)
    category: Optional[ItemCategory] = None
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None

# User models
class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: str = Field(..., description="User email")
    full_name: Optional[str] = Field(None, max_length=100, description="Full name")
    role: UserRole = Field(default=UserRole.USER, description="User role")
    is_active: bool = Field(default=True, description="Whether user is active")

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    full_name: Optional[str] = None
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

# Search and filter models
class ItemFilter(BaseModel):
    category: Optional[ItemCategory] = None
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    is_active: Optional[bool] = None
    tags: Optional[List[str]] = None
    search: Optional[str] = Field(None, max_length=100, description="Search in name and description")

class PaginationParams(BaseModel):
    skip: int = Field(default=0, ge=0, description="Number of items to skip")
    limit: int = Field(default=10, ge=1, le=100, description="Number of items to return")

# Response models
class PaginatedResponse(BaseModel):
    items: List[ItemResponse]
    total: int
    skip: int
    limit: int
    has_next: bool
    has_previous: bool