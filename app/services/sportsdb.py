import httpx
from datetime import date
from datetime import date as date_cls

BASE_URL = "https://www.thesportsdb.com/api/v1/json"
API_KEY = "123"

async def get_today_events(event_date: date_cls):
    today = event_date.isoformat()
    url = f"{BASE_URL}/{API_KEY}/eventsday.php"
    params = {"d": today, "s": "Soccer"}

    async with httpx.AsyncClient() as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        return r.json().get("events", []) or []

async def get_event_timeline(event_id: str):
    url = f"{BASE_URL}/{API_KEY}/lookuptimeline.php"
    params = {"id": event_id}

    async with httpx.AsyncClient() as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        return r.json().get("timeline", [])

async def get_event_by_id(event_id: str):
    url = f"{BASE_URL}/{API_KEY}/lookupevent.php"
    params = {"id": event_id}

    async with httpx.AsyncClient() as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        events = r.json().get("events")
        return events[0] if events else None

async def get_team_by_id(team_id: str):
    url = f"{BASE_URL}/{API_KEY}/lookupteam.php"
    params = {"id": team_id}

    async with httpx.AsyncClient() as client:
        r = await client.get(url, params=params)
        r.raise_for_status()

        teams = r.json().get("teams")
        return teams[0] if teams else None
