@echo off
echo ============================================================
echo   AI Research Agent - Full Stack Startup
echo ============================================================
echo.

echo [1/2] Starting Backend Server...
start "Backend Server" cmd /k ".venv\Scripts\python.exe start.py"
timeout /t 3 /nobreak >nul

echo [2/2] Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && npm start"

echo.
echo ============================================================
echo   Servers Started!
echo ============================================================
echo.
echo   Backend:  http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo   Frontend: http://localhost:3000
echo.
echo   Close terminal windows to stop servers
echo.
pause
