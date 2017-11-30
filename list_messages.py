#!/usr/local/bin/python3
#
# Author: Andres Aravena
#
# My contributions: CC-BY
# Derived from Google API reference
# Original licence: Code samples are licensed under the Apache 2.0 License.
#

from oauth2client import tools

from gmail_tools import get_service, ListMessagesMatchingQuery, GetMessage

import argparse
parser = argparse.ArgumentParser(parents=[tools.argparser])
parser.add_argument("--query", type=str, help='Gmail query to limit emails')
parser.add_argument("--before", type=str, help='Limit emails by date')
parser.add_argument("--after", type=str, help='Limit emails by date')
parser.add_argument("--label", type=str, help='Limit emails by label')
parser.add_argument("--format", type=str, help='Output format')
flags = parser.parse_args()

def main(flags):
    qry = list()
    if(flags.before):
        qry.append('before:' + flags.before)
    if(flags.after):
        qry.append('after:' + flags.after)
    if(flags.label):
        qry.append('label:' + flags.label)
    if(flags.query):
        qry.append(flags.query)
    if(flags.format):
      fmt = flags.format
    else:
      fmt="{date}\t{sender}\t{labels}\t{sbj}\t{snippet}"
    query =  ' '.join(qry)
    print("# " + query)

    service = get_service(flags)

    labels = service.users().labels().list(userId='me').execute()
    lbl = dict([(y['id'],y['name']) for y in labels['labels']])
    results = ListMessagesMatchingQuery(service, 'me', query)

    for r in results:
      try:
        msg = service.users().messages().get(userId='me', id=r['id'],
            format='metadata').execute()
        ans={}
        ans['date'] = [hdr['value'] for hdr in msg['payload']['headers'] if hdr['name']=='Date'][0]
        ans['sender'] = [hdr['value'] for hdr in msg['payload']['headers'] if hdr['name']=='From'][0]
        ans['sbj']  = [hdr['value'] for hdr in msg['payload']['headers'] if hdr['name']=='Subject'][0]
        ans['labels'] = ','.join([lbl[x] for x in msg['labelIds']])
        ans['snippet']= msg['snippet']
        print(fmt.format(**ans))
      except errors.HttpError as error:
        print('An error occurred: %s' % error)

if __name__ == '__main__':
    main(flags)
