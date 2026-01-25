from typing import Sequence

from googleapiclient.discovery import Resource
from langchain_google_community.calendar.utils import (
    build_calendar_service,
    get_google_credentials,
)

from langchain_google_community import (
    CalendarCreateEvent,
    CalendarDeleteEvent,
    CalendarSearchEvents,
    CalendarUpdateEvent,
)

from langchain_core.tools import BaseTool

DEFAULT_SCOPES: list[str] = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/tasks",
]

GMAIL_API_SCOPES: list[str] = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
]


ALL_SCOPES: list[str] = DEFAULT_SCOPES + GMAIL_API_SCOPES


def get_calendar_tools(
    token_file: str = "config/token.json",
    client_secrets_file: str = "config/credentials.json",
    scopes: Sequence[str] | None = None,
) -> list[BaseTool]:
    """Return Google Calendar LangChain tools.
    Uses OAuth credentials from local files and builds a Calendar API resource.
    """
    credentials = get_google_credentials(
        token_file=token_file,
        scopes=list(scopes) if scopes is not None else ALL_SCOPES,
        client_secrets_file=client_secrets_file,
    )
    api_resource: Resource = build_calendar_service(credentials=credentials)
    create_event = CalendarCreateEvent(api_resource=api_resource)
    create_event.description += (
        "Note: Default event duration should be 1 hour if not specified."
    )
    return [
        create_event,
        CalendarSearchEvents(api_resource=api_resource),
        CalendarUpdateEvent(api_resource=api_resource),
        CalendarDeleteEvent(api_resource=api_resource),
    ]
