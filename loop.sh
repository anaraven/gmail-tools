#!/bin/bash

while 1; do
	python3 ~/gmail-tools/attach_downloader.py --log log.txt $* | tee new.txt
	cat new.txt >> log.txt
	sleep 10
done
