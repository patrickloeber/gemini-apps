# Explore Gemini - Building Multimodal Gen AI Apps

3 example apps:

- Multimodal understanding
- Supermarket invoice and food assistant
- Personal assistant for emails and calendar (AI agent)

## 1. Gemini Multimodal

File: [gemini-multimodal.ipynb](gemini-multimodal.ipynb)

Walkthrough on how to analzye images, audio, video, and PDFs with Gemini.

## 2. Food Assistant

Directory: [/food-assistant](food-assistant)

Upload a PDF with your supermarket invoice and Gemini will:
            
1. Extract invoice items
2. Flag potentially unhealthy items
3. Suggest a few recipes  

#### Getting started

Enter your API key in `.env`. Then install requirements and run the app:

```
pip install streamlit python-dotenv google-genai
```

```
streamlit run main.py
```

## 3. Personal email and calendar assistant

An agent that can access Gmail and Gcal events, and act as an assistant
to review the user's calendar and emails, extracting the most important details to highlight for weekly overviews.


### OAuth setup for Google Calendar and Gmail

https://developers.google.com/workspace/calendar/api/quickstart/python

1. Enable Google Calendar API and Gmail API in the Google Cloud Console
2. Configure OAuth for Google Calendar and Google Drive
    - add client: Desktop type, download the JSON file and rename it `credentials.json` and put it in the project directory
    - add Scope for Calendar and Gmail
    - add Test Users (your gmail account)
    - add Allowed Domains: localhost.com (just trust me)
3. Run the agent.py file or test_tools.py file 
4. Will prompt you for OAuth (opening a browser) - Authorize the app
5. Will create or update the `token.json` file in the project directory

### Run the app

Install and run the app:

```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip install google-adk
```

```
adk web
```

Open the app, select the `google_workspace_agent`, and start chatting with the agent, e.g.
- "Get my meetings for next week"
- "Do I have any meeting conflicts?"
- "Get my latest 5 emails and summarize them"
