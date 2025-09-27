from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

FPL_BASE = "https://fantasy.premierleague.com/api"
TIMEOUT = 20  # seconds

session = requests.Session()
session.headers.update({"User-Agent": "FPL-Proxy/1.0"})

# -------------------------------
# BOOTSTRAP FILTERS (small chunks)
# -------------------------------
@app.get("/fpl/players")
def get_players():
    """Return only player (elements) data."""
    try:
        r = session.get(f"{FPL_BASE}/bootstrap-static/", timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()["elements"]
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error fetching players: {e}")

@app.get("/fpl/teams")
def get_teams():
    """Return only team data."""
    try:
        r = session.get(f"{FPL_BASE}/bootstrap-static/", timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()["teams"]
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error fetching teams: {e}")

@app.get("/fpl/events")
def get_events():
    """Return only event (gameweek) data."""
    try:
        r = session.get(f"{FPL_BASE}/bootstrap-static/", timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()["events"]
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error fetching events: {e}")

# -------------------------------
# FIXTURES: next 3 gameweeks only
# -------------------------------
@app.get("/fpl/fixtures/upcoming/{gw}")
def get_upcoming_fixtures(gw: int):
    """
    Return fixtures for the next 3 gameweeks starting from `gw`.
    Example: /fpl/fixtures/upcoming/8 -> GW8, GW9, GW10
    """
    try:
        r = session.get(f"{FPL_BASE}/fixtures/", timeout=TIMEOUT)
        r.raise_for_status()
        all_fixtures = r.json()
        return [f for f in all_fixtures if f.get("event") and gw <= f["event"] < gw + 3]
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error fetching fixtures: {e}")

# -------------------------------
# LIVE EVENT DATA (per gameweek)
# -------------------------------
@app.get("/fpl/event/{gw}/live")
def get_live(gw: int):
    """Return live data for a specific gameweek."""
    try:
        r = session.get(f"{FPL_BASE}/event/{gw}/live/", timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error fetching live event: {e}")
