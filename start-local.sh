#!/bin/bash

echo "Starting GetCharty Local Deployment..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed. Please install pip3 first."
    exit 1
fi

echo "Installing Python dependencies..."
cd server
pip3 install -r requirements.txt
cd ..

echo ""
echo "Starting Flask server on http://localhost:5000..."
echo "Starting client server on http://localhost:8000..."
echo ""
echo "Upload your CSV files to see the magic!"
echo ""

# Start Flask server in background
cd server
python3 app.py &
SERVER_PID=$!
cd ..

# Start HTTP server for client in background
cd client
python3 -m http.server 8000 &
CLIENT_PID=$!
cd ..

echo "Both servers started successfully!"
echo "Client: http://localhost:8000"
echo "API: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user to stop
trap "echo ''; echo 'Stopping servers...'; kill $SERVER_PID $CLIENT_PID 2>/dev/null; exit" INT
wait 