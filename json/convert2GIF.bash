#!/usr/bin/bash

for file in *.json
do
	echo "Generating GIF for $file";
	python json2gif.py "$file";
done
