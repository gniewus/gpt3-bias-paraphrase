import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .library.helpers import *
from app.routers import twoforms, unsplash, accordion
from pydantic import BaseModel
import json
import re

import openai
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]
openai.organization = os.environ["OPENAI_ORGANIZATION"]
_RE_COMBINE_WHITESPACE = re.compile(r"\s+")


app = FastAPI()

PROMPT_BASE = "Paraphrase gender-biased passages to neutral text avoiding gender-biased words like active, affectionate, adventurous, childish, aggressive, aggression, cheerful, ambitioned, commitment, communal, assertive, compassionate, athletic, connected, autonomous, considerate, cooperative, challenge, dependent, dependable, compete, competitive, emotional, confident, empath, courageous, feminine, decided, flatterable, decisive, gentle, decision, honest, determined, interpersonal, dominant, interdependent, interpersonal, forceful, kind, greedy, kinship, headstrong, loyalty, hierarchy, modesty, hostility, nag, impulsive, nurture, independent, pleasant, individual, polite, intellectual, quiet, lead, reason, logic, logically, sensitive, masculine, submissive, objective, support, opinion, sympathy, outspoken, tender, persist, together, trustworthy, reckless, understandable, understanding,stubborn, warm-hearted, superior, self-confident, boast, proud, develop warm client relationships, men, woman, female, male, assist, assistant\n\nWe’re looking for a strong businessman.\nParaphrase: We’re looking for an exceptional business person.\nMen who thrive in a competitive atmosphere.\nParaphrase: Person who is motivated by high goals.\nWe are looking for a reliable and polite waitress.\nParaphrase: Our company seeks a reliable server who is respectful towards clients\nCandidates who are assertive.\nParaphrase: Candidates who are go-getters.\nHave a polite and pleasant style.\nParaphrase: Are professional and courteous.\nNurture and connect with customers.\nParaphrase: Provide great customer service.\nWe are a determined company that delivers superior plumbing.\nParaphrase: We are a plumbing company that delivers great service.\nDemonstrated ability to act decisively in emergencies.\nParaphrase: Demonstrated ability to make quick decisions in emergencies.\nGood salesmen with strong computer skills.\nParaphrase: Good salesperson who knows how to efficiently use the computer.\nStrong women who is not afraid to take risks.\nParaphrase:  Person not afraid of challenges.\nSensitive men who know how to establish a good relationship with the customer\nParaphrase: Person who knows how to establish a great relationship with the customer\nA great salesman who is open to new challenges.\nParaphrase: Great salesperson who is open to new challenges.\nThe company boasts impressive salaries, allowing our employees with financial independence.\nParaphrase: Our company offers excellent benefits, allowing our employees to maintain financial independence.\nSupport office team and assist with departmental procedures so that work progresses more efficiently.\nParaphrase: Work closely with the office team to organize departmental procedures so that work progresses more efficiently.\n We boast a competitive compensation package.\nParaphrase: We offer excellent compensation packages.\nTake our sales challenge! Even if you have no previous experience, we will facilitate the acquisition of your sales abilities.\nParaphrase: We are a company that is committed to facilitating employees to enhance their sales abilities.\nStrong communicator.\nParaphrase: A person who is good at communicating with others.\nBe a leader in your store, representing our exclusive brand.\nParaphrase: Be a role model in your store, representing our exclusive brand.\nJoin our sales community! Even if you have no previous experience, we will help nurture and develop your sales talents.\nParaphrase: Join our company and help develop your sales abilities.\nWe are a dominant engineering firm that boasts many leading clients.\nParaphrase: We are an engineering company that has many leading clients.\nStrong communication and influencing skills.\nParaphrase: Communication and influencing skills.\nAnalyze problems logically and troubleshoot to determine needed repairs.\nParaphrase: Respond to problems and troubleshoot them to uncover needed repairs.\nSensitive to clients’ needs, can develop warm client relationships.\nParaphrase: Person who understands client needs and can establish great relationships with them.\n",


def build_query(INPUT):
    if type(INPUT) == str:
        INPUT = INPUT.replace("\n", "")
        INPUT = _RE_COMBINE_WHITESPACE.sub(" ", INPUT).strip()
        #print("build_query")
        #print(PROMPT_BASE[0])
        #print("{}{}\nParaphrase: ".format(PROMPT_BASE[0], INPUT.strip()))
        return "{}{}\nParaphrase: ".format(PROMPT_BASE[0], INPUT.strip())


templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(unsplash.router)
app.include_router(twoforms.router)
app.include_router(accordion.router)


@app.post('/api', response_class=JSONResponse)
async def get_prediction(data: Request):
    print()
    d = await data.json()
    # return json.loads(d)
    text = d['data']
    print("text",text)

    QUERY = build_query(text)
    api_response = openai.Completion.create(
        engine="curie-instruct-beta",
        prompt=QUERY,
        temperature=0.20,
        max_tokens=204,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=0.51,

        stop=["\n"]
    )
    print(QUERY)
    print(api_response)
    if api_response['choices'] and api_response["choices"][0].text:
        return json.dumps({"data": api_response["choices"][0].text})
    else:
        return json.dumps({'data': text})


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = openfile("home.md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})

# More CVs
# @app.get("/page/{page_name}", response_class=HTMLResponse)
# async def show_page(request: Request, page_name: str):
#     data = openfile(page_name+".md")
#     return templates.TemplateResponse("page.html", {"request": request, "data": data})
