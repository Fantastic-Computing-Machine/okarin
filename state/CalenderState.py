from pydantic import BaseModel, Field
from datetime import date, datetime

class CalenderState(BaseModel):
    event_title: str = Field(..., description="Title of the calendar event")
    event_date: str = Field(datetime.now().strftime("%Y-%m-%d"), description="Date of the event in YYYY-MM-DD format")
    event_time: str = Field(
        datetime.now().strftime("%H:%M"),
        description="Time of the event in HH:MM format",
    )
    event_duration_minutes: int = Field(60, description="Duration of the event in minutes")
    event_description: str | None = Field(
        None, description="Optional description of the event"
    )