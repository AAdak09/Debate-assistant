from fastapi import FastAPI

from models.AI_Judge.routerai_judgemock import router as judge_router
from models.Asain_Par.routerasianpar import router as asian_par_router
from models.MockDebate.routermockdebate import router as mock_debate_router
from models.POI_Engine.routerpoiengine import router as poi_router
from models.Speech_Engine.routerspeechengine import router as speech_router
from models.Body.routerbody import router as body_router

app = FastAPI()

app.include_router(judge_router)
app.include_router(asian_par_router)
app.include_router(mock_debate_router)
app.include_router(poi_router)
app.include_router(speech_router)
app.include_router(body_router)