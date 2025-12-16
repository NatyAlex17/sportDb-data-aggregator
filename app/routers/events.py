from fastapi import APIRouter, HTTPException, Query
from datetime import date
from app.services.sportsdb import (
    get_today_events,
    get_event_timeline,
    get_event_by_id
)
from app.util.helpers import compute_match_minute, get_kickoff_datetime, minutes_to_kickoff, normalize_status, resolve_team_badge

router = APIRouter(prefix="/events", tags=["Events"])

@router.get("/today")
async def today_events(
    date_param: date | None = Query(
        default=None,
        description="Date in YYYY-MM-DD format. Defaults to today."
    )
):
    target_date = date_param or date.today()

    events = await get_today_events(target_date)
    response = []

    for e in events:
        event_id = e["idEvent"]
        
        #timeline = await get_event_timeline(event_id)

        status = normalize_status(e.get("strStatus"))

        minute = compute_match_minute(
            e.get("dateEvent"),
            e.get("strTime"),
            status
        )
        home_badge = await resolve_team_badge(e, "Home")
        away_badge = await resolve_team_badge(e, "Away")
        kickoff = get_kickoff_datetime(
            e.get("dateEvent"),
            e.get("strTime")
        )
        
        response.append({
            "id": e["idEvent"],
            "home_team": e["strHomeTeam"],
            "away_team": e["strAwayTeam"],
            "league": {
                "id": e.get("idLeague"),
                "name": e.get("strLeague"),
            },
            "home_badge": home_badge,
            "away_badge": away_badge,
            "home_score": int(e["intHomeScore"] or 0),
            "away_score": int(e["intAwayScore"] or 0),
            "status": status,
            "minute": minute,
            "kickoff_time_utc": kickoff.isoformat() if kickoff else None,
            "minutes_to_kickoff": minutes_to_kickoff(kickoff, status),

            #"timeline": timeline
        })

    return response

@router.get("/{event_id}")
async def event_by_id(event_id: str):
    event = await get_event_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    timeline = await get_event_timeline(event_id)
    
    status = normalize_status(event.get("strStatus"))
    minute = compute_match_minute(
        event.get("dateEvent"),
        event.get("strTime"),
        status
    )
    home_badge = await resolve_team_badge(event, "Home")
    away_badge = await resolve_team_badge(event, "Away")
    kickoff = get_kickoff_datetime(
        event.get("dateEvent"),
        event.get("strTime")
    )
    return {
        "id": event["idEvent"],
        "home_team": event["strHomeTeam"],
        "away_team": event["strAwayTeam"],
        "league": {
            "id": event.get("idLeague"),
            "name": event.get("strLeague"),
        },
        "home_badge": home_badge,
        "away_badge": away_badge,
        "home_score": int(event["intHomeScore"] or 0),
        "away_score": int(event["intAwayScore"] or 0),
        "status": status,
        "minute": minute,
        "kickoff_time_utc": kickoff.isoformat() if kickoff else None,
        "minutes_to_kickoff": minutes_to_kickoff(kickoff, status),

        "timeline": timeline
    }
