from typing import Sequence

from googleapiclient.discovery import Resource
from langchain_google_community import CalendarToolkit
from langchain_google_community.calendar.utils import (
    build_calendar_service,
    get_google_credentials,
)

from langchain_core.tools import BaseTool

DEFAULT_SCOPES: list[str] = ["https://www.googleapis.com/auth/calendar"]


def get_calendar_tools(
    token_file: str = "tools/token.json",
    client_secrets_file: str = "tools/credentials.json",
    scopes: Sequence[str] | None = None,
) -> list[BaseTool]:
    """Return Google Calendar LangChain tools.
    Uses OAuth credentials from local files and builds a Calendar API resource.
    """
    credentials = get_google_credentials(
        token_file=token_file,
        scopes=list(scopes) if scopes is not None else DEFAULT_SCOPES,
        client_secrets_file=client_secrets_file,
    )
    api_resource: Resource = build_calendar_service(credentials=credentials)
    return CalendarToolkit(api_resource=api_resource).get_tools()
