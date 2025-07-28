@echo off
echo Starting GetCharty Local Deployment...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python first.
    pause
    exit /b 1
)

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo pip is not installed. Please install pip first.
    pause
    exit /b 1
)

echo 📦 Installing Python dependencies...
cd server
pip install --only-binary=all -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    echo Trying alternative installation method...
    pip install --upgrade pip setuptools wheel
    pip install --only-binary=all -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo 🔧 Initializing database...
python init_db.py
if %errorlevel% neq 0 (
    echo ❌ Failed to initialize database
    pause
    exit /b 1
)

cd ..

echo.
echo Starting Flask server on http://localhost:5000...
echo Starting client server on http://localhost:8000...
echo.
echo Upload your CSV files to see the magic!
echo.

REM Start Flask server in background
cd server
start "GetCharty Server" python app.py
cd ..

REM Start HTTP server for client in background
cd client
start "GetCharty Client" python server.py
cd ..

echo Both servers started successfully!
echo Client: http://localhost:8000
echo API: http://localhost:5000
echo.
echo Press any key to stop servers...
pause >nul

REM Kill background processes (Windows doesn't have easy process management)
echo Stopping servers...
taskkill /f /im python.exe >nul 2>&1
echo Servers stopped.
pause 