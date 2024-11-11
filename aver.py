from flask import Flask
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return "Socket.IO server running!"

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit('message', {'data': 'Connected to server!'}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

@socketio.on('message')
def handle_message(msg):
    print(f"Message received: {msg}")
    emit('response', {'data': 'Message received by server'}, broadcast=True)

@socketio.on('event')
def handle_custom_event(data):
    print(f"Custom event received: {data}")
    emit('response', {'data': 'Event received by server'}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
