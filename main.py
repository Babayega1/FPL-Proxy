from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

FPL_BASE = "https://fantasy.premierleague.com/api"
TIMEOUT = 20  # seconds

session = requests.Session()
session.headers.update({"User-Agent": "FPL-Proxy/1.0"})

# -------------------------------
# TEAMS
# -------------------------------
@app.get("/fpl/teams")
def get_teams():
    """Return all team data."""
    try:
        r = session.get(f"{FPL_BASE}/bootstrap-static/", timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()["teams"]
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error fetching teams: {e}")

# -------------------------------
# EVENTS (gameweeks)
# -------------------------------
@app.get("/fpl/events")
def get_events():
    """Return all gameweek (event) data."""
    try:
        r = session.get(f"{FPL_BASE}/bootstrap-static/", timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()["events"]
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error fetching events: {e}")

# -------------------------------
# PLAYERS BY POSITION
# -------------------------------
@app.get("/fpl/players/goalkeepers")
def get_goalkeepers():
    """Return all goalkeepers."""
    try:
        r = session.get(f"{FPL_BASE}/bootstrap-static/", timeout=TIMEOUT)
        r.raise_for_status()
        return [p for p in r.json()["elements"] if p["element_type"] == 1]
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error fetching goalkeepers: {e}")

@app.get("/fpl/players/defenders")
def get_defenders():
    """Return all defenders."""
    try:
        r = session.get(f"{FPL_BASE}/bootstrap-static/", timeout=TIMEOUT)
        r.raise_for_status()
        return [p for p in r.json()["elements"] if p["element_type"] == 2]
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error fetching defenders: {e}")

@app.get("/fpl/players/midfielders")
def get_midfielders():
    """Return all midfielders."""
    try:
        r = session.get(f"{FPL_BASE}/bootstrap-static/", timeout=TIMEOUT)
        r.raise_for_status()
        return [p for p in r.json()["elements"] if p["element_type"] == 3]
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error fetching midfielders: {e}")

@app.get("/fpl/players/forwards")
def get_forwards():
    """Return all forwards."""
    try:
        r = session.get(f"{FPL_BASE}/bootstrap-static/", timeout=TIMEOUT)
        r.raise_for_status()
        return [p for p in r.json()["elements"] if p["element_type"] == 4]
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error fetching forwards: {e}")

# -------------------------------
# FIXTURES (next 3 gameweeks only)
# -------------------------------
@app.get("/fpl/fixtures/upcoming/{gw}")
def get_upcoming_fixtures(gw: int):
    """
    Return fixtures for the next 3 gameweeks starting from gw.
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
# LIVE EVENT DATA
# -------------------------------
@app.get("/fpl/event/{gw}/live")
def get_live(gw: int):
    """Return live data for a specific gameweek."""
    try:
        r = session.get(f"{FPL_BASE}/event/{gw}/live/", timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error fetching live data: {e}")
