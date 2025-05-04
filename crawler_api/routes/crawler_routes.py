from fastapi import APIRouter, HTTPException, status
from typing import List
from crawler_api.services.crawler_service import CrawlerService

router = APIRouter()

@router.get("/crawler", response_model=list, status_code=status.HTTP_200_OK)
async def get_crawler_data():
    try:
        crawler_service = CrawlerService()
        return crawler_service.get_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))