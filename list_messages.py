#!/usr/local/bin/python
from __future__ import print_function
import httplib2
import os

import base64
from apiclient import discovery
from apiclient import errors
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import hashlib
import os

import argparse
parser = argparse.ArgumentParser(parents=[tools.argparser])
parser.add_argument("--query", type=str, help='Gmail query to limit emails')
parser.add_argument("--before", type=str, help='Limit emails by date')
parser.add_argument("--after", type=str, help='Limit emails by date')
parser.add_argument("--label", type=str, help='Limit emails by date')
flags = parser.parse_args()

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')
    
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials



"""Get a list of Messages from the user's mailbox.
"""

def ListMessagesMatchingQuery(service, user_id, query=''):
  """List all Messages of the user's mailbox matching the query.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    query: String used to filter messages returned.
    Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

  Returns:
    List of Messages that match the criteria of the query. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate ID to get the details of a Message.
  """
  try:
    response = service.users().messages().list(userId=user_id,
                                               q=query).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])
    
    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user_id, q=query,
                                         pageToken=page_token).execute()
      messages.extend(response['messages'])
    
    return messages
  except errors.HttpError as error:
    print('An error occurred: %s' % error)


def GetMessage(service, user_id, msg_id, lbl):
  """
  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
             can be used to indicate the authenticated user.
    msg_id: ID of Message containing attachment.
  """
  try:
    msg = service.users().messages().get(userId=user_id, id=msg_id, format='metadata').execute()
    date   = ','.join([hdr['value'] for hdr in msg['payload']['headers'] if hdr['name']=='Date'])
    sender = ','.join([hdr['value'] for hdr in msg['payload']['headers'] if hdr['name']=='From'])
    sbj    = ' '.join([hdr['value'] for hdr in msg['payload']['headers'] if hdr['name']=='Subject'])
    labels = ','.join([lbl[x] for x in msg['labelIds']])
    snippet= msg['snippet']
    print(("%s\t%s\t%s\t%s\t%s" % (date, sender, sbj, labels, snippet)).encode('UTF-8'))
  except errors.HttpError as error:
    print('An error occurred: %s' % error)

def main(query):
    """
    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    labels = service.users().labels().list(userId='me').execute()
    lbl = dict([(y['id'],y['name']) for y in labels['labels']])
    results = ListMessagesMatchingQuery(service, 'me', query)

    for msg in results:
      GetMessage(service, 'me', msg['id'], lbl)

if __name__ == '__main__':
    qry = list()
    if(flags.before):
        qry.append('before:' + flags.before)
    if(flags.after):
        qry.append('after:' + flags.after)
    if(flags.label):
        qry.append('label:' + flags.label)
    if(flags.query):
        qry.append(flags.query)
    print(' '.join(qry))
    main(' '.join(qry))
