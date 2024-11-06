from flask import Flask, request
import sqlite3

app = Flask(__name__)

# Función para conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect('mydatabase.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    sensor = data['sensor']
    valor = data['valor']

    # Guardar los datos en la base de datos
    conn = get_db_connection()
    conn.execute('INSERT INTO sensor_data (sensor, valor) VALUES (?, ?)', (sensor, valor))
    conn.commit()
    conn.close()

    print(f"Datos recibidos: {data}")
    return "Datos recibidos", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)