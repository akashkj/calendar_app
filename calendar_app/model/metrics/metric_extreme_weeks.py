from collections import defaultdict
from datetime import datetime, timedelta
from typing import List, Tuple, DefaultDict

from calendar_app.model.events.event_base import Event
from calendar_app.model.metrics.metric_base import Metric


class MetricExtremeWeeks(Metric):

    @staticmethod
    def get_metric_data(calendar_events: List[Event]) -> str:
        duration_by_weeks = defaultdict(int)
        for event in calendar_events:
            year = event.start_time.year
            week = event.week_number
            duration_by_weeks[(year, week)] += event.duration_seconds
        return MetricExtremeWeeks.get_extreme_weeks(duration_by_weeks)

    @staticmethod
    def get_time_range(year: int, week_number: int) -> Tuple[str, str]:
        week_start = datetime.strptime(f'{year}-W{week_number - 1}-1',
                                       "%Y-W%W-%w").date()
        week_end = week_start + timedelta(days=6.9)
        return str(week_start), str(week_end)

    @staticmethod
    def get_extreme_weeks(duration_by_weeks: DefaultDict[Tuple[int, int], int]) -> str:
        if not duration_by_weeks:
            return "No weeks to analyze"
        time_result = []
        duration_by_weeks = dict(
            sorted(duration_by_weeks.items(), key=lambda item: item[1]))
        (busy_year, busy_week), busy_duration = list(duration_by_weeks.items())[-1]
        (relax_year, relax_week), relax_duration = list(duration_by_weeks.items())[0]
        time_result.append(
            f"Most busy week: {MetricExtremeWeeks.get_time_range(busy_year, busy_week)}, duration: {MetricExtremeWeeks.get_duration_str(busy_duration)}")
        time_result.append(
            f"Most relaxed week: {MetricExtremeWeeks.get_time_range(relax_year, relax_week)}, duration: {MetricExtremeWeeks.get_duration_str(relax_duration)}")
        return "\n".join(time_result)
