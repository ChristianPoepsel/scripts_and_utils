#!/bin/zsh

YEAR="2024"
SOURCEPATH="/Volumes/Untitled/DCIM/"
TARGETPATH="/Volumes/01_A/MediaFiles/$YEAR/"


source venv/bin/activate
python app.py $SOURCEPATH $TARGETPATH