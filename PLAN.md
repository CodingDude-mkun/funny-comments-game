# Project Development Plan: Funny Comments Game

This document outlines the detailed development plan for the 'Funny Comments Game' project, including key features, tasks, and a tracking checklist.

## 1. Backend Development (FastAPI & PostgreSQL)

- [x] **Database Setup & Migrations**
    - [x] Finalize `database.py` with actual PostgreSQL connection string.
    - [x] Implement database migrations (e.g., using Alembic) for schema evolution.

- [x] **User Management**
    - [x] Implement user registration API endpoint.
    - [x] Implement user login API endpoint (e.g., using JWT for authentication).
    - [x] Implement user session management.

- [x] **Lobby Management**
    - [x] Create Lobby API endpoint.
    - [x] Join Lobby API endpoint.
    - [x] Leave Lobby API endpoint.
    - [x] Get List of Lobbies API endpoint.
    - [x] Get Lobby Details API endpoint.
    - [x] Implement WebSocket events for lobby updates (user joined/left).

- [x] **Game Logic & Core Features**
    - [x] **Round Management:**
        - [x] Implement API to start a new round.
        - [x] Implement API to transition between phases (product submission, commenting, voting).
        - [x] Implement server-side timers for each phase.
    - [x] **Product Submission:**
        - [x] Implement API for product link/image upload.
        - [x] Implement WebSocket event for new product submission.
    - [x] **Commenting:**
        - [x] Implement API for submitting comments.
        - [x] Implement WebSocket event for new comments.
    - [x] **Voting:**
        - [x] Implement API for submitting votes.
        - [x] Implement WebSocket event for vote updates.
    - [x] **Score Calculation:**
        - [x] Implement logic to determine round winner based on votes.
        - [x] Update player scores.
    - [x] **Game State Synchronization:**
        - [x] Implement WebSocket events to broadcast current game state (timers, active player, comments, votes) to all lobby members.

- [ ] **Error Handling & Validation**
    - [ ] Implement robust error handling for API endpoints.
    - [ ] Add input validation for all incoming data.

- [ ] **Testing**
    - [ ] Write unit tests for core game logic and API endpoints.
    - [ ] Write integration tests for database interactions and WebSocket communication.

## 2. Frontend Development (React)

- [ ] **Project Setup**
    - [ ] Install necessary React libraries (e.g., `react-router-dom`, `socket.io-client`, Bootstrap).

- [ ] **User Interface (UI) Components**
    - [ ] **Authentication:**
        - [ ] Login/Registration forms.
        - [ ] User dashboard/profile.
    - [ ] **Lobby System:**
        - [ ] Lobby list display.
        - [ ] Create Lobby form.
        - [ ] Join Lobby interface.
        - [ ] Lobby room display (list of members).
    - [ ] **Game Board:**
        - [ ] Product display area (for link/image).
        - [ ] Comment input form.
        - [ ] Comments display area.
        - [ ] Voting interface.
        - [ ] Timer display.
        - [ ] Scoreboard/Leaderboard.
        - [ ] Round winner announcement.

- [ ] **State Management**
    - [ ] Manage global game state (current lobby, round, phase, comments, votes) using React Context or Redux (if complexity warrants).

- [ ] **API Integration**
    - [ ] Connect React components to FastAPI backend API endpoints.

- [ ] **Real-time Communication**
    - [ ] Integrate `socket.io-client` to listen for and emit WebSocket events.
    - [ ] Update UI in real-time based on WebSocket messages.

- [ ] **Styling & Responsiveness**
    - [ ] Apply Bootstrap for consistent styling.
    - [ ] Ensure responsive design for various screen sizes.

## 3. Deployment Configuration

- [ ] **Backend (Render)**
    - [x] Configure Render service for the FastAPI application.
    - [x] Set up environment variables on Render (e.g., `DATABASE_URL`, any secrets).
    - [x] Configure PostgreSQL database on Render and obtain connection string.
    - [x] Ensure `Procfile` is correctly configured for Render.
    - [x] Document backend startup instructions.
    - [x] Create robust local backend startup script.

- [ ] **Frontend (Vercel)**
    - [ ] Connect Vercel project to the GitHub repository.
    - [ ] Configure environment variables on Vercel (e.g., `REACT_APP_BACKEND_URL` pointing to Render backend).
    - [ ] Ensure build commands are correct for React.

## 4. Testing & Refinement

- [ ] **End-to-End Testing**
    - [ ] Test full game flow from user registration to multiple rounds.
    - [ ] Test real-time updates across multiple clients.

- [ ] **Performance Optimization**
    - [ ] Identify and address any performance bottlenecks.

- [ ] **UI/UX Improvements**
    - [ ] Gather feedback and refine user experience.
    - [ ] Add animations or visual cues for better engagement.

## 5. Documentation & Cleanup

- [ ] Update `README.md` with instructions for running the project locally and deployment.
- [ ] Clean up unused code and dependencies.
