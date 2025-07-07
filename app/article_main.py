from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List, Optional
from datetime import datetime
import logging
import json

from article_models import (
    Article, ArticleResponse, ArticleSummary, ArticleFilter,
    PaginationParams, ArticleListResponse, Theme, Language
)
from database import (
    connect_to_mongo, close_mongo_connection, get_collection
)
from bson import ObjectId

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Collection name for articles
ARTICLES_COLLECTION = "articles"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()

app = FastAPI(
    title="Articles on Bible API", 
    version="1.0.0",
    description="API for serving biblical articles with multilingual content (Tamil & English)",
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
def article_helper(article) -> dict:
    """Convert MongoDB document to response model"""
    return {
        "id": article["id"],
        "title": article["title"],
        "theme": article["theme"],
        "content": article["content"],
        "created_at": article.get("created_at", datetime.utcnow()),
        "updated_at": article.get("updated_at", datetime.utcnow())
    }

def article_summary_helper(article) -> dict:
    """Convert MongoDB document to summary response"""
    
    def extract_excerpt(content_blocks, max_length=150):
        """Extract excerpt from content blocks"""
        if not content_blocks:
            return ""
        
        # Find the first mainText or reflection block
        for block in content_blocks:
            if block.get("type") in ["mainText", "reflection"]:
                text = block.get("value", "")
                if len(text) <= max_length:
                    return text
                else:
                    # Truncate at word boundary
                    words = text[:max_length].split()
                    if len(words) > 1:
                        words = words[:-1]  # Remove potentially cut-off word
                    return " ".join(words) + "..."
        
        # If no mainText/reflection found, use first block
        if content_blocks:
            text = content_blocks[0].get("value", "")
            if len(text) <= max_length:
                return text
            else:
                words = text[:max_length].split()
                if len(words) > 1:
                    words = words[:-1]
                return " ".join(words) + "..."
        
        return ""
    
    content = article.get("content", {"tamil": [], "english": []})
    
    return {
        "id": article["id"],
        "title": article["title"],
        "theme": article["theme"],
        "excerpt": {
            "tamil": extract_excerpt(content.get("tamil", [])),
            "english": extract_excerpt(content.get("english", []))
        },
        "created_at": article.get("created_at", datetime.utcnow())
    }

async def build_search_query(filters: ArticleFilter) -> dict:
    """Build MongoDB query from filters"""
    query = {}
    
    if filters.theme:
        query["theme"] = filters.theme
    
    if filters.search:
        # Search in titles and content
        search_regex = {"$regex": filters.search, "$options": "i"}
        query["$or"] = [
            {"title.tamil": search_regex},
            {"title.english": search_regex},
            {"content.tamil.value": search_regex},
            {"content.english.value": search_regex}
        ]
    
    return query

# Root endpoints
@app.get("/")
async def root():
    return {
        "message": "Articles on Bible API is running!",
        "version": "1.0.0",
        "description": "API for biblical articles with Tamil and English content",
        "endpoints": {
            "get_all_articles": "/articles/",
            "get_article_by_id": "/articles/{article_id}",
            "search_articles": "/articles/search",
            "upload_articles": "/articles/upload",
            "health_check": "/health"
        }
    }

@app.get("/health")
async def health_check():
    try:
        collection = get_collection(ARTICLES_COLLECTION)
        count = await collection.count_documents({})
        return {
            "status": "healthy", 
            "database": "connected",
            "articles_count": count,
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

# Article endpoints
@app.get("/articles/", response_model=ArticleListResponse)
async def get_articles(
    skip: int = Query(0, ge=0, description="Number of articles to skip"),
    limit: int = Query(10, ge=1, le=50, description="Number of articles to return"),
    theme: Optional[Theme] = Query(None, description="Filter by theme"),
    search: Optional[str] = Query(None, description="Search in titles and content")
):
    """Get all articles with filtering and pagination"""
    collection = get_collection(ARTICLES_COLLECTION)
    
    # Build filter query
    filters = ArticleFilter(theme=theme, search=search)
    query = await build_search_query(filters)
    
    # Get total count
    total = await collection.count_documents(query)
    
    # Get articles with pagination
    cursor = collection.find(query).skip(skip).limit(limit).sort("created_at", -1)
    articles = []
    async for article in cursor:
        articles.append(article_summary_helper(article))
    
    return ArticleListResponse(
        articles=articles,
        total=total,
        skip=skip,
        limit=limit,
        has_next=skip + limit < total,
        has_previous=skip > 0
    )

@app.get("/articles/{article_id}", response_model=ArticleResponse)
async def get_article_by_id(article_id: str):
    """Get a specific article by its ID"""
    collection = get_collection(ARTICLES_COLLECTION)
    
    article = await collection.find_one({"id": article_id})
    if not article:
        raise HTTPException(status_code=404, detail=f"Article with id '{article_id}' not found")
    
    return article_helper(article)

@app.get("/articles/search", response_model=List[ArticleSummary])
async def search_articles(
    q: str = Query(..., min_length=1, description="Search query"),
    language: Optional[Language] = Query(None, description="Search in specific language"),
    limit: int = Query(10, ge=1, le=50, description="Number of results")
):
    """Search articles by content"""
    collection = get_collection(ARTICLES_COLLECTION)
    
    search_regex = {"$regex": q, "$options": "i"}
    
    if language:
        # Search in specific language
        if language == Language.TAMIL:
            query = {
                "$or": [
                    {"title.tamil": search_regex},
                    {"content.tamil.value": search_regex}
                ]
            }
        else:  # English
            query = {
                "$or": [
                    {"title.english": search_regex},
                    {"content.english.value": search_regex}
                ]
            }
    else:
        # Search in both languages
        query = {
            "$or": [
                {"title.tamil": search_regex},
                {"title.english": search_regex},
                {"content.tamil.value": search_regex},
                {"content.english.value": search_regex}
            ]
        }
    
    cursor = collection.find(query).limit(limit).sort("created_at", -1)
    articles = []
    async for article in cursor:
        articles.append(article_summary_helper(article))
    
    return articles

@app.post("/articles/upload")
async def upload_articles_from_json():
    """Upload articles from the content.json file"""
    collection = get_collection(ARTICLES_COLLECTION)
    
    try:
        # Read the content.json file
        with open("content.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        
        articles_data = data.get("pages", [])
        if not articles_data:
            raise HTTPException(status_code=400, detail="No articles found in content.json")
        
        # Clear existing articles
        await collection.delete_many({})
        
        # Prepare articles for insertion
        articles_to_insert = []
        current_time = datetime.utcnow()
        
        for article_data in articles_data:
            # Validate and clean the data
            article = {
                "id": article_data.get("id", ""),
                "title": article_data.get("title", {"tamil": "", "english": ""}),
                "theme": article_data.get("theme", "gray"),  # Default theme if missing
                "content": article_data.get("content", {"tamil": [], "english": []}),
                "created_at": current_time,
                "updated_at": current_time
            }
            articles_to_insert.append(article)
        
        # Insert all articles
        result = await collection.insert_many(articles_to_insert)
        
        # Create indexes for better search performance
        await collection.create_index("id", unique=True)
        await collection.create_index("theme")
        await collection.create_index([
            ("title.tamil", "text"),
            ("title.english", "text"),
            ("content.tamil.value", "text"),
            ("content.english.value", "text")
        ])
        
        return {
            "message": "Articles uploaded successfully",
            "uploaded_count": len(result.inserted_ids),
            "articles": [article["id"] for article in articles_to_insert]
        }
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="content.json file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format in content.json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading articles: {str(e)}")

@app.get("/articles/themes/", response_model=List[str])
async def get_available_themes():
    """Get all available themes"""
    collection = get_collection(ARTICLES_COLLECTION)
    
    themes = await collection.distinct("theme")
    return themes

@app.get("/stats/articles")
async def get_article_stats():
    """Get article statistics"""
    collection = get_collection(ARTICLES_COLLECTION)
    
    # Get theme distribution
    pipeline = [
        {
            "$group": {
                "_id": "$theme",
                "count": {"$sum": 1}
            }
        }
    ]
    
    theme_stats = []
    async for stat in collection.aggregate(pipeline):
        theme_stats.append({
            "theme": stat["_id"],
            "count": stat["count"]
        })
    
    total_articles = await collection.count_documents({})
    
    return {
        "total_articles": total_articles,
        "by_theme": theme_stats,
        "available_languages": ["tamil", "english"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)