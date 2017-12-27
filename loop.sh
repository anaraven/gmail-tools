#!/bin/bash
BIN=~/gmail-tools
while true; do
	python3 $BIN/attach_downloader.py --log log.txt $* | tee new.txt
	if test -s new.txt
	then
	  awk -f $BIN/messg-csp1.awk new.txt |sh
	  cat new.txt >> log.txt
        fi
	sleep 30
done
