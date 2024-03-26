import logging

from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel

# from main_app.db_models import ()
from piccolo.apps.user.tables import BaseUser
from piccolo_admin.endpoints import create_admin

from main_app.api.api_admin import router as admin_router
from main_app.api.api_v1 import router as api_router
from main_app.logging_configurator import configure_logging

configure_logging()
logger = logging.getLogger(__name__)
logger.info("Server restarted")

app = FastAPI()
templates = Jinja2Templates(directory="templates")
admin = create_admin(
    tables=[BaseUser]  # Add any Piccolo tables you want to manage here.
)


@app.get("/")
async def root(request: Request):
    """
    Returns the root endpoint of the FastAPI application.

    Parameters:
    - request (Request): The incoming request object.

    Returns:
    - TemplateResponse: The response containing the rendered "index.html" template.
    """
    return templates.TemplateResponse(
        "index.html.jinja", {"request": request, "app_name": "Plastic"}
    )

@app.get("/calculator")
async def calculator_render(request: Request):
    return templates.TemplateResponse("calculator.html.jinja", {"request": request, "app_name": "Plastic"})

class ResultData(BaseModel):
    price: float
    filament_used: float
    total_hours: float

@app.post("/calculator-results")
async def render_results(request: Request, data: ResultData):
    return templates.TemplateResponse("result.html.jinja", {
        "request": request, 
        "price": data.price, 
        "filament_used": data.filament_used, 
        "total_hours": data.total_hours
    })

# Include the router from router.py
app.include_router(api_router.router, prefix="/api/v1")

app.include_router(admin_router.router, prefix="/admin")

app.mount("/database", admin)  # Mount the Piccolo admin interface at /database

app.mount("/static", StaticFiles(directory="static"), name="static")
