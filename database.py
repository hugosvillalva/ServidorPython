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
    SELECT id_usuario FROM dispositivo WHERE id_dispositivo = ?
    ''', (id_dispositivo,))
    resultado = cursor.fetchone()

    if resultado:
        id_usuario = resultado[0]

        # Insertar en la tabla registro
        cursor.execute('''
        INSERT INTO registro (fecha, hora, id_usuario, tipo) VALUES (?, ?, ?, ?)
        ''', (fecha, hora, id_usuario, 'cerradura'))

        # Guardar (commit) los cambios
        db.commit()
    else:
        print("No se encontró el id_usuario para el id_dispositivo proporcionado.")



def obtener_Pin(id_dispositivo):
    # Obtener ID de usuario y PIN a partir del ID del dispositivo
    cursor.execute('''
    SELECT id_usuario, pin FROM dispositivo WHERE id_dispositivo = ?
    ''', (id_dispositivo,))
    resultado = cursor.fetchone()

    if resultado:
        id_usuario = resultado[0]
        pin = resultado[1]
        return pin  # Devuelve ambos valores
    else:
        print("No se encontró el ID de usuario o PIN para el ID de dispositivo proporcionado.")
