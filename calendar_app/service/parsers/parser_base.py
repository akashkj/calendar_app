from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Any

from calendar_app.model.events.event_base import Event


@dataclass
class EventParser(object):
    data: Any = None
    service: Any = None
    user_credentials: Any = None

    @abstractmethod
    def fetch_user_data(self, client_secret: dict) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_calendar_events(self) -> List[Event]:
        raise NotImplementedError()
