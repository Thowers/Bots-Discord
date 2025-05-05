import os
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
    return {"mensaje": "Bienvenido a la API de crawler de criptomonedas desde la pagina de CoinMarketCap"}

def run_app():
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("crawler_api.crawler:app", host="0.0.0.0", port=port, log_level="info")