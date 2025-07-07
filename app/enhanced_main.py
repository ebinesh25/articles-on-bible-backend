from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List, Optional
from datetime import datetime
import logging

from models import (
    Item, ItemResponse, ItemUpdate, ItemFilter, 
    PaginationParams, PaginatedResponse,
    User, UserResponse
)
from database import (
    connect_to_mongo, close_mongo_connection, get_collection,
    ITEMS_COLLECTION, USERS_COLLECTION
)
from bson import ObjectId

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()

app = FastAPI(
    title="Enhanced FastAPI MongoDB Example", 
    version="2.0.0",
    description="A comprehensive FastAPI application with MongoDB, featuring advanced CRUD operations, search, filtering, and pagination",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper functions
def item_helper(item) -> dict:
    """Convert MongoDB document to response model"""
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "description": item.get("description"),
        "price": item["price"],
        "quantity": item["quantity"],
        "category": item.get("category", "other"),
        "tags": item.get("tags", []),
        "is_active": item.get("is_active", True),
        "created_at": item.get("created_at", datetime.utcnow()),
        "updated_at": item.get("updated_at", datetime.utcnow())
    }

def user_helper(user) -> dict:
    """Convert MongoDB user document to response model"""
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "full_name": user.get("full_name"),
        "role": user.get("role", "user"),
        "is_active": user.get("is_active", True),
        "created_at": user.get("created_at", datetime.utcnow()),
        "updated_at": user.get("updated_at", datetime.utcnow())
    }

async def build_filter_query(filters: ItemFilter) -> dict:
    """Build MongoDB query from filters"""
    query = {}
    
    if filters.category:
        query["category"] = filters.category
    
    if filters.is_active is not None:
        query["is_active"] = filters.is_active
    
    if filters.min_price is not None or filters.max_price is not None:
        price_query = {}
        if filters.min_price is not None:
            price_query["$gte"] = filters.min_price
        if filters.max_price is not None:
            price_query["$lte"] = filters.max_price
        query["price"] = price_query
    
    if filters.tags:
        query["tags"] = {"$in": filters.tags}
    
    if filters.search:
        query["$text"] = {"$search": filters.search}
    
    return query

# Root endpoints
@app.get("/")
async def root():
    return {
        "message": "Enhanced FastAPI with MongoDB is running!",
        "version": "2.0.0",
        "features": [
            "Advanced CRUD operations",
            "Search and filtering",
            "Pagination",
            "User management",
            "Data validation",
            "Performance optimized"
        ]
    }

@app.get("/health")
async def health_check():
    try:
        # Test database connection
        collection = get_collection(ITEMS_COLLECTION)
        await collection.find_one()
        return {
            "status": "healthy", 
            "database": "connected",
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

# Enhanced Items endpoints
@app.post("/items/", response_model=ItemResponse)
async def create_item(item: Item):
    """Create a new item with enhanced validation"""
    collection = get_collection(ITEMS_COLLECTION)
    
    item_dict = item.dict()
    item_dict["created_at"] = datetime.utcnow()
    item_dict["updated_at"] = datetime.utcnow()
    
    result = await collection.insert_one(item_dict)
    new_item = await collection.find_one({"_id": result.inserted_id})
    
    return item_helper(new_item)

@app.get("/items/", response_model=PaginatedResponse)
async def get_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to return"),
    category: Optional[str] = Query(None, description="Filter by category"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    search: Optional[str] = Query(None, description="Search in name and description"),
    tags: Optional[List[str]] = Query(None, description="Filter by tags")
):
    """Get items with advanced filtering and pagination"""
    collection = get_collection(ITEMS_COLLECTION)
    
    # Build filter query
    filters = ItemFilter(
        category=category,
        min_price=min_price,
        max_price=max_price,
        is_active=is_active,
        search=search,
        tags=tags
    )
    query = await build_filter_query(filters)
    
    # Get total count
    total = await collection.count_documents(query)
    
    # Get items with pagination
    cursor = collection.find(query).skip(skip).limit(limit).sort("created_at", -1)
    items = []
    async for item in cursor:
        items.append(item_helper(item))
    
    return PaginatedResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit,
        has_next=skip + limit < total,
        has_previous=skip > 0
    )

@app.get("/items/search", response_model=List[ItemResponse])
async def search_items(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(10, ge=1, le=50, description="Number of results")
):
    """Full-text search in items"""
    collection = get_collection(ITEMS_COLLECTION)
    
    cursor = collection.find(
        {"$text": {"$search": q}},
        {"score": {"$meta": "textScore"}}
    ).sort([("score", {"$meta": "textScore"})]).limit(limit)
    
    items = []
    async for item in cursor:
        items.append(item_helper(item))
    
    return items

@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: str):
    """Get a specific item by ID"""
    collection = get_collection(ITEMS_COLLECTION)
    
    try:
        item = await collection.find_one({"_id": ObjectId(item_id)})
        if item:
            return item_helper(item)
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid item ID")

@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: str, item_update: ItemUpdate):
    """Update an item with partial updates"""
    collection = get_collection(ITEMS_COLLECTION)
    
    try:
        # Only update fields that are provided
        update_data = {k: v for k, v in item_update.dict().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        update_data["updated_at"] = datetime.utcnow()
        
        result = await collection.update_one(
            {"_id": ObjectId(item_id)}, 
            {"$set": update_data}
        )
        
        if result.modified_count == 1:
            updated_item = await collection.find_one({"_id": ObjectId(item_id)})
            return item_helper(updated_item)
        
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid item ID")

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    """Delete an item"""
    collection = get_collection(ITEMS_COLLECTION)
    
    try:
        result = await collection.delete_one({"_id": ObjectId(item_id)})
        if result.deleted_count == 1:
            return {"message": "Item deleted successfully"}
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid item ID")

# User management endpoints
@app.post("/users/", response_model=UserResponse)
async def create_user(user: User):
    """Create a new user"""
    collection = get_collection(USERS_COLLECTION)
    
    # Check if username or email already exists
    existing_user = await collection.find_one({
        "$or": [
            {"username": user.username},
            {"email": user.email}
        ]
    })
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    user_dict = user.dict()
    user_dict["created_at"] = datetime.utcnow()
    user_dict["updated_at"] = datetime.utcnow()
    
    result = await collection.insert_one(user_dict)
    new_user = await collection.find_one({"_id": result.inserted_id})
    
    return user_helper(new_user)

@app.get("/users/", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    role: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None)
):
    """Get users with filtering"""
    collection = get_collection(USERS_COLLECTION)
    
    query = {}
    if role:
        query["role"] = role
    if is_active is not None:
        query["is_active"] = is_active
    
    cursor = collection.find(query).skip(skip).limit(limit).sort("created_at", -1)
    users = []
    async for user in cursor:
        users.append(user_helper(user))
    
    return users

# Statistics endpoints
@app.get("/stats/items")
async def get_item_stats():
    """Get item statistics"""
    collection = get_collection(ITEMS_COLLECTION)
    
    pipeline = [
        {
            "$group": {
                "_id": "$category",
                "count": {"$sum": 1},
                "total_value": {"$sum": {"$multiply": ["$price", "$quantity"]}},
                "avg_price": {"$avg": "$price"}
            }
        }
    ]
    
    stats = []
    async for stat in collection.aggregate(pipeline):
        stats.append({
            "category": stat["_id"],
            "count": stat["count"],
            "total_value": round(stat["total_value"], 2),
            "avg_price": round(stat["avg_price"], 2)
        })
    
    total_items = await collection.count_documents({})
    active_items = await collection.count_documents({"is_active": True})
    
    return {
        "total_items": total_items,
        "active_items": active_items,
        "inactive_items": total_items - active_items,
        "by_category": stats
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)