from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .library.helpers import *
from app.routers import twoforms, unsplash, accordion
from pydantic import BaseModel
import json,re

import openai
from dotenv import load_dotenv
load_dotenv()
import os

openai.api_key = os.environ["OPENAI_API_KEY"]
openai.organization = os.environ["OPENAI_ORGANIZATION"]
_RE_COMBINE_WHITESPACE = re.compile(r"\s+")


app = FastAPI()


PROMPT_BASE="""Paraphrase female-biased or male-biased passages to neutral text avoiding gender-biased words from the list: 
            \n\nactive, affectionate, adventurous, childish, aggressive, aggression, cheerful, ambitioned, commitment, communal, assertive, compassionate, athletic,
            connected, autonomous, considerate, cooperative, challenge, dependent, dependable, compete, competitive, emotional, confident, empath, courageous, feminine, 
            decided, flatterable, decisive, gentle, decision, honest, determined, interpersonal, dominant, interdependent, interpersonal, forceful, kind, greedy, kinship, 
            headstrong, loyalty, hierarchy, modesty, hostility, nag, impulsive, nurture, independent, pleasant, individual, polite, intellectual, quiet, lead, reason, logic, 
            sensitive, masculine, submissive, objective, support, opinion, sympathy, outspoken, tender, persist, together, trustworthy, reckless, understandable, stubborn, warm-hearted, 
            superior, self-confident, boast, proud, develop warm client relationships, men, woman, female, male\n\n
            Input: We’re looking for strong…\nOutput: We’re looking for exceptional…\n###\nInput: Men who thrive in a competitive atmosphere…\nOutput: Person who is motivated by high goals…\n###\nInput: Candidates who are assertive…\nOutput: Candidates who are go-getters…\n###\nInput: We are a community of concerned…\nOutput: We are a team focused on…\n###\nInput: Have a polite and pleasant style…\nOutput: Are professional and courteous…\n###\nInput: Nurture and connect with customers.\nOutput:Provide great customer service.\n###\nInput:We are determined company that delivers superior plumbing.\nOutput:We are a plumbing company that delivers great service.\n###\nInput: Demonstrated ability to act decisively in emergencies.\nOutput: Demonstrated ability to make quick decisions in emergencies.\n###\nInput: Good salesmen\nOutput: Good salesperson\n###\nInput: Strong women who is not afraid to take risks\nOutput:  Person not afraid of challenges\n###\nInput: Sensitive men who is knows how to establish good relationship with customer\nOutput: Person who knows how to establish good relationship with customer\n###\n""",


def build_query(INPUT):
    if type(INPUT) == str:
        INPUT=INPUT.replace("\n","")
        INPUT  = _RE_COMBINE_WHITESPACE.sub(" ", INPUT).strip()
        QUERY_BASE= "Input: {}".format(INPUT.strip())
        return "{}{}\nOutput: ".format(PROMPT_BASE,QUERY_BASE)



templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(unsplash.router)
app.include_router(twoforms.router)
app.include_router(accordion.router)

@app.post('/api',response_class=JSONResponse)
async def get_prediction(data: Request):
    print()
    d = await data.json()
    #return json.loads(d)
    text = d['data']
    print(text)
    
    QUERY = build_query(text)
    api_response =  openai.Completion.create(
        engine="davinci",
        prompt=QUERY,
        temperature=0.25,
        max_tokens=152,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"]
    )
    print(QUERY)
    print(api_response)
    if api_response['choices'] and api_response["choices"][0].text:
        return json.dumps({"data":api_response["choices"][0].text})
    else:
        return json.dumps({'data':text})

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = openfile("home.md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})

#More CV
# @app.get("/page/{page_name}", response_class=HTMLResponse)
# async def show_page(request: Request, page_name: str):
#     data = openfile(page_name+".md")
#     return templates.TemplateResponse("page.html", {"request": request, "data": data})
