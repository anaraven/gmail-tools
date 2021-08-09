#!/bin/bash
BIN=~/gmail-tools
LBL=$1; shift
if test -z "$LBL"; then
  echo "Usage: $0 LABEL [options]"
  exit 1
fi

echo Label is $LBL

while true; do
	date
	/usr/bin/python3 $BIN/attach_downloader.py --log log.txt --label "$LBL" $* | tee new.txt
	if test -s new.txt
	then
	  awk -vLBL="$LBL" -f $BIN/messg.awk new.txt | sh
	  cat new.txt >> log.txt
	  echo NOW sleeping
	  sleep 3600
	else
	  echo NOW sleeping
	  sleep 7200
        fi
done
