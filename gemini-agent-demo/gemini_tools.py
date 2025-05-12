from typing import Dict

from google import genai
from google.genai import types

from dotenv import load_dotenv
load_dotenv()

import google_api_service


def get_calendar_events(
    date_time_min: str = "week start",
    date_time_max: str = "week end",
    max_items: int = 200,
) -> Dict:
    """
    Fetches google calendar events within a specified time window.

    Args:
        date_time_min: start time in ISO format (e.g. "2025-02-20T10:00:00Z") or you can use magic words like "next week start" or "last month start".
        date_time_max: end time in ISO format or you can use magic words like "next week end" or "last month end".
        max_items: The maximum number of events to retrieve from the calendar.

    Returns:
        A dictionary containing the list of events or an error message.
    """
    event_details = google_api_service.get_calendar_events(
        time_min=date_time_min,
        time_max=date_time_max,
        max_items=max_items,
    )
    return event_details


# Configure the client and model
client = genai.Client()

config = types.GenerateContentConfig(tools=[get_calendar_events])

# Make the request
response = client.models.generate_content(
    model="gemini-2.5-flash-preview-04-17",
    contents="Get this week's meetings",
    config=config,
)

print(response.text)
