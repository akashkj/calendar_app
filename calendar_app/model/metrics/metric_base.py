from abc import abstractmethod
from dataclasses import dataclass
from datetime import timedelta as td
from typing import List

from calendar_app.model.events.event_base import Event


@dataclass
class Metric(object):
    name: str
    description: str = ""

    @staticmethod
    @abstractmethod
    def get_metric_data(calendar_events: List[Event]):
        raise NotImplementedError()

    @staticmethod
    def get_duration_str(duration_in_seconds: int):
        return str(td(seconds=duration_in_seconds))
