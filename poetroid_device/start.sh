#!/bin/bash

# Get th current directory
APP_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Sync with git
git pull

# Check for venv directory, create it if it doesn't exist and install requirements
if [ ! -d "../$APP_DIR/venv" ]; then
    python3 -m venv "../$APP_DIR/venv"
    "../$APP_DIR/venv/bin/pip" install -r "../$APP_DIR/requirements.txt"
fi

# Start application
"../$APP_DIR/venv/bin/python3" "../$APP_DIR/poetroid_app.py"
