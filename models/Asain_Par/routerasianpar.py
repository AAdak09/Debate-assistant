from fastapi import APIRouter
from models.Asain_Par.DLO import Speech_Gen
from models.Asain_Par.DPM import Speech_Gen
from models.Asain_Par.GovtWhip import Speech_Gen

router = APIRouter(prefix="/asian_par", tags=["Asian Parliamentary"])

@router.post("/dlo_speech")
def generate_dlo_speech(data: dict):  # For production, use a Pydantic model
    motion = data.get("motion")
    result = Speech_Gen(motion)
    return {"result": result}

from fastapi import APIRouter


router = APIRouter(prefix="/asian_par", tags=["Asian Parliamentary"])

@router.post("/dpm_speech")
def generate_dpm_speech(data: dict):  # For production, use a Pydantic model
    motion = data.get("motion")
    result = Speech_Gen(motion)
    return {"result": result}

from models.Asain_Par.GovtWhip import Speech_Gen

router = APIRouter(prefix="/asian_par", tags=["Asian Parliamentary"])

@router.post("/govtwhip_speech")
def generate_govtwhip_speech(data: dict):  # For production, use a Pydantic model
    motion = data.get("motion")
    result = Speech_Gen(motion)
    return {"result": result}

from fastapi import APIRouter
from models.Asain_Par.OppositionLeader import Speech_Gen

router = APIRouter(prefix="/asian_par", tags=["Asian Parliamentary"])

@router.post("/opposition_leader_speech")
def generate_opposition_leader_speech(data: dict):  # For production, use a Pydantic model
    motion = data.get("motion")
    result = Speech_Gen(motion)
    return {"result": result}

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






