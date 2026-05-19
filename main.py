from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from Market_Research_Agent.market_research import market_research
import markdown
from Multi_Persona_System.multi_persona import multi_persona
from fastapi.middleware.cors import CORSMiddleware


class research(BaseModel):
    name:str
    description:str
    pricing:str
    innovations:str

class persona(BaseModel):
    name:str
    description:str
    pricing:str
    innovations:str

app=FastAPI()
# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace later with frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/research',response_class=HTMLResponse)
async def marketresearch(data:research):

    report=market_research(data.name,data.description,data.pricing,data.innovations)

    html=markdown.markdown(report)
    
    return html

@app.post('/persona',response_class=HTMLResponse)
async def multipersona(data:persona):

    report=multi_persona(data.name,data.description,data.pricing,data.innovations)

    html=markdown.markdown(report)
    
    return html


