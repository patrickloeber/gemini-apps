
https://developers.google.com/workspace/calendar/api/quickstart/python


pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip install google-adk


### OAuth setup for Google Calendar and Gmail

1. Enable Google Calendar API and Gmail API in the Google Cloud Console
2. Configure OAuth for Google Calendar and Google Drive
    - add client: Desktop type, download the JSON file and rename it `credentials.json` and put it in the project directory
    - add Scope for Calendar and Gmail
    - add Test Users (your gmail account)
    - add Allowed Domains: localhost.com (just trust me)
3. Run the agent.py file or test_tools.py file 
4. Will prompt you for OAuth (opening a browser) - Authorize the app
5. Will create or update the `token.json` file in the project directory