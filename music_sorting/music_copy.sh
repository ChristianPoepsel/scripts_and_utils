#!/bin/bash

SOURCE_DIR="/Volumes/VideoWork1/Musikbibliothek JP FLAC backup"
DEST_DIR="/Volumes/LR RAW DATA/Music FLAC"
LOG_FILE="music_copy.log"

find "$SOURCE_DIR" -type f | while read -r source_file; do
    relative_path="${source_file#$SOURCE_DIR/}"
    dest_file="$DEST_DIR/$relative_path"

    if [ ! -f "$dest_file" ]; then
        echo "Copying: $source_file"
        mkdir -p "$(dirname "$dest_file")"

        # Error handling
        if cp "$source_file" "$dest_file"; then
            echo "$(date): $source_file copied" >> "$LOG_FILE"
        else
            echo "$(date): ERROR copying $source_file" >> "$LOG_FILE"
        fi
    else
        echo "Already exists: $source_file"
    fi
done
