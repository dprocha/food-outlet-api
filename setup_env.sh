#!/bin/bash

# Check if a virtual environment directory exists
ENV_DIR=".venv"
REQUIREMENTS_FILE="requirements.txt"

# Create virtual environment if it doesn't exist
if [ ! -d "$ENV_DIR" ]; then
  echo "Creating virtual environment..."
  python3 -m venv $ENV_DIR
  echo "Virtual environment created at ./$ENV_DIR"
else
  echo "Virtual environment already exists."
fi

# Activate virtual environment
source "$ENV_DIR/bin/activate"
echo "Virtual environment activated."

# Install dependencies if requirements.txt exists
if [ -f "$REQUIREMENTS_FILE" ]; then
  echo "Installing dependencies from $REQUIREMENTS_FILE..."
  pip3 install --no-cache-dir -r $REQUIREMENTS_FILE
  echo "Dependencies installed."
else
  echo "No $REQUIREMENTS_FILE found. You can create one by running 'pip freeze > $REQUIREMENTS_FILE'."
fi

# Final message
echo "Setup complete. To deactivate the environment, type 'deactivate'."
