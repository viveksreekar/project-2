# app.py
# --- Imports ---
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import os

# --- App Initialization ---
app = Flask(__name__, static_folder='.', static_url_path='')
app.config['SECRET_KEY'] = 'your-very-secret-key!' # Replace with a real secret key in production

# --- CORS Configuration ---
# Enable Cross-Origin Resource Sharing to allow the frontend to connect.
CORS(app)

# --- Socket.IO Initialization ---
# We use eventlet as the async_mode for its high performance.
# You will need to install it: pip install eventlet
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# --- Global State ---
# In a real-world application, you would persist this data in a database
# or a more robust in-memory store like Redis. For this example, a simple
# global variable will suffice to hold the current content of the editor.
editor_content = ""

# --- Routes ---

@app.route('/')
def index():
    """
    Serves the main HTML file of the application.
    Flask will look for 'index.html' in the 'templates' folder by default.
    Since we want to serve the file from the root, we'll use a different method.
    """
    # We assume 'index.html' is in the same directory as this script.
    return send_from_directory('.', 'index.html')

# --- Socket.IO Event Handlers ---

@socketio.on('connect')
def handle_connect():
    """
    Handles a new client connection.
    When a user opens the page, this event is fired.
    We send them the most recent version of the code.
    """
    global editor_content
    print(f"Client connected. Sending current content.")
    # Send the current editor content to the newly connected client.
    emit('code_update', editor_content)

@socketio.on('code_change')
def handle_code_change(text):
    """
    Handles incoming code changes from a client.
    When a user types in the editor, this event is fired.
    We update our server state and broadcast the change to all other clients.
    """
    global editor_content
    editor_content = text
    # Broadcast the new content to all clients except the one who sent it.
    # This prevents the sender from receiving their own update.
    emit('code_update', text, broadcast=True, include_self=False)
    print("Code changed, broadcasting to other clients.")


@socketio.on('disconnect')
def handle_disconnect():
    """
    Handles a client disconnection.
    """
    print("Client disconnected.")

# --- Main Execution ---

if __name__ == '__main__':
    """
    Starts the Flask-SocketIO server.
    We use socketio.run() instead of app.run() to ensure the WebSocket
    server is started correctly.
    """
    print("Starting server on http://localhost:5000")
    # The host '0.0.0.0' makes the server accessible from your local network.
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
