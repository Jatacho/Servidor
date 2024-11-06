from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)



# Ruta para recibir datos del sensor
@app.route('/sensor-data', methods=['POST'])
def sensor_data():
    data = request.json
    if data:
        sensor_value = data.get('value')
        print(f"Valor del sensor recibido: {sensor_value}")
        return jsonify({'status': 'Datos recibidos correctamente'}), 200
    return jsonify({'status': 'Fallo en los datos recibidos'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)