#!/bin/bash

# Script to start the poetroid server in the background

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVER_DIR="$SCRIPT_DIR/server"
VENV_DIR="$SERVER_DIR/venv"
PID_FILE="$SERVER_DIR/server.pid"
LOG_FILE="$SERVER_DIR/logs/server.log"

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Error: Virtual environment not found at $VENV_DIR"
    echo "Please run server/install.sh first"
    exit 1
fi

# Check if server is already running
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "Server is already running with PID $OLD_PID"
        echo "To stop it, run: kill $OLD_PID"
        exit 1
    else
        echo "Removing stale PID file"
        rm "$PID_FILE"
    fi
fi

# Ensure log directory exists
mkdir -p "$SERVER_DIR/logs"

# Start the server in the background
echo "Starting poetroid server..."
cd "$SERVER_DIR"
source "$VENV_DIR/bin/activate"

nohup python serve.py > "$LOG_FILE" 2>&1 &
SERVER_PID=$!

# Save the PID
echo "$SERVER_PID" > "$PID_FILE"

echo "Server started successfully!"
echo "PID: $SERVER_PID"
echo "PID file: $PID_FILE"
echo "Log file: $LOG_FILE"
echo "Server URL: http://localhost:3090"
echo ""
echo "To stop the server, run: kill $SERVER_PID"
echo "Or use: kill \$(cat $PID_FILE)"
echo ""
echo "To view logs, run: tail -f $LOG_FILE"
