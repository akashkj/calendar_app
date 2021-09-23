from collections import defaultdict
from typing import List
from calendar import month_name

from calendar_app.model.events.event_base import Event
from calendar_app.model.metrics.metric_base import Metric


class MetricTotalTime(Metric):

    @staticmethod
    def get_metric_data(calendar_events: List[Event]) -> str:
        time_result = []
        duration_by_months = defaultdict(int)
        for event in calendar_events:
            year = event.start_time.year
            month = event.start_time.month
            duration_by_months[(year, month)] += event.duration_seconds
        for year_month, duration in sorted(duration_by_months.items(),
                                           key=lambda x: x[1], reverse=True):
            year, month = year_month
            time_result.append(
                f"{month_name[month]}-{year} : {MetricTotalTime.get_duration_str(duration)}")
        return "\n".join(time_result)
