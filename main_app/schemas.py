from pydantic import BaseModel


class calculatePriceResponse(BaseModel):
    price: float
    filament_used: float
    total_hours: float
    order_id: str


class submitOrderInput(BaseModel):
    order_id: str
    email: str
    filament_id: str


class submitOrderResponse(BaseModel):
    confirmation: bool
