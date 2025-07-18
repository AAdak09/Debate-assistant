from fastapi import APIRouter
from models.POI_Engine.poi import Chatbot

router = APIRouter(prefix="/poi", tags=["POI Engine"])

@router.post("/generate")
def generate_poi(data: dict):  # For production, use a Pydantic model
    motion = data.get("motion")
    side = data.get("side")
    # You may need to update Chatbot to accept both motion and side
    result = Chatbot(motion, side)
    return {"result": result}