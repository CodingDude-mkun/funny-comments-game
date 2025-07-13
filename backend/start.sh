#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run database migrations (if any, for now just create tables)
python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"

# Start the FastAPI application
uvicorn main:app --host 0.0.0.0 --port 8000
