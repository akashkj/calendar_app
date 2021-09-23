from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Event(object):
    id: str
    summary: str
    description: str
    start_time: datetime
    end_time: datetime
    attendees: List[str]
    duration_seconds: int
    week_number: int
    is_recruitment: bool
