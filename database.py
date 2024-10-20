import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="smartkey",
    port="3306"
)
cursor = db.cursor()

def insertar_registro_cerradura(id_dispositivo, fecha, hora):
    # Obtener el id_usuario a partir del id_dispositivo
    cursor.execute(''' 
    SELECT id_usuario FROM dispositivo WHERE id_dispositivo = %s 
    ''', (id_dispositivo,))
    resultado = cursor.fetchone()

    if resultado:
        id_usuario = resultado[0]

        # Insertar en la tabla registro
        cursor.execute(''' 
        INSERT INTO registro (fecha, hora, id_usuario, tipo) VALUES (%s, %s, %s, %s) 
        ''', (fecha, hora, id_usuario, 'cerradura'))  # Asegúrate de que el tipo sea correcto

        # Guardar (commit) los cambios
        db.commit()
    else:
        print("No se encontró el id_usuario para el id_dispositivo proporcionado.")

def insertar_registro_timbre(id_dispositivo, fecha, hora):
    # Obtener el id_usuario a partir del id_dispositivo
    cursor.execute(''' 
    SELECT id_usuario FROM dispositivo WHERE id_dispositivo = %s 
    ''', (id_dispositivo,))
    resultado = cursor.fetchone()

    if resultado:
        id_usuario = resultado[0]

        # Insertar en la tabla registro
        cursor.execute(''' 
        INSERT INTO registro (fecha, hora, id_usuario, tipo) VALUES (%s, %s, %s, %s) 
        ''', (fecha, hora, id_usuario, 'timbre'))  # Asegúrate de que el tipo sea correcto

        # Guardar (commit) los cambios
        db.commit()
    else:
        print("No se encontró el id_usuario para el id_dispositivo proporcionado.")


def obtener_chatid(id_dispositivo):
    try:
        # Obtener ID de usuario a partir del ID del dispositivo
        cursor.execute('''
        SELECT id_usuario FROM dispositivo WHERE id_dispositivo = %s
        ''', (id_dispositivo,))
        resultado = cursor.fetchone()

        if resultado:
            id_usuario = resultado[0]

            # Obtener telegram_id a partir del id_usuario
            cursor.execute('''
            SELECT telegram_id FROM usuario WHERE id_usuario = %s
            ''', (id_usuario,))
            resultado_usuario = cursor.fetchone()

            if resultado_usuario:
                telegram_id = resultado_usuario[0]
                return telegram_id  # Devuelve el telegram_id
            else:
                print("No se encontró el telegram_id para el ID de usuario proporcionado.")
                return None
        else:
            print("No se encontró el ID de usuario para el ID de dispositivo proporcionado.")
            return None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def obtener_Pin(id_dispositivo):
    # Obtener ID de usuario a partir del ID del dispositivo
    cursor.execute(''' 
    SELECT id_usuario FROM dispositivo WHERE id_dispositivo = %s 
    ''', (id_dispositivo,))
    resultado = cursor.fetchone()

    if resultado:
        id_usuario = resultado[0]

        # Obtener el PIN a partir del ID de usuario
        cursor.execute(''' 
        SELECT pin FROM usuario WHERE id_usuario = %s 
        ''', (id_usuario,))
        resultado_pin = cursor.fetchone()

        if resultado_pin:
            pin = resultado_pin[0]
            return pin  # Devuelve el PIN
        else:
            print("No se encontró el PIN para el ID de usuario proporcionado.")
    else:
        print("No se encontró el ID de usuario para el ID de dispositivo proporcionado.")
