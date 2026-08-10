@echo off
echo Starting GurmadAI Startup Sequence...

echo Starting GurmadAI Backend...
start "GurmadAI Backend" cmd /k "cd backend && if not exist venv python -m venv venv && call venv\Scripts\activate.bat && pip install -r requirements.txt && python main.py"

echo Waiting 3 seconds for backend to initialize...
timeout /t 3 /nobreak

echo Starting GurmadAI Frontend...
start "GurmadAI Frontend" cmd /k "python -m http.server 8080"

echo Startup sequence complete!
echo You can test the backend connection by running: python test_connection.py
