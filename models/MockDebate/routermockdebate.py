from fastapi import APIRouter
from models.MockDebate.Opposition import Speech_Gen

router = APIRouter(prefix="/mock_debate", tags=["Mock Debate"])

@router.post("/opposition_speech")
def generate_opposition_speech(data: dict):  # For production, use a Pydantic model
    motion = data.get("motion")
    result = Speech_Gen(motion)
    return {"result": result}
from fastapi import APIRouter
from models.MockDebate.Proposition import Speech_Gen

router = APIRouter(prefix="/mock_debate", tags=["Mock Debate"])

@router.post("/proposition_speech")
def generate_proposition_speech(data: dict):  # For production, use a Pydantic model
    motion = data.get("motion")
    result = Speech_Gen(motion)
    return {"result": result}