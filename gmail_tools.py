#
# Author: Andres Aravena
#
# My contributions: CC-BY
# Derived from Google API reference
# Original licence: Code samples are licensed under the Apache 2.0 License.
#

from __future__ import print_function

from apiclient import discovery, errors
from oauth2client import client, tools
from oauth2client.file import Storage
import hashlib
import base64
import os
import httplib2

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Download attached files'

def get_credentials(flags, cred_filename='gmail-python-quickstart.json'):
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
    credential_path = os.path.join(credential_dir, cred_filename)
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

def get_service(flags):
    credentials = get_credentials(flags)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    return service

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

    return reversed(messages)
  except errors.HttpError as error:
    print('An error occurred: %s' % error)

# Retrieve an attachment from a Message.
def GetAttachments(service, user_id, msg_id, flags, format="full", metadataHeaders=[]):
  """Get and store attachment from Message with given id.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: ID of Message containing attachment.
    store_dir: The directory used to store attachments.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id,
        format=format, metadataHeaders=metadataHeaders).execute()
    sender = [hdr['value'] for hdr in message['payload']['headers'] if hdr['name']=='From']
    date   = [hdr['value'] for hdr in message['payload']['headers'] if hdr['name']=='Date']
    for part in message['payload']['parts']:
      if part['filename']:
        att_id = part['body']['attachmentId']
        attach = service.users().messages().attachments().get(userId=user_id,
            messageId=msg_id, id=att_id).execute()
        file_data = base64.urlsafe_b64decode(attach['data'].encode('UTF-8'))
        m = hashlib.md5()
        m.update(file_data)
        filename, file_extension = os.path.splitext(part['filename'])
        path = ''.join([flags.outdir, m.hexdigest(), file_extension])
        print( "%s\t%s\t%s\t%s\t%s%s" % (m.hexdigest(), file_extension,
            ";".join(date), sender[0],
            filename, file_extension, msg_id))
        with open(path, 'wb') as f:
            f.write(file_data)
  except errors.HttpError as error:
    print('An error occurred: %s' % error)

def GetMsgAttach(service, user_id, msg_id):
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()
    sender = [hdr['value'] for hdr in message['payload']['headers'] if hdr['name']=='From']
    date   = [hdr['value'] for hdr in message['payload']['headers'] if hdr['name']=='Date']
    sbj    = [hdr['value'] for hdr in message['payload']['headers'] if hdr['name']=='Subject']
    attch = []
    fname = []
    if 'parts' in message['payload']:
      for part in message['payload']['parts']:
        if part['filename']:
          att_id = part['body']['attachmentId']
          attach = service.users().messages().attachments().get(userId=user_id,
              messageId=msg_id, id=att_id).execute()
          attch.append(base64.urlsafe_b64decode(attach['data'].encode('ascii')))
          fname.append(part['filename'])
    return (sender, date, fname, attch, sbj[0])
  except errors.HttpError as error:
    print('An error occurred: %s' % error)

def GetMsgText(service, user_id, msg_id):
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()
    sender = [hdr['value'] for hdr in message['payload']['headers'] if hdr['name']=='From']
    date   = [hdr['value'] for hdr in message['payload']['headers'] if hdr['name']=='Date']
    attch = []
    for part in message['payload']['parts']:
      if part['mimeType']=="text/plain" and part['filename']=="":
        att_id = part['body']
        attch.append(base64.urlsafe_b64decode(att_id['data'].encode('ascii')))
    return (sender, date, fname, attch)
  except errors.HttpError as error:
    print('An error occurred: %s' % error)

def GetMessage(service, user_id, msg_id):
  """
  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
             can be used to indicate the authenticated user.
    msg_id: ID of Message containing attachment.
  """
  try:
    msg = service.users().messages().get(userId=user_id, id=msg_id, format='metadata').execute()
    date   = [hdr['value'] for hdr in msg['payload']['headers'] if hdr['name']=='Date']
    sender = [hdr['value'] for hdr in msg['payload']['headers'] if hdr['name']=='From']
    sbj    = [hdr['value'] for hdr in msg['payload']['headers'] if hdr['name']=='Subject']
    labels = msg['labelIds']
    snippet= msg['snippet']
    return (date, sender, sbj, labels, snippet)
  except errors.HttpError as error:
    print('An error occurred: %s' % error)
