from fastapi import FastAPI
from routes.crawler_routes import router as crawler_router

app = FastAPI(title="Crawler API", description="API for web scraping", version="1.0.0")
app.include_router(crawler_router, prefix="", tags=["crawler"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Crawler API!"}
