from flask import Flask,request
from database import obtener_Pin

app = Flask(__name__)

@app.route("/")
def home():
    print('Obteniendo respuesta')
    return "hello world"

@app.route("/registro-entrada", methods=["GET"])
def fecha_hora():
    # Obtener los parámetros de la URL (fecha y hora)
    fecha_hora= request.args.get('fecha_hora')
    fecha,hora = fecha_hora.split()
    # Imprimir los parámetros en la consola
    print(f"Fecha recibida: {fecha}, Hora recibida: {hora}")
    
    return f"Datos recibidos: Fecha={fecha}, Hora={hora}"


@app.route("/obtener-pin", methods=["GET"])
def pin():
    #Obtener Dispositivo para poder obtener usuario
    dispositivo_id = request.args.get("dispositivo-id")
    pin = obtener_Pin(dispositivo_id)  # Solo se obtiene el PIN


    return pin


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') 