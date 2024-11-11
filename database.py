from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return "Socket.IO server running!"

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit('connection_response', {'status': 'success', 'message': 'Connected to server!'})

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

@socketio.on('message')
def handle_message(data):
    print(f"Message received: {data}")
    response = {
        'status': 'success',
        'message': 'Message received by server',
        'echo': data
    }
    emit('response', response)

@socketio.on('custom_event')
def handle_custom_event(data):
    print(f"Custom event received: {data}")
    response = {
        'status': 'success',
        'event': 'custom_event',
        'data_received': data,
        'message': 'Custom event received by server'
    }
    emit('custom_event_response', response)

@socketio.on('another_event')
def handle_another_event(data):
    print(f"Another event received: {data}")
    response = {
        'status': 'success',
        'event': 'another_event',
        'data': data,
        'message': 'Another event processed by server'
    }
    emit('another_event_response', response)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
