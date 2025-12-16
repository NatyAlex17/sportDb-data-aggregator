from pydantic import BaseModel 
from enum import Enum

class MatchStatus(str, Enum):
    TBD = "TBD"
    NS = "NS"
    FIRST_HALF = "1H"
    HT = "HT"
    SECOND_HALF = "2H"
    ET = "ET"
    PENALTY_IN_PROGRESS = "P"
    FT = "FT"
    AET = "AET"
    PEN = "PEN"
    BT = "BT"
    SUSPENDED = "SUSP"
    INTERRUPTED = "INT"
    POSTPONED = "PST"
    CANCELLED = "CANC"
    ABANDONED = "ABD"
    AWARDED = "AWD"
    WALKOVER = "WO"


class TimelineItem(BaseModel):
    time: str | None
    event: str | None
    team: str | None
    player: str | None

class Event(BaseModel):
    id: str
    home_team: str
    away_team: str
    league: str
    date: str
    time: str | None

class TeamInfo(BaseModel):
    name: str
    badge: str | None
    score: int


class EventWithTimeline(BaseModel):
    id: str
    home: TeamInfo
    away: TeamInfo
    status: MatchStatus
    minute: int | None
    timeline: list[TimelineItem]
