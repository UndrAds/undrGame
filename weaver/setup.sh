#!/bin/bash

# Setup script for weaver subproject

echo "Setting up weaver subproject..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file from template if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp env.template .env
    echo "Please edit .env file and add your OpenAI API key"
else
    echo ".env file already exists"
fi

echo ""
echo "Setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source .venv/bin/activate"
echo ""
echo "To run the generator, execute:"
echo "  python main.py"
echo ""
echo "Don't forget to add your OpenAI API key to the .env file!"
