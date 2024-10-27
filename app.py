from flask import Flask,request
from database import obtener_Pin,obtener_chatid, insertar_registro_timbre, insertar_registro_cerradura
import requests
import os  # Asegúrate de importar el módulo os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from urllib.parse import unquote
import json

app = Flask(__name__)

API_TOKEN = '7399497160:AAFnNp-3UsEBPHXj-AK3VYyF5C4BnvTDKYk'

@app.route("/")
def home():
    print('Obteniendo respuesta')
    return "hello world"

@app.route("/registro-entrada", methods=["GET"])
def fecha_hora():
    serial_num = request.args.get('device_id')

    # Obtener los parámetros de la URL (fecha y hora)
    fecha_hora = request.args.get('fecha_hora')
    fecha_hora = unquote(fecha_hora)  # Decodificar la URL
    fecha, hora = fecha_hora.split()
    
    # Imprimir los parámetros en la consola
    insertar_registro_cerradura(serial_num, fecha, hora)

    print(f"Fecha recibida: {fecha}, Hora recibida: {hora}")
    
    return f"Datos recibidos: Fecha={fecha}, Hora={hora}"


@app.route("/obtener-pin", methods=["GET"])
def pin():
    # Obtener Dispositivo para poder obtener usuario
    dispositivo_id = request.args.get("device_id")
    print(dispositivo_id)
    pinacomparar = request.args.get("password")  # Eliminar espacios en blanco
    print(pinacomparar)
    
    pin = obtener_Pin(dispositivo_id)  # Obtener el PIN
    if isinstance(pin, int):  # Verificar si el PIN es un entero
        pin = str(pin)  # Convertir a string si es necesario
    pin = pin  # Eliminar espacios en blanco
    print(pin)

    if pin == pinacomparar:
        return "OK", 200  # Retorna un mensaje de éxito
    else:
        return "PIN incorrecto", 403  # Retorna un mensaje de error

@app.route("/timbre-notificacion", methods=["GET"])
def timbre_notificacion():
    dispositivo_id = request.args.get('data')
    telegram_id = obtener_chatid(dispositivo_id)

    # Obtener la fecha y hora actuales
    fecha_actual = datetime.now().strftime("%Y-%m-%d")  # Obtener solo la fecha
    hora_actual = datetime.now().strftime("%H:%M:%S")   # Obtener solo la hora

    # Llamar a la función para insertar el registro de la cerradura con fecha y hora
    insertar_registro_timbre(dispositivo_id, fecha_actual, hora_actual)  # Asegúrate de que esta función esté definida

    # Crear el teclado de respuesta
    markup = InlineKeyboardMarkup()
    markup.row_width = 2

    # Asegúrate de que los botones tengan el tipo correcto
    markup.add(InlineKeyboardButton(text="Solicitar Imagen", callback_data="solicitar_imagen"),
               InlineKeyboardButton(text="No", callback_data="no"))

    # Enviar el mensaje con el menú
    send_telegram_message("Se ha activado el timbre🛎️. ¿Le gustaría solicitar una imagen?", telegram_id, reply_markup=markup)
    return "Notificación enviada con éxito.", 200  # Mensaje de éxito

def send_telegram_message(message, telegram_id, reply_markup=None):
    # Aquí puedes agregar la lógica para enviar la notificación al bot de Telegram
    url = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'
    payload = {
        'chat_id': telegram_id,
        'text': message,
        'reply_markup': reply_markup.to_json() if reply_markup else None  # Asegúrate de que esto esté correcto
    }
    response = requests.post(url, json=payload)  # Enviar el mensaje al bot de Telegram
    if response.status_code != 200:
        print(f"Error al enviar el mensaje: {response.status_code} - {response.text}")  # Manejo de errores

@app.route("/solicitar-foto", methods=["GET"])
def solicitar_foto():
    chat_id = request.args.get('chatid')
    print(chat_id)

    # Aquí deberías enviar un comando al Raspberry Pi para tomar la foto
    # Suponiendo que tienes una función para enviar comandos al Raspberry
    if enviar_comando_al_raspberry(chat_id):
        return "Solicitud de foto enviada al Raspberry Pi.", 200
    else:
        return "Error al enviar la solicitud al Raspberry Pi.", 500

def enviar_comando_al_raspberry(chat_id):
    try:
        params = {
    'chatid': chat_id  # El valor del chatid que quieres pasar
        }
        # Cambia 'httptu_ip_raspb://<erry>/comando' a la ruta correcta en tu Raspberry Pi
        response = requests.get('http://192.168.1.18:5000/solicitar-foto', params=params )
        return response.status_code == 200  # Retorna True si la respuesta es exitosa
    except Exception as e:
        print(f"Error al enviar comando al Raspberry Pi: {e}")
        return False

@app.route("/enviar-foto", methods=["POST"])
def enviar_foto():
    foto = request.files['file']
    telegram_id = request.form.get('telegram_id')  # Obtener el telegram_id del formulario

    # Verificar que telegram_id no esté vacío
    if not telegram_id:
        return "Error: telegram_id está vacío.", 400

    # Crear la carpeta para almacenar la foto basada en telegram_id
    carpeta = f"./{telegram_id}"
    os.makedirs(carpeta, exist_ok=True)  # Crear la carpeta si no existe

    # Enumerar y agregar fecha y hora a la foto
    fecha_y_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_foto = f"{fecha_y_hora}_{foto.filename}"
    ruta_foto = os.path.join(carpeta, nombre_foto)
    foto.save(ruta_foto)  # Guardar la foto    

    # Enviar la foto al bot de Telegram
    enviar_foto_al_bot(ruta_foto, telegram_id)  # Pasar la ruta del archivo guardado

    return "Foto recibida y almacenada.", 200


def enviar_foto_al_bot(ruta_foto, telegram_id):
    url = f'https://api.telegram.org/bot{API_TOKEN}/sendPhoto'



    # Asegúrate de que 'ruta_foto' sea la ruta del archivo
    with open(ruta_foto, 'rb') as photo_file:  # Abre el archivo de imagen en modo binario

        # 'photo' se envía en 'files', mientras que 'chat_id' y 'caption' se envían en 'data'
        files = {'photo': photo_file}
        data = {
            'chat_id': telegram_id,
            'caption': 'Imagen Solicitada'
        }

        response = requests.post(url, files=files, data=data)  # Enviar el mensaje al bot de Telegram
    
    # Verifica la respuesta
    if response.status_code == 200:
        enviaraudio(telegram_id)
        print("Foto enviada con éxito.")
    else:
        print(f"Error al enviar la foto: {response.status_code} - {response.text}")



def enviaraudio(telegram_id):
    # Obtener la lista de audios
    audios = obtenerAudios()  # Llamar a la función para obtener los nombres de los audios

    # Crear el teclado de respuesta
    markup = InlineKeyboardMarkup()
    markup.row_width = 2

    # Agregar botones al teclado usando los nombres de los audios
    for i, audio in enumerate(audios, start=1):
        markup.add(InlineKeyboardButton(text=f"{i} - {audio}", callback_data=f"audio_{i}"))

    markup.add(InlineKeyboardButton(text="No", callback_data="no"))
    # Enviar el mensaje con el menú
    send_telegram_message("¿Le gustaría responder mediante un audio?", telegram_id, reply_markup=markup)
    return "Notificación enviada con éxito.", 200  # Mensaje de éxito

def obtenerAudios():
    # Simulando la respuesta que obtienes (deberías reemplazar esto con tu lógica real)
    response = requests.get('http://192.168.1.18:5000/solicitarAudios')
    
    # Decodificar la respuesta y cargarla como JSON
    data = json.loads(response.text)
    
    # Retornar solo los nombres de los audios sin la extensión .mp3
    audios = data.get("audios", [])  # Devuelve la lista de audios o una lista vacía si no existe
    return [audio.replace('.mp3', '') for audio in audios]  # Eliminar la extensión .mp3


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') 
