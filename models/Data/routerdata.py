from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from models.Asian_par import thread_runner

router = APIRouter(
    prefix="/asian-par",
    tags=["Asian Parliamentary"]
)

class MotionRequest(BaseModel):
    motion: str

@router.post("/generate")
def run_asian_parliamentary_debate(req: MotionRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(thread_runner.generate_asian_parliamentary_debate, req.motion)
    return {"status": "Generation started", "motion": req.motion}

from fastapi import APIRouter
from models.Asain_Par.OppWhip import Speech_Gen

router = APIRouter(prefix="/asian_par", tags=["Asian Parliamentary"])

@router.post("/oppwhip_speech")
def generate_oppwhip_speech(data: dict):  # For production, use a Pydantic model
    motion = data.get("motion")
    result = Speech_Gen(motion)
    return {"result": result}

from fastapi import APIRouter
from models.Asain_Par.PrimeMinister import Speech_Gen

router = APIRouter(prefix="/asian_par", tags=["Asian Parliamentary"])

@router.post("/prime_minister_speech")
def generate_prime_minister_speech(data: dict):  # For production, use a Pydantic model
    motion = data.get("motion")
    result = Speech_Gen(motion)
    return {"result": result}