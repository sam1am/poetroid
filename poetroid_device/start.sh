#!/bin/bash

# Get the current directory
APP_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PARENT_DIR="$(dirname "$APP_DIR")"

# Sync with git
git pull

# Check for venv directory, create it if it doesn't exist and install requirements
if [ ! -d "$PARENT_DIR/venv" ]; then
    python3 -m venv "$PARENT_DIR/venv"
    "$PARENT_DIR/venv/bin/pip" install -r "$APP_DIR/requirements.txt"
fi

# Start application
"$PARENT_DIR/venv/bin/python3" "$APP_DIR/poetroid_app.py"