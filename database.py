import time
from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
    
@app.route('/')
def index():
    enviar_esp()
    return "Socket.IO server running!"

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit('connection_response', {'status': 'success', 'message': 'Connected to server!'})

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

@socketio.on('mandar_datos_a_esp')
def enviar_esp():
    #def enviar_esp(seteo_ciclos, tiempo_apagado, tiempo_prendido):
    datos = {
        'seteo_ciclos': 20,
        'tiempo_apagado': 30,
        'tiempo_prendido': 40
    }
    emit('mandar_datos_a_esp', datos)

@socketio.on('message')
def handle_message(data):

    global latest_now, latest_temperature, latest_humidity, latest_status, temp, hum, sta
    # Extrae datos del JSON recibido

    latest_now = data.get("now")
    latest_temperature = data.get("temperature")
    latest_humidity = data.get("humidity")
    latest_status = data.get("status")

    temp = latest_temperature
    hum = latest_humidity
    sta = latest_status

    print("Datos recibidos:")
    print("Now:", latest_now)
    print("Temperature:", latest_temperature)
    print("Humidity:", latest_humidity)
    print("Status:", latest_status)

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

@socketio.on('recibirTodosLosDatos')
def handle_recibir_todos_los_datos():
    
    # Send all data back to the client
    data_store = {
    'Temperature': temp,
    'Humidity': hum,
    'Status': sta
    }
    socketio.emit('respuestaTodosLosDatos', data_store)

@app.route('/send_events')
def send_events():
    enviar_esp()
    time.sleep(1)  # Espera un segundo entre envíos para simular un retraso
    return "Eventos enviados."

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
