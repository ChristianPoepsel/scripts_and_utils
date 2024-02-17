#!/bin/bash

FLAC_DIR="/Volumes/LR RAW DATA/Music FLAC/AC DC"
MP4_DIR="/Volumes/LR RAW DATA/Music MP4"
LOG_FILE="mp4_converter_log.log"
BITRATE="320k"
SAMPLE_RATE="44100"
XLD_PATH="/Applications/XLD.app/Contents/MacOS/XLD"

find "$FLAC_DIR" -type f -name "*.flac" | while read -r flac_file; do
    relative_path="${flac_file#$FLAC_DIR/}"
    mp4_file="$MP4_DIR/$relative_path"
    mp4_file="${mp4_file%.flac}.mp4"

    if [ ! -f "$mp4_file" ]; then
        echo "Converting: $flac_file"
        mkdir -p "$(dirname "$mp4_file")"

        # Error handling
        # if "$XLD_PATH" -f mp4 -o "$(dirname "$mp4_file")" -t aac -b "$BITRATE" -s "$SAMPLE_RATE" "$flac_file"; then
        if ffmpeg -nostdin -i "$flac_file" -c:a aac -b:a "$BITRATE" -vn -f mp4 "$mp4_file"; then
            echo "$(date): $flac_file converted" >> "$LOG_FILE"
        else
            echo "$(date): ERROR converting $flac_file" >> "$LOG_FILE"
        fi
    else
        echo "Already converted: $flac_file"
    fi
done
