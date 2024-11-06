import logging

from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel

# from main_app.db_models import ()
from piccolo.apps.user.tables import BaseUser
from piccolo_admin.endpoints import create_admin
from main_app.db_models import PotentialOrdersFromEstimate, FilamentsStock, SpecialSale

from main_app.api.api_admin import router as admin_router
from main_app.api.api_v1 import router as api_router
from main_app.logging_configurator import configure_logging

configure_logging()
logger = logging.getLogger(__name__)
logger.info("Server restarted")

app = FastAPI()
templates = Jinja2Templates(directory="templates")
admin = create_admin(
    tables=[
        BaseUser,
        PotentialOrdersFromEstimate,
        FilamentsStock,
    ]  # Add any Piccolo tables you want to manage here.
)


@app.get("/")
async def root(request: Request):
    current_sales = await SpecialSale.objects().where(SpecialSale.active == True).run()
    return templates.TemplateResponse(
        "index.html.jinja",
        {"request": request, "app_name": "Plastic Lab", "sales": current_sales},
    )


@app.get("/calculator")
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
            "app_name": "Plastic",
            "order_id": order_id,
            "filament_available": filament,
        },
    )


@app.get("/shop")
async def shop_render(request: Request):
    return templates.TemplateResponse(
        "shop.html.jinja", {"request": request, "app_name": "Plastic Lab"}
    )

@app.get("/information")
async def information_render(request: Request):
    return templates.TemplateResponse(
        "information.html.jinja", {"request": request, "app_name": "Plastic Lab"}
    )


# Include the router from router.py
app.include_router(api_router.router, prefix="/api/v1")

app.include_router(admin_router.router, prefix="/admin")

app.mount("/database", admin)  # Mount the Piccolo admin interface at /database

app.mount("/static", StaticFiles(directory="static"), name="static")
