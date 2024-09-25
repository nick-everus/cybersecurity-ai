#!/bin/bash

# Directory to monitor
MONITOR_DIR="/etc"

# Create a baseline file hash list using sha256sum
find $MONITOR_DIR -type f -exec sha256sum {} \; > baseline.txt

# Monitor for changes
while true; do
    find $MONITOR_DIR -type f -exec sha256sum {} \; > current.txt
    diff baseline.txt current.txt > file_changes.txt

    if [ -s file_changes.txt ]; then
        echo "Alert! File changes detected in $MONITOR_DIR"
        cat file_changes.txt
    fi

    # Wait for 10 minutes before checking again
    sleep 600
done