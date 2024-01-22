#!/bin/bash

# Define the app's directory
APP_DIR="/home/sam/poetroid"

# Change to the app's directory
cd $APP_DIR

# Sync with git
git pull

# Check for venv directory, create it if it doesn't exist and install requirements
if [ ! -d "$APP_DIR/venv" ]; then
    python3 -m venv "$APP_DIR/venv"
    "$APP_DIR/venv/bin/pip" install -r "$APP_DIR/requirements.txt"
fi

# Start application
"$APP_DIR/venv/bin/python3" "$APP_DIR/main_tk.py"
