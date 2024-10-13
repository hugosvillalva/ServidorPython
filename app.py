from flask import Flask,request

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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') 