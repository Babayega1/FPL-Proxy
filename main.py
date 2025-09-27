from fastapi import FastAPI
import requests

app = FastAPI()

FPL_BASE = "https://fantasy.premierleague.com/api"

@app.get("/fpl/bootstrap")
def get_bootstrap():
    r = requests.get(f"{FPL_BASE}/bootstrap-static/")
    return r.json()

@app.get("/fpl/fixtures")
def get_fixtures():
    r = requests.get(f"{FPL_BASE}/fixtures/")
    return r.json()

@app.get("/fpl/event/{gw}/live")
def get_live(gw: int):
    r = requests.get(f"{FPL_BASE}/event/{gw}/live/")
    return r.json()
