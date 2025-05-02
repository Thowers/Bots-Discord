from fastapi import APIRouter, HTTPException,status
from services.crawler_service import CrawlerService
from models.crawler_models import Producto

router = APIRouter()

@router.get("/crawler", response_model=list, status_code=status.HTTP_200_OK)
async def get_crawler_data():
    try:
        crawler_service = CrawlerService()
        data = crawler_service.get_data()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e