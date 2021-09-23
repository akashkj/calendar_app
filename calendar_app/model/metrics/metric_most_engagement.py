from collections import defaultdict
from typing import List

from calendar_app.model.events.event_base import Event
from calendar_app.model.metrics.metric_base import Metric


class MetricMostEngagement(Metric):

    @staticmethod
    def get_metric_data(calendar_events: List[Event]):
        result = defaultdict(int)
        for event in calendar_events:
            if not event.attendees:
                continue
            for person in event.attendees:
                result[person] += event.duration_seconds
        result = sorted(result.items(), key=lambda item: item[1], reverse=True)
        return "\n".join(
            [f"{name} - {MetricMostEngagement.get_duration_str(duration)}" for
             name, duration in result[-3:]])
