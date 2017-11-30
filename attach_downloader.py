#!/usr/local/bin/python3
#
# Author: Andres Aravena
#
# My contributions: CC-BY
# Derived from Google API reference
# Original licence: Code samples are licensed under the Apache 2.0 License.
#

from oauth2client import tools
import hashlib, os
from gmail_tools import get_service, ListMessagesMatchingQuery, GetMsgAttach

import argparse
parser = argparse.ArgumentParser(parents=[tools.argparser])
parser.add_argument("--query", type=str, help='Gmail query to limit emails')
parser.add_argument("--before", type=str, help='Limit emails by date')
parser.add_argument("--after", type=str, help='Limit emails by date')
parser.add_argument("--label", type=str, help='Limit emails by label')
parser.add_argument("--filename", type=str, help='Limit emails by attach filename or extension')
parser.add_argument("--outdir", type=str, help='Output directory (must exits)',
        default="")
parser.add_argument("--log", type=str, help='Log filename')
flags = parser.parse_args()


def main(flags):
    m_id = {}
    old_qry = None
    if(flags.log):
      with open(flags.log,"r") as logfile:
        for l in logfile:
            if l[0]=="#":
              old_qry=l[2:].strip()
              continue
            ll = l.strip().split("\t")
            m_id[ll[5]]=1

    qry = ['has:attachment']
    if(flags.before):
        qry.append('before:' + flags.before)
    if(flags.after):
        qry.append('after:' + flags.after)
    if(flags.label):
        qry.append('label:' + flags.label)
    if(flags.filename):
        qry.append('filename:' + flags.filename)
    if(flags.query):
        qry.append(flags.query)
    query =  ' '.join(qry)
    if query != old_qry:
      print("# " + query)

    service = get_service(flags)
    results = ListMessagesMatchingQuery(service, 'me', query)

    for msg in results:
        if not msg['id'] in m_id:
          (sender, date, fname, file_data) = GetMsgAttach(service, 'me', msg['id'])
          for i in range(len(fname)):
            m = hashlib.md5()
            m.update(file_data[i])
            filename, file_ext= os.path.splitext(fname[i])
            path = ''.join([flags.outdir, m.hexdigest(), file_ext])
            with open(path, 'wb') as f:
              f.write(file_data[i])
            print("%s\t%s\t%s\t%s\t%s%s\t%s" % (m.hexdigest(), file_ext,
              date[0], sender[0], filename, file_ext, msg['id']))


if __name__ == '__main__':
    main(flags)
