# importacion de librerias y funcionalidades modulares.
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from backend.data import conexion
from backend.logic import actualizar_tarea
from backend.logic import eliminar_tarea
from backend.logic import mostrar_tarea
import psycopg2

# Aplicacion principal.
app = Flask(__name__)
# Conexion hacia el frontend.
CORS(app,origins='www.prueba.com',supports_credentials=True)
load_dotenv() # Carga kas varibales de entorno registradas.

# Registramos en la aplicacion principal las funcionalidades modulares.
app.register_blueprint(actualizar_tarea) 
app.register_blueprint(eliminar_tarea)
app.register_blueprint(mostrar_tarea)

# Conexion importada del conjunto de 'data' de la aplicacion.
def conexion_bd():
    return conexion.conexion_bd()

# Enrutador para la creacion de tareas con el metodo 'POST'.
@app.route('/create', methods = ['POST'])
def crear_tarea():
    data = request.get_json() # Convertimos la informacion del usuario a un Json.

    # Entradas de usuario.
    titulo_tarea = data.get('titulo','').strip() 
    contenido_tarea = data.get('contenido','').strip()
    estado_tarea = data.get('estado','').strip()

    # Verificador de los campos.
    if not all([titulo_tarea,contenido_tarea,estado_tarea]):
        return jsonify({'Error' : 'todos los campos deben estar completos.'}),400
    
    # Verificador del estado de la conexion a la base de datos.
    conn = conexion_bd()
    if conn is None:
        return jsonify({'Error' : 'no se encontro la conexion con la base de datos.'}),400
    
    try:
        cursor = conn.cursor() # Cursor para manejo con la base de datos.
        # Consulta de ingreso a la base de datos.
        cursor.execute('''INSERT INTO lista_tareas(nombre_tarea,contenido_tarea,estado_tarea) VALUES (%s,%s,%s) RETURNING tarea_id''',(titulo_tarea,contenido_tarea,estado_tarea))
        tarea_id = cursor.fetchone()[0] # Registra el id de la tarea para las funcionalidades modulares.
        conn.commit() # Se efectuan los cambios en la base de datos.
        # Retorno del mensaje de exito y id de la tarea.
        return jsonify({'Mensaje' : 'Tarea ingresada con exito', 'id' : tarea_id}),201
    # Manejo de errores
    except psycopg2.errors.InternalError:
        conn.rollback() # Si se marca error se eliminan los cambios realizados.
        return jsonify({'Error' : 'error interno de la base de datos.'}),400
    except Exception as error:
        print(f'Error en la base de datos: {error}.'),400
    finally:
        cursor.close() # Cierre del cursor.
        conn.close() # Cierre de la conexion.

