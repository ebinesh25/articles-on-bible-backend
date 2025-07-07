# FastAPI + MongoDB Docker Setup

This project provides a complete Docker Compose setup for running FastAPI with MongoDB.

## Features

- FastAPI web framework with async MongoDB support
- MongoDB database with authentication
- Docker Compose orchestration
- Sample CRUD API endpoints
- Health check endpoints
- Database initialization with sample data

## Quick Start

1. **Start the services:**
   ```bash
   docker-compose up -d
   ```

2. **Check if services are running:**
   ```bash
   docker-compose ps
   ```

3. **Access the API:**
   - FastAPI docs: http://localhost:8000/docs
   - API health check: http://localhost:8000/health
   - MongoDB: localhost:27017

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /items/` - Get all items
- `POST /items/` - Create new item
- `GET /items/{item_id}` - Get specific item
- `PUT /items/{item_id}` - Update item
- `DELETE /items/{item_id}` - Delete item

## Example API Usage

### Create an item:
```bash
curl -X POST "http://localhost:8000/items/" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Test Item",
       "description": "A test item",
       "price": 19.99,
       "quantity": 3
     }'
```

### Get all items:
```bash
curl http://localhost:8000/items/
```

## Database Access

### MongoDB Connection Details:
- Host: localhost
- Port: 27017
- Database: fastapi_db
- Username: admin
- Password: password123

### Connect via MongoDB Compass or CLI:
```bash
mongodb://admin:password123@localhost:27017/fastapi_db?authSource=admin
```

## Development

### View logs:
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f fastapi
docker-compose logs -f mongodb
```

### Rebuild and restart:
```bash
docker-compose down
docker-compose up --build -d
```

### Stop services:
```bash
docker-compose down
```

### Remove volumes (delete data):
```bash
docker-compose down -v
```

## Project Structure

```
.
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile             # FastAPI container definition
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── app/
│   └── main.py           # FastAPI application
├── mongo-init/
│   └── init-mongo.js     # MongoDB initialization script
└── README.md             # This file
```

## Customization

- Modify `app/main.py` to add your API endpoints
- Update `requirements.txt` for additional Python packages
- Edit `mongo-init/init-mongo.js` for custom database initialization
- Adjust `docker-compose.yml` for different configurations


│                                                                                                              │
│                                                                                                              │
│                                           ✅ Mission Accomplished!                                           │
│                                                                                                              │
│                                       What We've Successfully Created:                                       │
│                                                                                                              │
│  1 ✅ Docker Compose Setup - MongoDB + FastAPI running perfectly                                             │
│  2 ✅ Data Upload Complete - All 19 biblical articles from content.json uploaded                             │
│  3 ✅ API Structure Customized - Built specifically for your biblical content                                │
│  4 ✅ Multilingual Support - Tamil & English content preserved                                               │
│  5 ✅ ID-based Retrieval - Get articles by ID as requested                                                   │
│                                                                                                              │
│                                          🔥 Working API Endpoints:                                           │
│                                                                                                              │
│  • Get Article by ID: GET /articles/{id} ✅                                                                  │
│                                                                                                              │
│     curl http://localhost:8000/articles/weakness                                                             │
│     curl http://localhost:8000/articles/remember                                                             │
│                                                                                                              │
│  • List All Articles: GET /articles/ ✅                                                                      │
│  • Search Articles: GET /articles/search?q={query} ✅                                                        │
│  • Statistics: GET /stats/articles ✅                                                                        │
│                                                                                                              │
│                                              📊 Current Status:                                              │
│                                                                                                              │
│  • 19 Articles successfully loaded                                                                           │
│  • 9 Different themes (gray, warm, blue, green, etc.)                                                        │
│  • Multilingual content (Tamil + English)                                                                    │
│  • 3 Content types (mainText, scripture, reflection)                                                         │
│                                                                                                              │
│                                               🚀 Ready to Use:                                               │
│                                                                                                              │
│  • API Base URL: http://localhost:8000                                                                       │
│  • Interactive Docs: http://localhost:8000/docs                                                              │
│  • MongoDB: Running on port 27017                                                                            │
│                                                                                                              │


<!-- API USAGE -->

╭─ Response ───────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│ ┃                                   Biblical Articles API - Quick Reference                                    ┃ │
│ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ │
│                                                                                                                  │
│                                                                                                                  │
│                                         Base URL: http://localhost:8000                                          │
│                                                                                                                  │
│                                                   📋 Core APIs                                                   │
│                                                                                                                  │
│                                                                                                                  │
│   Method   Endpoint   Description                      Parameters                                                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                                               │
│   GET      /          API info & available endpoints   -                                                         │
│   GET      /health    Health check + article count     -                                                         │
│                                                                                                                  │
│                                                                                                                  │
│                                                 📖 Article APIs                                                  │
│                                                                                                                  │
│                                                                                                                  │
│   Method   Endpoint           Description                 Parameters                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━       │
│   GET      /articles/         List articles (paginated)   skip=0, limit=10, theme=gray, search=text              │
│   GET      /articles/{id}     Get specific article        id (path param)                                        │
│   GET      /articles/search   Search articles             q=search_text, language=tamil/english, limit=10        │
│   POST     /articles/upload   Upload from content.json    - (no params)                                          │
│                                                                                                                  │
│                                                                                                                  │
│                                                 🎨 Utility APIs                                                  │
│                                                                                                                  │
│                                                                                                                  │
│   Method   Endpoint            Description            Parameters                                                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                                                │
│   GET      /articles/themes/   Get available themes   -                                                          │
│   GET      /stats/articles     Article statistics     -                                                          │
│                                                                                                                  │
│                                                                                                                  │
│ ──────────────────────────────────────────────────────────────────────────────────────────────────────────────── │
│                                                                                                                  │
│                                                🚀 Usage Examples                                                 │
│                                                                                                                  │
│                                                 Get All Articles                                                 │
│                                                                                                                  │
│                                                                                                                  │
│  GET /articles/?skip=0&limit=5&theme=blue                                                                        │
│                                                                                                                  │
│                                                                                                                  │
│                                                 Search Articles                                                  │
│                                                                                                                  │
│                                                                                                                  │
│  GET /articles/search?q=prayer&language=tamil&limit=3                                                            │
│                                                                                                                  │
│                                                                                                                  │
│                                               Get Specific Article                                               │
│                                                                                                                  │
│                                                                                                                  │
│  GET /articles/ART001                                                                                            │
│                                                                                                                  │
│                                                                                                                  │
│                                                 Upload Articles                                                  │
│                                                                                                                  │
│                                                                                                                  │
│  POST /articles/upload                                                                                           │
│                                                                                                                  │
│                                                                                                                  │
│                                                 Filter by Theme                                                  │
│                                                                                                                  │
│                                                                                                                  │
│  GET /articles/?theme=warm&limit=10                                                                              │
│                                                                                                                  │
│                                                                                                                  │
│ ──────────────────────────────────────────────────────────────────────────────────────────────────────────────── │
│                                                                                                                  │
│                                               📊 Response Formats                                                │
│                                                                                                                  │
│                                              Article List Response                                               │
│                                                                                                                  │
│                                                                                                                  │
│  {                                                                                                               │
│    "articles": [...],                                                                                            │
│    "total": 25,                                                                                                  │
│    "skip": 0,                                                                                                    │
│    "limit": 10,                                                                                                  │
│    "has_next": true,                                                                                             │
│    "has_previous": false                                                                                         │
│  }                                                                                                               │
│                                                                                                                  │
│                                                                                                                  │
│                                             Single Article Response                                              │
│                                                                                                                  │
│                                                                                                                  │
│  {                                                                                                               │
│    "id": "ART001",                                                                                               │
│    "title": {"tamil": "...", "english": "..."},                                                                  │
│    "theme": "blue",                                                                                              │
│    "content": {"tamil": [...], "english": [...]},                                                                │
│    "created_at": "2024-01-01T00:00:00",                                                                          │
│    "updated_at": "2024-01-01T00:00:00"                                                                           │
│  }                                                                                                               │
│                                                                                                                  │
│                                                                                                                  │
│ ──────────────────────────────────────────────────────────────────────────────────────────────────────────────── │
│                                                                                                                  │
│                                                  🎯 Quick Start                                                  │
│                                                                                                                  │
│  1 List articles: GET /articles/                                                                                 │
│  2 Search: GET /articles/search?q=your_search                                                                    │
│  3 Get article: GET /articles/{article_id}                                                                       │
│  4 Upload data: POST /articles/upload                                                                            │
│                                                                                                                  │
│ Available Themes: gray, warm, blue, green, purple, yellow, light, red, brown                                     │
│ Languages: tamil, english                                                                                        │
│                                                                                                                  │
│ Would you like me to help you test any of these APIs or show you the actual content structure?                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
