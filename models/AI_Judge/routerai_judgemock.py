# routers/ai_judge_router.py

from fastapi import APIRouter

from models.AI_Judge import AI_Judge_Mock, AI_Judge_Par, FeedbackAsian, FeedbackMock

from models.AI_Judge.AI_Judge_Par import Speech_Gen

from models.AI_Judge.FeedbackAsian import Speech_Gen

from models.AI_Judge.FeedbackMock import Speech_Gen

router = APIRouter(prefix="/judge", tags=["AI Judge"])

@router.post("/MockDebate_Judge")
def judge_mock(data: dict):  # Replace with Pydantic model later
    def judge_mock(data: dict):  # Replace with Pydantic model later
    # Extract fields from data dict
    motion = data.get("motion")
    opening_prop = data.get("opening_prop")
    opening_opp = data.get("opening_opp")
    rebuttal_prop = data.get("rebuttal_prop")
    rebuttal_opp = data.get("rebuttal_opp")
    qna_summary = data.get("qna_summary")

    result = MockDebate_Judge(
        motion,
        opening_prop,
        opening_opp,
        rebuttal_prop,
        rebuttal_opp,
        qna_summary
    )
    return {"result": result}

router = APIRouter(prefix="/par", tags=["AI Judge Parli"])

@router.post("/speech_gen")
def speech_gen(data: dict):  # Replace with Pydantic model for production
    motion = data.get("motion")
    pm = data.get("pm")
    ol = data.get("ol")
    dpm = data.get("dpm")
    dlo = data.get("dlo")
    gw = data.get("gw")
    ow = data.get("ow")
    committee_summary = data.get("committee_summary")

    result = Speech_Gen(
        motion,
        pm,
        ol,
        dpm,
        dlo,
        gw,
        ow,
        committee_summary
    )
    return {"result": result}

router = APIRouter(prefix="/feedback/asian", tags=["Feedback Asian"])

@router.post("/speech_gen")
def feedback_asian_speech_gen(data: dict):  # Replace with Pydantic model for production
    motion = data.get("motion")
    information = data.get("information")
    role = data.get("role")

    result = Speech_Gen(
        motion,
        information,
        role
    )
    return {"result": result}

router = APIRouter(prefix="/feedback/mock", tags=["Feedback Mock"])

@router.post("/speech_gen")
def feedback_mock_speech_gen(data: dict):  # Replace with Pydantic model for production
    motion = data.get("motion")
    opening_statement_text = data.get("opening_statement_text")
    role = data.get("role")
    rebuttal_speech_text = data.get("rebuttal_speech_text")

    result = Speech_Gen(
        motion,
        opening_statement_text,
        role,
        rebuttal_speech_text
    )
    return {"result": result}
