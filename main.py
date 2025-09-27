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
    r = session.get(f"{FPL_BASE}/bootstrap-static/", timeout=TIMEOUT)
    return [p for p in r.json()["elements"] if p["element_type"] == 1]

@app.get("/fpl/players/defenders")
def get_defenders():
    """Return all defenders."""
    r = session.get(f"{FPL_BASE}/bootstrap-static/", timeout=TIMEOUT)
    return [p for p in r.json()["elements"] if p["element_type"] == 2]

@app.get("/fpl/players/midfielders")
def get_midfielders():
    """Return all midfielders."""
    r = session.get(f"{FPL_BASE}/bootstrap-static/", timeout=TIMEOUT)
    return [p for p in r.json()["elements"] if p["element_type"] == 3]

@app.get("/fpl/players/forwards")
def get_forwards():
    """Return all forwards."""
    r = session.get(f"{FPL_BASE}/bootstrap-static/", timeout=TIMEOUT)
    return [p for p in r.json()["elements"] if p["element_type"] == 4]

# -------------------------------
# PLAYER LOOKUP (by ID)
# -------------------------------
@app.get("/fpl/player/{player_id}")
def get_player(player_id: int):
    """
    Return a single player by ID.
    Example: /fpl/player/101 -> player info
    """
    try:
        r = session.get(f"{FPL_BASE}/bootstrap-static/", timeout=TIMEOUT)
        r.raise_for_status()
        for p in r.json()["elements"]:
            if p["id"] == player_id:
                return p
        raise HTTPException(status_code=404, detail="Player not found")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error fetching player: {e}")

# -------------------------------
# FIXTURES (next 3 gameweeks only)
# -------------------------------
@app.get("/fpl/fixtures/upcoming/{gw}")
def get_upcoming_fixtures(gw: int):
    """
    Return fixtures for the next 3 gameweeks starting from gw.
    Example: /fpl/fixtures/upcoming/8 -> GW8, GW9, GW10
    """
    r = session.get(f"{FPL_BASE}/fixtures/", timeout=TIMEOUT)
    all_fixtures = r.json()
    return [f for f in all_fixtures if f.get("event") and gw <= f["event"] < gw + 3]

# -------------------------------
# LIVE EVENT DATA
# -------------------------------
@app.get("/fpl/event/{gw}/live")
def get_live(gw: int):
    """Return live data for a specific gameweek."""
    r = session.get(f"{FPL_BASE}/event/{gw}/live/", timeout=TIMEOUT)
    return r.json()
