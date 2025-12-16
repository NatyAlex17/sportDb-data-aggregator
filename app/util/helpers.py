from typing import Optional
from app.models.schemas import MatchStatus
from app.services.sportsdb import get_team_by_id
from datetime import datetime, timezone
from datetime import datetime, timezone


def normalize_status(raw_status: str | None) -> MatchStatus:
    if not raw_status:
        return MatchStatus.NS

    
    STATUS_MAP = {
        "TBD": MatchStatus.TBD,
        "NS": MatchStatus.NS,
        "1H": MatchStatus.FIRST_HALF,
        "HT": MatchStatus.HT,
        "2H": MatchStatus.SECOND_HALF,
        "ET": MatchStatus.ET,
        "P": MatchStatus.PENALTY_IN_PROGRESS,
        "FT": MatchStatus.FT,
        "AET": MatchStatus.AET,
        "PEN": MatchStatus.PEN,
        "BT": MatchStatus.BT,
        "SUSP": MatchStatus.SUSPENDED,
        "INT": MatchStatus.INTERRUPTED,
        "PST": MatchStatus.POSTPONED,
        "CANC": MatchStatus.CANCELLED,
        "ABD": MatchStatus.ABANDONED,
        "AWD": MatchStatus.AWARDED,
        "WO": MatchStatus.WALKOVER,
        "Match Finished": MatchStatus.FT
    }

    return STATUS_MAP.get(raw_status, MatchStatus.NS)

def compute_match_minute(
    date_event: str | None,
    time_event: str | None,
    status: MatchStatus
) -> Optional[int]:
    # Only compute minute when the clock is running
    LIVE_STATUSES = {
        MatchStatus.FIRST_HALF,   # 1H
        MatchStatus.SECOND_HALF,  # 2H
        MatchStatus.ET,           # Extra Time
        MatchStatus.PENALTY_IN_PROGRESS,  # P
    }

    if status not in LIVE_STATUSES:
        return None

    if not date_event or not time_event:
        return None

    try:
        kickoff = datetime.fromisoformat(
            f"{date_event}T{time_event}"
        ).replace(tzinfo=timezone.utc)
    except ValueError:
        return None

    now = datetime.now(timezone.utc)
    minutes = int((now - kickoff).total_seconds() // 60)

    # Clamp to realistic football bounds
    if minutes < 0:
        return 0
    if minutes > 130:  # 120 + stoppage safety
        return 130

    return minutes
async def resolve_team_badge(event: dict, side: str):
    badge_key = f"str{side}TeamBadge"
    team_id_key = f"id{side}Team"

    if event.get(badge_key):
        return event[badge_key]

    team_id = event.get(team_id_key)
    if not team_id:
        return None

    team = await get_team_by_id(team_id)
    return team.get("strTeamBadge") if team else None


def get_kickoff_datetime(date_event: str | None, time_event: str | None):
    if not date_event or not time_event:
        return None

    return datetime.fromisoformat(
        f"{date_event}T{time_event}"
    ).replace(tzinfo=timezone.utc)

def minutes_to_kickoff(kickoff: datetime | None, status: MatchStatus):
    if not kickoff or status != MatchStatus.NS:
        return None

    now = datetime.now(timezone.utc)
    diff = int((kickoff - now).total_seconds() // 60)

    return max(diff, 0)
