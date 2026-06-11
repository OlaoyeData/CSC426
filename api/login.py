import json
from http.server import BaseHTTPRequestHandler

# Dummy user database (replace with env vars for production)
USERS = {
    "admin": "password123",
    "user": "letmein"
}

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Read request body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        try:
            data = json.loads(body)
        except:
            self.send_error_response(400, "Invalid JSON")
            return

        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        if not username or not password:
            self.send_error_response(400, "Username and password are required.")
            return

        if username in USERS and USERS[username] == password:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "success",
                "message": f"Welcome, {username}!"
            }).encode())
        else:
            self.send_error_response(401, "Invalid username or password.")

    def send_error_response(self, status_code, message):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "error",
            "message": message
        }).encode())