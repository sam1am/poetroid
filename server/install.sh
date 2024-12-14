#!/bin/bash

# Print commands and their arguments as they are executed
set -x

# Exit on any error
set -e

echo "Starting Poetroid Server installation..."

# Check if running as root and exit if true
if [ "$(id -u)" = "0" ]; then
   echo "This script must not be run as root" 
   exit 1
fi

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    curl https://ollama.ai/install.sh | sh
    
    # Wait for Ollama service to start
    echo "Waiting for Ollama service to start..."
    sleep 5
else
    echo "Ollama is already installed"
fi

# Start Ollama if it's not running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama service..."
    ollama serve &
    sleep 5  # Wait for service to start
fi

# Pull the model
echo "Pulling llama3.2-vision model..."
ollama pull llama3.2-vision

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is required but not installed. Please install pip3 first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$SCRIPT_DIR/venv"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$SCRIPT_DIR/venv/bin/activate"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing Python requirements..."
pip install -r "$SCRIPT_DIR/requirements.txt"

echo "Installation complete!"
echo "To start the server, run:"
echo "source venv/bin/activate"
echo "python server.py"

# Print Ollama status
echo "Checking Ollama status..."
ollama list

# Check if model was downloaded successfully
if ollama list | grep -q "llama3.2-vision"; then
    echo "llama3.2-vision model is installed successfully"
else
    echo "Warning: llama3.2-vision model may not have installed correctly"
fi

# Print system information
echo "System Information:"
echo "Python version: $(python3 --version)"
echo "Pip version: $(pip --version)"
echo "Virtual environment location: $SCRIPT_DIR/venv"

# Create a start script
cat > "$SCRIPT_DIR/start.sh" << 'EOF'
#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Start Ollama if not running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama service..."
    ollama serve &
    sleep 5
fi

# Activate virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

# Start the server
python "$SCRIPT_DIR/server.py"
EOF

# Make start script executable
chmod +x "$SCRIPT_DIR/start.sh"

echo "A start script has been created. To start the server, run: ./start.sh"