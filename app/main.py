from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List, Optional
import os
from bson import ObjectId

app = FastAPI(title="FastAPI MongoDB Example", version="1.0.0")

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "fastapi_db")

client = AsyncIOMotorClient(MONGODB_URL)
database = client[DATABASE_NAME]
collection = database["items"]

# Pydantic models
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int

class ItemResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    price: float
    quantity: int

# Helper function to convert MongoDB document to response model
def item_helper(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "description": item.get("description"),
        "price": item["price"],
        "quantity": item["quantity"]
    }

@app.on_event("startup")
async def startup_event():
    """Test database connection on startup"""
    try:
        await client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")

@app.get("/")
async def root():
    return {"message": "FastAPI with MongoDB is running!"}

@app.get("/health")
async def health_check():
    try:
        await client.admin.command('ping')
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

@app.post("/items/", response_model=ItemResponse)
async def create_item(item: Item):
    item_dict = item.dict()
    result = await collection.insert_one(item_dict)
    new_item = await collection.find_one({"_id": result.inserted_id})
    return item_helper(new_item)

@app.get("/items/", response_model=List[ItemResponse])
async def get_items():
    items = []
    async for item in collection.find():
        items.append(item_helper(item))
    return items

@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: str):
    try:
        item = await collection.find_one({"_id": ObjectId(item_id)})
        if item:
            return item_helper(item)
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid item ID")

@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: str, item: Item):
    try:
        item_dict = item.dict()
        result = await collection.update_one(
            {"_id": ObjectId(item_id)}, 
            {"$set": item_dict}
        )
        if result.modified_count == 1:
            updated_item = await collection.find_one({"_id": ObjectId(item_id)})
            return item_helper(updated_item)
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid item ID")

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    try:
        result = await collection.delete_one({"_id": ObjectId(item_id)})
        if result.deleted_count == 1:
            return {"message": "Item deleted successfully"}
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid item ID")