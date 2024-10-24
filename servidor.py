from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Permitir CORS para desarrollos en distintos dominios

@app.route('/')
def index():
    return "Servidor WebSocket con Flask está funcionando."

# Evento para recibir y enviar datos en tiempo real
@socketio.on('connect')
def handle_connect():
    print("Cliente conectado.")
    emit('message', {'data': 'Bienvenido al servidor WebSocket'})

@socketio.on('disconnect')
def handle_disconnect():
    print("Cliente desconectado.")

@socketio.on('new_data')
def handle_new_data(data):
    print(f"Datos recibidos: {data}")
    emit('response', {'data': 'Datos recibidos correctamente'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3000)
