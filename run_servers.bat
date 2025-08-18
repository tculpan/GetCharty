@echo off
echo Starting GetCharty servers...
echo.

echo Starting Flask server on port 5000...
start "Flask Server" cmd /k "cd server && python app.py"

echo Waiting 3 seconds for Flask server to start...
timeout /t 3 /nobreak > nul

echo Starting HTTP server on port 8000...
start "HTTP Server" cmd /k "cd client && python -m http.server 8000"

echo.
echo Both servers are starting...
echo Flask server: http://localhost:5000
echo HTTP server: http://localhost:8000
echo.
echo Press any key to close this window...
pause > nul

