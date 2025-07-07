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