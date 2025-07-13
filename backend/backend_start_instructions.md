# Backend Server Startup Instructions

This document provides instructions on how to start the FastAPI backend server for the Product Review Game, both locally and in a deployment environment.

## 1. Local Development Setup

To run the backend server on your local machine, follow these steps:

### Prerequisites:
*   **Python 3.9+**: Ensure Python is installed and added to your system's PATH. You can download it from [python.org](https://www.python.org/downloads/).
*   **pip**: Python's package installer (usually comes with Python).
*   **Virtual Environment (Recommended)**: It's highly recommended to use a virtual environment to manage dependencies.

### Steps:

1.  **Navigate to the Backend Directory:**
    Open your terminal or command prompt and change your current directory to the backend folder of the project:
    ```bash
    cd F:/Codes/FunnnyComments/product-game/backend/
    ```

2.  **Create and Activate a Virtual Environment (Optional but Recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    Install all required Python packages using `pip`:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize Database Tables:**
    This command creates the necessary database tables if they don't already exist.
    ```bash
    python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"
    ```

5.  **Start the FastAPI Application:**
    You can start the server using `uvicorn`. The server will be accessible at `http://localhost:8000`.
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```
    To run it in the background (Unix-like systems):
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 &
    ```

### Using `start.sh` (for Unix-like environments like Git Bash, WSL, Linux, macOS):

The `start.sh` script automates the installation of dependencies, database table creation, and server startup.

1.  **Make the script executable (if necessary):**
    ```bash
    chmod +x start.sh
    ```
2.  **Run the script:**
    ```bash
    ./start.sh
    ```
    To run it in the background:
    ```bash
    ./start.sh &
    ```

## 2. Deployment Setup (Render)

As outlined in the `PLAN.md`, the backend is designed for deployment on Render. Render uses a `Procfile` to define how your application should be started.

### Key Files for Deployment:

*   **`requirements.txt`**: Specifies all Python dependencies that Render will automatically install.
*   **`Procfile`**: This file tells Render how to run your web service. It typically contains a command like:
    ```
    web: bash start.sh
    ```
    This instructs Render to execute the `start.sh` script when starting the web service.
*   **`start.sh`**: This script (as detailed above) handles installing dependencies, setting up the database, and launching the `uvicorn` server.
*   **Environment Variables**: On Render, you will configure environment variables, most importantly `DATABASE_URL`, which will be used by `database.py` to connect to your PostgreSQL database.

### Deployment Process on Render:

1.  **Connect to Git Repository**: Link your Render service to your Git repository (e.g., GitHub, GitLab).
2.  **Configure Service**: Set the build command (e.g., `pip install -r requirements.txt`) and start command (e.g., `bash start.sh` or `uvicorn main:app --host 0.0.0.0 --port $PORT`). Render automatically detects the `Procfile`.
3.  **Database Setup**: Create a PostgreSQL database service on Render and link it to your backend service, providing the `DATABASE_URL` environment variable.

Render will automatically use these configurations to build and deploy your FastAPI application.
