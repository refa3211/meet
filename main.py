from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import datetime
import os.path
import pickle

def create_google_meet():
    """
    Create a Google Meet meeting and return the meeting link
    Returns:
        str: Google Meet link
    """
    # If you're modifying these scopes, delete token.pickle
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None

    # Load saved credentials if they exist
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials available, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for future use
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Create Google Calendar API service
    service = build('calendar', 'v3', credentials=creds)

    # Define event details
    start_time = datetime.datetime.utcnow()
    end_time = start_time + datetime.timedelta(hours=1)

    event = {
        'summary': 'Google Meet Meeting',
        'start': {
            'dateTime': start_time.isoformat() + 'Z',
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time.isoformat() + 'Z',
            'timeZone': 'UTC',
        },
        'conferenceData': {
            'createRequest': {
                'requestId': f"meet-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}",
                'conferenceSolutionKey': {'type': 'hangoutsMeet'}
            }
        }
    }

    # Create the event with Google Meet
    event = service.events().insert(
        calendarId='primary',
        body=event,
        conferenceDataVersion=1
    ).execute()

    # Get the Google Meet link
    meet_link = event['conferenceData']['entryPoints'][0]['uri']
    
    return meet_link

def main():
    try:
        meeting_link = create_google_meet()
        print(f"Meeting created successfully!")
        print(f"Meeting link: {meeting_link}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    main()