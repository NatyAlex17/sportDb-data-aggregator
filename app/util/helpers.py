from app.models.schemas import MatchStatus
from app.services.sportsdb import get_team_by_id
from datetime import datetime, timezone


def normalize_status(raw_status: str | None) -> MatchStatus:
    if not raw_status:
        return MatchStatus.NS

    s = raw_status.lower()

    if "live" in s:
        return MatchStatus.LIVE
    if "half" in s:
        return MatchStatus.HT
    if "finished" in s:
        return MatchStatus.FT
    if "postponed" in s:
        return MatchStatus.POSTPONED

    return MatchStatus.NS

from datetime import datetime, timezone

def compute_match_minute(
    date_event: str | None,
    time_event: str | None,
    status: MatchStatus
) -> int | None:
    if status not in {MatchStatus.LIVE, MatchStatus.HT}:
        return None

    if not date_event or not time_event:
        return None

    kickoff = datetime.fromisoformat(
        f"{date_event}T{time_event}"
    ).replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)
    minutes = int((now - kickoff).total_seconds() // 60)

    # Clamp values
    if minutes < 0:
        return 0
    if minutes > 120:
        return 120

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
