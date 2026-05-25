# DiabetesOredictionSystem

This folder contains a simple backend/frontend scaffold for the Diabetes Prediction System API.

## Backend

- `backend/app.py`: FastAPI backend exposing prediction and deployment endpoints.
- `backend/requirements.txt`: Python dependencies to install.

Run the backend:

```powershell
cd DiabetesOredictionSystem\backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload
```

## Frontend

- `frontend/index.html`: Static UI to send prediction requests.
- `frontend/login.html`: Local login page for the application.
- `frontend/script.js`: Client-side JavaScript calling the backend.
- `frontend/style.css`: Basic styling.

Open `DiabetesOredictionSystem/frontend/index.html` in a browser while the backend is running at `http://127.0.0.1:8000`.

Then visit the login page at:

```text
http://127.0.0.1:8000/login
```

Default credentials:

- Username: `admin`
- Password: `password123`
