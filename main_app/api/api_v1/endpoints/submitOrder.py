import logging

import uuid

from fastapi import APIRouter, Form, Request, HTTPException

from main_app.db_models import PotentialOrdersFromEstimate, FilamentsStock

from main_app.schemas import submitOrderResponse, submitOrderInput

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

        await existing_order.save()

        return submitOrderResponse(confirmation=True)

    except Exception as e:
        logging.error(f"Error updating order: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update order")
