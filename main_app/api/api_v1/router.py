from fastapi import APIRouter

from main_app.api.api_v1.endpoints import (calculatePrice)

router = APIRouter()

router.include_router(calculatePrice.router, prefix="/calculateprice", tags=["calculatePrice"])
