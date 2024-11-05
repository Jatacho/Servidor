import sqlite3
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import threading
import time

app = Flask(__name__)

# Variable global para almacenar el valor del sensor más reciente
sensor_value = 0

# Función para crear la base de datos y la tabla
def create_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hora TEXT NOT NULL,
            fecha TEXT NOT NULL,
            valor REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Función para guardar datos cada segundo con el valor del sensor
def save_data():
    global sensor_value
    while True:
        hora = datetime.now().strftime('%H:%M:%S')
        fecha = datetime.now().strftime('%Y-%m-%d')
        
        print(f"Guardando en DB: {hora}, {fecha}, {sensor_value}")  # Imprimir valor antes de guardar
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sensor_data (hora, fecha, valor) VALUES (?, ?, ?)
        ''', (hora, fecha, sensor_value))
        conn.commit()
        conn.close()
        
        time.sleep(1)

# Ruta principal que muestra los datos


# Ruta para recibir datos del sensor
@app.route('/obtener-sensor-data-esp', methods=['POST'])
def in_sensor_data():
    global sensor_value
    data = request.json
    if data:
        sensor_value = data.get("value")  # Actualiza el valor del sensor
        print(f"Valor del sensor recibido: {sensor_value}")
        return jsonify({'status': 'Datos recibidos correctamente'}), 200
    print("Fallo en los datos recibidos")  # Imprimir mensaje de fallo
    return jsonify({'status': 'Fallo en los datos recibidos'}), 400

# Ruta para recibir datos de ciclos
@app.route('/obtener-ciclos-data-esp', methods=['POST'])
def in_ciclos_data():
    global ciclos
    global ciclos_transcurridos
    global ciclos_faltantes
    global estado_SSR
    data = request.json
    if data:
        ciclos = data.get("ciclos")  # Actualiza el valor del sensor
        ciclos_transcurridos = data.get("ciclos_transcurridos")
        ciclos_faltantes = data.get("ciclos_faltantes")
        estado_SSR = data.get("estado")
        print(f"Ciclos: {ciclos}")
        print(f"Ciclos_transcurridos: {ciclos_transcurridos}")
        print(f"Ciclos_faltantes: {ciclos_faltantes}")
        print(f"estado_ssr: {estado_SSR}")
        return jsonify({'status': 'Datos recibidos correctamente'}), 200
    print("Fallo en los datos recibidos")  # Imprimir mensaje de fallo
    return jsonify({'status': 'Fallo en los datos recibidos'}), 400

# Ruta para enviar datos JSON a la ESP8266
@app.route('/enviar-data-esp', methods=['GET'])
def out_esp_data():
    # Crear un diccionario con los datos que deseas enviar
    datos = {
        "set_ciclos": 90,
        "set_tiempo_apagado": 23456789,
        "set_tiempo_encendido": 34567890
    }
    # Devolver los datos como JSON
    return jsonify(datos)

# Ruta para enviar datos JSON a la APP
@app.route('/enviar-data-app', methods=['GET'])
def out_obtener_datos_app():
    # Crear un diccionario con los datos que deseas enviar
    datos = {
        "set_ciclos": {ciclos},
        "ciclos_transcurridos": {ciclos_transcurridos},
        "estado_SSR": {estado_SSR}
    }
    # Devolver los datos como JSON
    return jsonify(datos)

# Ruta para recibir datos de app
@app.route('/obtener-data-app', methods=['POST'])
def sensor_data_app():
    global seteo_ciclos
    global seteo_tiempo_apagado
    global seteo_tiempo_encendido

    data = request.json
    if data:
        seteo_ciclos = data.get("seteo_ciclos")  
        seteo_tiempo_apagado = data.get("seteo_tiempo_apagado")
        seteo_tiempo_encendido = data.get("seteo_tiempo_encendido")
        print(f"Valor de ciclos recibido: {seteo_ciclos}")
        print(f"Valor de apagado recibido: {seteo_tiempo_apagado}")
        print(f"Valor de encendido recibido: {seteo_tiempo_encendido}")
        return jsonify({'status': 'Datos recibidos correctamente'}), 200
    print("Fallo en los datos recibidos")  # Imprimir mensaje de fallo
    return jsonify({'status': 'Fallo en los datos recibidos'}), 400

if __name__ == '__main__':
    create_db()
    threading.Thread(target=save_data, daemon=True).start()  # Inicia el guardado automático en segundo plano
    app.run(host='0.0.0.0', port=5000)

