from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # If the request is for the root path, serve index.html
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

if __name__ == '__main__':
    # Change to the directory containing index.html
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("🌐 Starting GetCharty Client Server...")
    print("📊 Client will be available at: http://localhost:8000")
    print("📁 Upload your CSV files to see the magic!")
    print("")
    
    server = HTTPServer(('localhost', 8000), CustomHandler)
    print("✅ Client server started successfully!")
    print("🌐 Open your browser and go to: http://localhost:8000")
    print("")
    print("Press Ctrl+C to stop the server")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Stopping client server...")
        server.shutdown() 