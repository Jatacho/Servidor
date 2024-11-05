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
@app.route('/sensor-data', methods=['POST'])
def sensor_data():
    global sensor_value
    data = request.json
    if data:
        sensor_value = data.get("value")  # Actualiza el valor del sensor
        print(f"Valor del sensor recibido: {sensor_value}")
        return jsonify({'status': 'Datos recibidos correctamente'}), 200
    print("Fallo en los datos recibidos")  # Imprimir mensaje de fallo
    return jsonify({'status': 'Fallo en los datos recibidos'}), 400

# Ruta para recibir datos de ciclos
@app.route('/ciclos-data', methods=['POST'])
def ciclos_data():
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
@app.route('/obtener-data', methods=['GET'])
def obtener_datos():
    # Crear un diccionario con los datos que deseas enviar
    datos = {
        "set_ciclos": 90,
        "set_tiempo_apagado": 23456789,
        "set_tiempo_encendido": 34567890
    }
    # Devolver los datos como JSON
    return jsonify(datos)

if __name__ == '__main__':
    create_db()
    threading.Thread(target=save_data, daemon=True).start()  # Inicia el guardado automático en segundo plano
    app.run(host='0.0.0.0', port=5000)

