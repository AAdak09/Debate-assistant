from fastapi import APIRouter
from models.Speech_Engine.Speech import Speech_Gen

router = APIRouter(prefix="/speech", tags=["Speech Engine"])

@router.get("/generate")
def generate_speech(motion: str, time: int, side: str):
    result = Speech_Gen(motion, time, side)
    return {"result": result}