import logging

import uuid

from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

from main_app.db_models import PotentialOrdersFromEstimate, FilamentsStock

from main_app.schemas import submitOrderResponse, submitOrderInput

from main_app.send_mail import send_order_confirmation_email

router = APIRouter()


@router.post("/")
async def submit_order(
    order_id: str = Form(...),
    email: str = Form(...),
    filament_id: str = Form(...)
) -> submitOrderResponse:
    try:
        existing_order = await PotentialOrdersFromEstimate.objects().where(PotentialOrdersFromEstimate.orderID == order_id).first().run()

        existing_order.mail = email

        filament = await FilamentsStock.objects().where(FilamentsStock.filamentID == filament_id).first().run()
        existing_order.filament = filament
        existing_order.orderValue = filament.filamentPriceMultiplier * existing_order.orderValue

        await existing_order.save()

        email_sent = send_order_confirmation_email(email, existing_order.orderValue)
        if not email_sent:
            logging.warning(f"Failed to send confirmation email to {email}")

        return RedirectResponse(url="/api/v1/submitorder/success", status_code=303)

    except Exception as e:
        logging.error(f"Error updating order: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update order")
    
@router.get("/success")
async def success_page(request: Request):
    return templates.TemplateResponse("order_success.html.jinja", {"request": request})
