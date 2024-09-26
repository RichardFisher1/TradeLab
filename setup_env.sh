#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting setup..."

# Step 1: Create a virtual environment (if it doesn't exist)
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv || { echo "Failed to create virtual environment"; exit 1; }
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Step 2: Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }

# Step 3: Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip -v || { echo "Failed to upgrade pip"; exit 1; }

# Step 4: Install dependencies from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt -v || { echo "Failed to install dependencies from requirements.txt"; exit 1; }
else
    echo "No requirements.txt found. Skipping dependency installation."
fi

# Step 5: Install the entire project as an editable package
echo "Installing the project as an editable package..."
pip install -e . -v || { echo "Failed to install project as an editable package"; exit 1; }

echo "Setup complete. Virtual environment is ready."
