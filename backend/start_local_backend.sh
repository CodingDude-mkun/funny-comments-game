#!/bin/bash

echo "Starting local backend server..."

# Check for Python and pip
if ! command -v python &> /dev/null
then
    echo "Python is not installed or not in PATH. Please install Python 3.9+ and add it to your system PATH."
    exit 1
fi

echo "Python found: $(python --version)"

if ! command -v pip &> /dev/null
then
    echo "pip is not installed. Attempting to install pip..."
    python -m ensurepip --default-pip
    if [ $? -ne 0 ]; then
        echo "Failed to install pip. Please install it manually."
        exit 1
    fi
fi

# Check for uvicorn and install if not found
if ! command -v uvicorn &> /dev/null
then
    echo "uvicorn is not installed. Attempting to install uvicorn..."
    pip install uvicorn
    if [ $? -ne 0 ]; then
        echo "Failed to install uvicorn. Please install it manually (pip install uvicorn)."
        exit 1
    fi
fi

# Install other dependencies from requirements.txt
echo "Installing/updating dependencies from requirements.txt..."
pip install -r requirements.txt

# Create database tables
echo "Creating database tables..."
python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"

# Start the FastAPI application
echo "Starting FastAPI application..."
uvicorn main:app --host 0.0.0.0 --port 8000