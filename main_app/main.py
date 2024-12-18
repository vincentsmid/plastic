import logging
import json

from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from main_app.redis_client import cache_page

from functools import wraps

from pydantic import BaseModel

# from main_app.db_models import ()
from piccolo.apps.user.tables import BaseUser
from piccolo_admin.endpoints import create_admin
from main_app.db_models import PotentialOrdersFromEstimate, FilamentsStock, SpecialSale, ItemsForSale

from main_app.api.api_admin import router as admin_router
from main_app.api.api_v1 import router as api_router
from main_app.logging_configurator import configure_logging

configure_logging()
logger = logging.getLogger(__name__)
logger.info("Server restarted")

origins = [
    "https://plasticlab.xyz",
    "https://www.plasticlab.xyz",
]

app = FastAPI(docs_url=None, redoc_url=None, title="Plastic Lab", version="1.0.0", openapi_url="/api/v1/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
admin = create_admin(
    tables=[
        BaseUser,
        PotentialOrdersFromEstimate,
        FilamentsStock,
        SpecialSale,
        ItemsForSale
    ]  # Add any Piccolo tables you want to manage here.
)

@app.get("/")
@cache_page(expire_time=3600) 
async def root(request: Request):
    current_sales = await SpecialSale.objects().where(SpecialSale.active == True).run()
    return templates.TemplateResponse(
        "index.html.jinja",
        {"request": request, "app_name": "Plastic Lab", "sales": current_sales},
    )


@app.get("/calculator")
@cache_page(expire_time=3600)
async def calculator_render(request: Request):
    filament_available = (
        await FilamentsStock.objects().where(FilamentsStock.available == True).run()
    )
    return templates.TemplateResponse(
        "calculator.html.jinja",
        {
            "request": request,
            "app_name": "Plastic Lab",
            "filament_colors": filament_available,
        },
    )


class ResultData(BaseModel):
    price: float
    filament_used: float
    total_hours: float


@app.get("/calculator-results/{order_id}")
@cache_page(expire_time=3600)
async def render_results(request: Request, order_id: str):
    filament = (
        await FilamentsStock.objects().where(FilamentsStock.available == True).run()
    )
    data = (
        await PotentialOrdersFromEstimate.objects()
        .where(PotentialOrdersFromEstimate.orderID == order_id)
        .first()
        .run()
    )

    return templates.TemplateResponse(
        "result.html.jinja",
        {
            "request": request,
            "price": data.orderValue,
            "filament_used": data.filamentUsed,
            "total_hours": data.printTime,
            "app_name": "Plastic Lab",
            "order_id": order_id,
            "filament_available": filament,
        },
    )


@app.get("/shop")
@cache_page(expire_time=3600)
async def shop_render(request: Request):
    items = await ItemsForSale.objects().where(ItemsForSale.available == True).run()
    return templates.TemplateResponse(
        "shop.html.jinja", {"request": request, "app_name": "Plastic Lab", "items": items}
    )

@app.get("/information")
@cache_page(expire_time=3600)
async def information_render(request: Request):
    return templates.TemplateResponse(
        "information.html.jinja", {"request": request, "app_name": "Plastic Lab"}
    )


# Include the router from router.py
app.include_router(api_router.router, prefix="/api/v1")

app.include_router(admin_router.router, prefix="/admin")

app.mount("/database", admin)  # Mount the Piccolo admin interface at /database

app.mount("/static", StaticFiles(directory="static"), name="static")
