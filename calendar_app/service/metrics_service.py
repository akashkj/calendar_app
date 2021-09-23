from calendar_app.model.metrics.metric_total_time import MetricTotalTime


class MetricsService(object):

    def __init__(self) -> None:
        self._metrics = MetricTotalTime()
        self._user = None

    def add_metrics(self):
        pass

    def evaluate_metrics(self):
        pass

    def display_metrics(self):
        pass