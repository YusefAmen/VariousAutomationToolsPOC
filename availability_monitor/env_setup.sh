#! /bin/bash

# Exit immediately if any command fails
set -e

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 to continue."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install pip-tools if not already installed
pip install pip-tools

# Compile requirements.txt from requirements.in (if exists)
if [ -f "requirements.in" ]; then
    echo "Compiling requirements.txt from requirements.in..."
    pip-compile requirements.in
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Environment setup complete. You're ready to run the monitor script."

