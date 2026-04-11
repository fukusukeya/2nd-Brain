#!/bin/bash

# ==============================================================================
# Voice Inbox Sync Script (iCloud -> 2nd-Brain)
# ==============================================================================
# Description: 
#   Automatically moves audio files from the iCloud "Voice Inbox"
#   to the local 2nd-Brain "02_音声" folder.
#   Triggered seamlessly by macOS launchd (WatchPaths).
# ==============================================================================

# Directory definitions
INBOX_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Voice Inbox"
DEST_DIR="/Users/kasuyatooru/Product/2nd-Brain/02_音声"

# 1. Ensure both directories exist
mkdir -p "$INBOX_DIR"
mkdir -p "$DEST_DIR"

# 2. Find and move supported audio files safely
# Using a small pause or checks ensures files aren't moved while still uploading from iPhone, 
# although Shortcuts usually makes the file fully available atomically via iCloud.
find "$INBOX_DIR" -maxdepth 1 -type f \( -iname "*.wav" -o -iname "*.m4a" -o -iname "*.mp3" -o -iname "*.mp4" \) -print0 | while IFS= read -r -d '' file; do
    # Move the file
    mv "$file" "$DEST_DIR/"
done

exit 0
