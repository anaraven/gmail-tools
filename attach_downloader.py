#!/usr/local/bin/python
from __future__ import print_function
from apiclient import discovery, errors
from oauth2client import tools
from gmail_tools import get_credentials, ListMessagesMatchingQuery, GetAttachments
import argparse 
import httplib2

parser = argparse.ArgumentParser(parents=[tools.argparser])
parser.add_argument("--query", type=str, help='Gmail query to limit emails')
parser.add_argument("--before", type=str, help='Limit emails by date')
parser.add_argument("--after", type=str, help='Limit emails by date')
parser.add_argument("--label", type=str, help='Limit emails by date')
parser.add_argument("--outdir", type=str, help='Output directory (must exits)',
        default="")
flags = parser.parse_args()


def main(query):
    credentials = get_credentials(flags)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    results = ListMessagesMatchingQuery(service, 'me', query)

    for msg in results:
      GetAttachments(service, 'me', msg['id'], flags.outdir)


if __name__ == '__main__':
    qry = ['has:attachment']
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
