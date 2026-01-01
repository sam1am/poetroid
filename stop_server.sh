#!/bin/bash

# Script to stop the poetroid server

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVER_DIR="$SCRIPT_DIR/server"
PID_FILE="$SERVER_DIR/server.pid"

# Check if PID file exists
if [ ! -f "$PID_FILE" ]; then
    echo "Error: PID file not found at $PID_FILE"
    echo "Server may not be running or was started manually"
    exit 1
fi

# Read the PID
SERVER_PID=$(cat "$PID_FILE")

# Check if the process is running
if ! ps -p "$SERVER_PID" > /dev/null 2>&1; then
    echo "Server with PID $SERVER_PID is not running"
    rm "$PID_FILE"
    exit 1
fi

# Stop the server
echo "Stopping server with PID $SERVER_PID..."
kill "$SERVER_PID"

# Wait a moment and check if it stopped
sleep 2
if ps -p "$SERVER_PID" > /dev/null 2>&1; then
    echo "Server didn't stop gracefully, forcing..."
    kill -9 "$SERVER_PID"
fi

# Remove PID file
rm "$PID_FILE"
echo "Server stopped successfully!"
