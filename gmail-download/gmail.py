from __future__ import print_function
import pickle
import os.path
import base64
import quopri
import re
import sys
import os
# import pprint
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Add default query for Gmail here
# This can be overriden from commandline as additional arguments after calling script
# e.g. gmail.py from:someone@test.com is:unread
# e.g. gmail.py from:someone@test.com after:2020/06/29 before:2020/08/01
QUERY = 'from:someone@test.com'

# Download details
DOWNLOAD_FOLDER = 'downloads'
DEFAULT_FILENAME = 'output.html'

def get_message_list(service, overrideQ):

    """ Get a list messages from authenticated user's account
    based on QUERY or unvalidated argument from command line

    Args:
    service: Authorized Gmail API service instance.
    overrideQ: String value for query parameter to API, can be None
    
    Returns:
    An array of messages or None
    """
    try:
        query = QUERY
        if overrideQ:
            print(overrideQ)
            query = overrideQ

        # Call the Gmail API    
        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])

        return messages

    except errors.HttpError as error:
        print('An error occurred: %s' % error)
    
    return None


def main():
    """Uses the Gmail API to connect to your account through OAuth 
    and download the html version of emails based on query parameters 
    provided through the command line
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    query = None
    if len(sys.argv) > 3:
        query = ' '.join(sys.argv[3:])

    print(query)
    messages = get_message_list(service, query)

    if not messages:
        print('No messages found.')
    else:
        
        for message_id in messages:
            message = service.users().messages().get(userId='me', id=message_id['id'], format='full').execute()
            if message:
                # pp.pprint(message)
                parts = message['payload']['parts']
                headers = message['payload']['headers']
                subject = None
                for header in headers:
                    if header['name'] == 'Subject':
                        subject = header['value']

                for part in parts:
                    if part['mimeType'] == 'text/html':
                        body = part['body']['data']
                        body = quopri.decodestring(body)
                        body = base64.urlsafe_b64decode(body + b'===') # adding b'===' to fix incorrect padding issues

                        # Save email content to local file
                        outfile = DEFAULT_FILENAME
                        if subject:
                            outfile = re.sub(r'[^\.\d\s\w]', '', subject) + "_" + message_id['id'] + ".html"
                        
                        output_folder = os.path.join(DOWNLOAD_FOLDER)

                        # Check if output folder exists
                        if not os.path.exists(output_folder):
                            os.makedirs(output_folder) 
                            
                        open(os.path.join(output_folder, outfile), 'wb').write(body)

if __name__ == '__main__':
    main()
