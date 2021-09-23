from typing import List

from calendar_app.model.events.event_base import Event
from calendar_app.model.metrics.metric_base import Metric


class MetricTotalTimeRecruitment(Metric):

    @staticmethod
    def get_metric_data(calendar_events: List[Event]):
        total_seconds = sum([event.duration_seconds for event in calendar_events if
                             event.is_recruitment])
        return MetricTotalTimeRecruitment.get_duration_str(total_seconds)
