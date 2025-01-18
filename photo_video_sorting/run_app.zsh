#!/bin/zsh

YEAR="2024"
SOURCEPATH="/Volumes/Untitled/DCIM/"
TARGETPATH="/Volumes/mac_ext_1/MediaFiles/$YEAR/"


source venv/bin/activate
python app.py $SOURCEPATH $TARGETPATH
