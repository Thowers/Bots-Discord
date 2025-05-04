from fastapi import FastAPI
from crawler_api.routes.crawler_routes import router as crawler_router

app = FastAPI(
    title="Crawler API",
    description="API for web scraping",
    version="1.0.0"
)
app.include_router(crawler_router, prefix="", tags=["crawler"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Crawler API!"}

def run_app():
    import uvicorn
    uvicorn.run("crawler_api.crawler:app", host="0.0.0.0", port=8000)