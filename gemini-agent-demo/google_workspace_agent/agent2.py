from typing import Dict
from google.adk.agents import Agent
from . import google_api_service


def get_emails(max_items: int = 10) -> Dict:
    """
    Fetches gmail messages.

    Args:
        max_items: The maximum number of messages to retrieve from the inbox.

    Returns:
        A dictionary containing the list messages or an error message.
    """
    emails = google_api_service.get_emails(max_items=max_items)
    return emails


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


email_agent = Agent(
    name="email_agent",
    model="gemini-2.5-flash-preview-04-17",
    description=("Agent to answer questions about Emails."),
    instruction="""
    You are an AI assistant designed to review the user's emails, and provide summaries, and write emails

    Use the tool only if it is needed.

    Instructions:
    1. If required, use the `get_emails` tool to fetch the latest emails. If the user does not specify the number of emails, use max_items=10 as default.
    2. Present the information in an easy to digest way.

    Retrieval tools:
    - If the 'get_emails' tool returns an error message, inform the user and provide troubleshooting steps.
    """,
    tools=[get_emails],
)

calendar_agent = Agent(
    name="calendar_agent",
    model="gemini-2.5-flash-preview-04-17",
    description=("Agent to answer questions about Google Calendar events."),
    instruction="""
    You are an AI assistant designed to review the user's calendar and emails,
    extracting the most important details to highlight for weekly overviews.

    If you dont have a date range, ask the user for the date range.
    If the user has given you anything like a date range, use that date range with the following assumptions:
    - If a week is mentioned, just use the whole week, Monday to Sunday.
    - If a month is mentioned, just use the whole month, first to last day.
    - If a year is mentioned, just use the whole year, January 1 to December 31.
    - If a year is not mentioned, assume the user wants the current year.
    - Expect current/this week, or next week, or next month, or recent past week, or recent past month, or recent past year.

    Use the tool only if it is needed.

    Instructions:
    1. If you have low confidence in the date range, ask the user to confirm the date range.
    2. If required, use the `get_calendar_events` tool to fetch the calendar events. Be sure to use the correct date range in ISO format.
       If the user does not specify the number of meetings, use max_items=200 as default.
    3. Present the information in an easy to digest way.

    Retrieval tools:
    - If the 'get_calendar_events' tool returns an error message, inform the user and provide troubleshooting steps.
    """,
    tools=[get_calendar_events],
)


root_agent = Agent(
    name="google_workspace_agent",
    model="gemini-2.5-flash-preview-04-17",
    description=("Agent to answer questions about Google Calendar events and Emails."),
    instruction="""
    You are an AI assistant designed to help users get info about their calendar events and emails.

    Your job is to help the user accomplish their goal, you figure out what child agent you should use and triage to the right one.

    Skills:
    - Get info about calendar events. Transfer to the `calendar_agent` for this.
    - Get info about email events. Transfer to the `email_agent` for this.
    - Draft emails
    - Tell a joke

    Refine the user intent:
    - If the user's intent is not clear, ask the user for clarification.
    
    Failover:
    - If the user wants to talk about something else, refuse and redirect to your skillset.
    """,
    sub_agents=[
        calendar_agent,
        email_agent,
    ],
)
