import argparse
import json
import logging
from typing import List, Union, Dict, Any

from calendar_app.model.events.event_base import Event
from calendar_app.model.metrics.metric_extreme_weeks import MetricExtremeWeeks
from calendar_app.model.metrics.metric_most_engagement import MetricMostEngagement
from calendar_app.model.metrics.metric_total_time import MetricTotalTime
from calendar_app.model.metrics.metric_total_time_recruitment import \
    MetricTotalTimeRecruitment
from calendar_app.model.metrics.metric_weekly_averge import MetricWeeklyAverage
from calendar_app.service.parsers.google_event_parser import GoogleEventParser

logger = logging.getLogger(__name__)

SOURCE_NAME = "google"


def get_choices() -> Dict[int, Any]:
    return {
        1: MetricTotalTime("Total time in meetings"),
        2: MetricTotalTimeRecruitment("Total time in recruitment"),
        3: MetricExtremeWeeks("Busiest and relaxed weeks"),
        4: MetricMostEngagement("Top 3 persons with whom you have meetings"),
        5: MetricWeeklyAverage("Average")
    }


def get_parser() -> Union[GoogleEventParser]:
    return {
        "google": GoogleEventParser,
    }.get(SOURCE_NAME, GoogleEventParser)


def interact_with_user(events: List[Event]) -> None:
    choices = get_choices()
    exit_code = len(choices) + 1
    while True:
        for idx, metric in choices.items():
            print(f"{idx} - {metric.name}")
        print(f"{exit_code} - Exit")
        answer = input('Give me some input: ')
        if int(answer) == exit_code:
            print("Exiting")
            break
        if int(answer) not in choices.keys():
            print("Not a valid choice")
            continue
        print("=" * 100)
        print(choices.get(int(answer)).get_metric_data(events))
        print("=" * 100)


def run_app(args) -> None:
    app_secret = json.loads(args.app_secret.read())
    logger.info("Fetching calendar data for the user..")
    try:
        parser_callable = get_parser()()
        print(parser_callable)
        parser_callable.fetch_user_data(app_secret)
        events = parser_callable.get_calendar_events()
    except Exception as e:
        logger.error(f"Error during data fetch {e}")
        return
    logger.info("Done fetching calendar data..")
    interact_with_user(events)


def main() -> int:
    print("running app")
    parser = argparse.ArgumentParser()
    parser.add_argument('--app_secret',
                        metavar='file',
                        type=argparse.FileType('r'),
                        help='JSON file containing app secret',
                        default='client_secret.json')

    parser.set_defaults(func=run_app)

    args = parser.parse_args()
    args.func(args)

    return 0
