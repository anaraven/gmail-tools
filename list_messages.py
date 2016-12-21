#!/usr/local/bin/python
from __future__ import print_function
from apiclient import discovery
from oauth2client import tools
from gmail_tools import get_credentials, ListMessagesMatchingQuery, GetMessage
import argparse
import httplib2

parser = argparse.ArgumentParser(parents=[tools.argparser])
parser.add_argument("--query", type=str, help='Gmail query to limit emails')
parser.add_argument("--before", type=str, help='Limit emails by date')
parser.add_argument("--after", type=str, help='Limit emails by date')
parser.add_argument("--label", type=str, help='Limit emails by date')
flags = parser.parse_args()


def main(query):
    """
    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials(flags)
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
    print("# " + ' '.join(qry))
    main(' '.join(qry))
