from collections import defaultdict
from typing import List
from calendar import month_name

import pytz
from dateutil.tz import tzlocal
from datetime import datetime, timedelta, timezone

from calendar_app.model.events.event_base import Event
from calendar_app.model.metrics.metric_base import Metric

ONE_WEEK_IN_SECONDS = 604800


class MetricWeeklyAverage(Metric):

    @staticmethod
    def get_metric_data(calendar_events: List[Event]) -> str:
        if not calendar_events:
            return "No events to process"
        total_time = 0
        total_meetings = len(calendar_events)
        max_time = calendar_events[0].end_time
        min_time = calendar_events[0].start_time
        for event in calendar_events:
            max_time = max(max_time, event.end_time.replace(tzinfo=pytz.utc))
            min_time = min(min_time, event.start_time.replace(tzinfo=pytz.utc))
            total_time += event.duration_seconds
        total_weeks = int(float((max_time - min_time).days) / 7)
        average_meetings_per_week = float(total_meetings) / total_weeks
        average_time_per_week = MetricWeeklyAverage.get_duration_str(
            int(total_time / total_weeks))
        return "\n".join([
            f"Average number of meetings per week {average_meetings_per_week}",
            f"Average time spent every week in meetings {average_time_per_week}"
        ])
