import base64
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .date_helper import convert_strings_to_datetime


# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/gmail.readonly",
]


def _get_google_oauth_creds():
    """Get the OAuth credentials for the Google APIs."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def get_calendar_events(
    time_min: str = None,
    time_max: str = None,
    max_items: int = 200,
):
    """Fetches calendar events within a specified time window.

    Args:
        time_min: Optional start time in ISO format (e.g. "2025-02-20T10:00:00Z")
        time_max: Optional end time in ISO format. Defaults to current time if not provided.
        max_items: Maximum number of items to return.

    Returns:
        A dictionary containing the list of events or an error message.
    """

    try:
        creds = _get_google_oauth_creds()
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        time_min, time_max = convert_strings_to_datetime(time_min, time_max)

        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=time_min.strftime("%Y-%m-%dT%H:%M:%SZ"),
                timeMax=time_max.strftime("%Y-%m-%dT%H:%M:%SZ") if time_max else None,
                maxResults=int(max_items if max_items else 200),
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        events = events_result.get("items", [])

        if not events:
            return {"status": "error", "message": "No upcoming events found."}

        return {"status": "success", "events": events}

    except HttpError as error:
        return {
            "status": "error",
            "message": f"An error occurred: {error}.",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"An unexpected error occurred: {e}.",
        }


def get_emails(max_items: int = 10):
    """Fetches emails.

    Args:
        max_items: Maximum number of items to return.

    Returns:
        A dictionary containing the list of emails or an error message.
    """
    try:
        # Call the Gmail API
        creds = _get_google_oauth_creds()
        service = build("gmail", "v1", credentials=creds)
        results = service.users().messages().list(userId="me", maxResults=10).execute()

        messages = results.get("messages", [])
        if not messages:
            return {"status": "error", "message": "No messages found."}

        parsed_messages = []

        for message in messages:
            result = (
                service.users().messages().get(userId="me", id=message["id"]).execute()
            )

            parsed_message = {}
            parsed_message["snippet"] = result["snippet"]
            parsed_message["date"] = str(
                datetime.datetime.fromtimestamp(int(result["internalDate"]) / 1000.0)
            )

            payload = result["payload"]

            if "headers" in payload:
                for values in payload["headers"]:
                    if values["name"] == "From":
                        parsed_message["from"] = values["value"]
                    if values["name"] == "Subject":
                        parsed_message["subject"] = values["value"]

            # Get the email text
            if "parts" in payload:
                plain_text, html_text = None, None
                for p in payload["parts"]:
                    if p["mimeType"] == "text/plain":
                        plain_text = base64.urlsafe_b64decode(p["body"]["data"]).decode(
                            "utf-8"
                        )
                    if p["mimeType"] == "text/html":
                        html_text = base64.urlsafe_b64decode(p["body"]["data"]).decode(
                            "utf-8"
                        )

                if plain_text:
                    parsed_message["text"] = plain_text
                elif html_text:  # use HTML as fallback if no text is available
                    parsed_message["text"] = html_text
            else:
                # no parts, use body data directly, this is possibly HTML
                data = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8")
                parsed_message["text"] = data

            parsed_messages.append(parsed_message)

        return {"status": "success", "messages": parsed_messages}

    except HttpError as error:
        return {
            "status": "error",
            "message": f"An error occurred: {error}.",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"An unexpected error occurred: {e}.",
        }


if __name__ == "__main__":
    import json

    print("Calendar events")
    events = get_calendar_events()
    print(json.dumps(events, indent=4))

    print("Emails")
    messages = get_emails()
    print(json.dumps(messages, indent=4))
