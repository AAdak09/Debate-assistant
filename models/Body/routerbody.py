from fastapi import APIRouter
from models.Body.Listen import SpeechToTextListener
from models.Body.TTS_Judge import TextToSpeech as JudgeTextToSpeech
from models.Body.Listen2 import SpeechRecognition
from models.Body.TTS import TextToSpeech as SimpleTextToSpeech

router = APIRouter(tags=["Body Endpoints"])

@router.post("/listen/speech_to_text")
def speech_to_text(language: str = "en-IN"):
    listener = SpeechToTextListener(language=language)
    text = listener.listen()
    return {"transcription": text}

@router.post("/tts_judge/speak")
def tts_judge_speak(data: dict):
    text = data.get("text")
    JudgeTextToSpeech(text)
    return {"status": "Speech generated and played"}

@router.get("/listen2/speech_to_text")
def listen2_speech_to_text():
    result = SpeechRecognition()
    return {"transcription": result}

@router.post("/tts/speak")
def tts_speak(data: dict):
    text = data.get("text")
    SimpleTextToSpeech(text)
    return {"status": "Speech generated and played"}