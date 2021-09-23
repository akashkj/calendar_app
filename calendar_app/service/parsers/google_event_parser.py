import pickle
from datetime import datetime
from logging import getLogger
from traceback import print_exc
from typing import List

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from calendar_app.model.events.event_base import Event
from calendar_app.model.events.google_event import GoogleEvent
from calendar_app.service.parsers.parser_base import EventParser

scopes = ['https://www.googleapis.com/auth/calendar.readonly',
          'https://www.googleapis.com/auth/calendar.events.readonly']
user_credential_file = "google_user_token.pkl"
DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S+%z"  # "2016-03-17T20:15:00+05:30"

logger = getLogger(__name__)


class GoogleEventParser(EventParser):

    def _populate_credentials(self, client_secret: dict) -> None:
        if self.user_credentials:
            return
        try:
            self.user_credentials = pickle.load(open(user_credential_file, "rb"))
            logger.info("Using token already present..")
        except IOError:
            logger.info("No client token present.. acquiring new..")
            flow = InstalledAppFlow.from_client_config(client_secret, scopes=scopes)
            self.user_credentials = flow.run_console()
            pickle.dump(self.user_credentials, open(user_credential_file, "wb"))

    def fetch_user_data(self, client_secret: dict) -> None:
        try:
            self._populate_credentials(client_secret)
            self.service = build("calendar", "v3", credentials=self.user_credentials)
            self.data = self.service.calendarList().list().execute()
        except Exception as e:
            logger.error(e)
            print_exc()

    def get_calendar_events(self) -> List[Event]:
        logger.info("Getting events")
        if not self.data:
            return []
        calendar_id = self.data.get('items')[2].get('id')
        logger.info(f"Got calendar id - {calendar_id}")
        events: List[dict] = self.service.events().list(calendarId=calendar_id,
                                                        timeZone="Asia/Kolkata").execute().get(
            "items", [])
        return GoogleEventParser._get_events_objs(events)

    @staticmethod
    def _get_events_objs(events: List[dict]) -> List[Event]:
        event_objs = []
        for event in events:
            event_id = event.get("id")
            summary: str = event.get("summary", "")
            description: str = event.get("description", "")
            start_time: datetime = datetime.fromisoformat(
                event.get("start", {}).get("dateTime", datetime.now().isoformat()))
            end_time: datetime = datetime.fromisoformat(
                event.get("end", {}).get("dateTime", datetime.now().isoformat()))
            duration_seconds: int = (end_time - start_time).seconds
            week_number = start_time.isocalendar()[1]
            is_recruitment = "recruitment" in summary.lower() or "recruitment" in description.lower()
            attendees: List[str] = [
                attendee.get("displayName", attendee.get("email").split("@")[0])
                for attendee in event.get("attendees", []) if
                not attendee.get("self", False)]
            event_objs.append(
                GoogleEvent(id=event_id, summary=summary, description=description,
                            start_time=start_time, end_time=end_time,
                            duration_seconds=duration_seconds, week_number=week_number,
                            is_recruitment=is_recruitment, attendees=attendees))
        return event_objs
