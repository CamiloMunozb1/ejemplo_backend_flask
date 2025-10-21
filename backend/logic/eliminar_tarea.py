# Importacion de las librerias que se utilizaran junto con Blueprint para modularidad y conexion con la logica para la base de datos.
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from backend.data import conexion
import psycopg2

# Registro del Bulueprint.
eliminar_tarea = Blueprint('eliminar_tarea',__name__)

# Conexion con la base de datos desde la carpeta logic.
def conexion_bd():
    return conexion.conexion_db()

load_dotenv() # Carga de variables de entorno.

# Enrutador del Blueprint con el metodo 'POST'.
@eliminar_tarea.route('/delete', methods = ['POST'])
def eliminar_tarea(): 
    data = request.get_json() # Se convirte la informacion ingresada en el archivo Json.
    eliminar_tarea = int(data.get('eliminar','')) # Se indica el Id que se va a eliminar.

    # Verificacion de campo.
    if not eliminar_tarea:
        return jsonify({'Error' : 'el campo debe estar completo'}),400
    
    # Verificacion de la conexion con la base de datos.
    conn = conexion_bd()
    if conn is None:
        return jsonify({'Error' : 'no se encontro conexion con la base de datos.'}),400
    
    try:
        cursor = conn.cursor() # Creacion del cursor para manipular la base de datos.
        cursor.execute('''SELECT * FROM Lista_tareas WHERE tarea_id = %s''',(eliminar_tarea,))
        # Se buscan las tareas.
        if cursor.fetchone() is None:
            return jsonify({'Error' : 'no se encontraron tareas.'}),400
        # Se busca la tarea en especifico desde el id.
        cursor.execute('''DELETE FROM lista_tareas WHERE tarea_id = %s''',(eliminar_tarea,))
        if cursor.rowcount == 0: # buscamos el id desde el primer indice
            return jsonify({'Error' : 'No se encontro la tarea a eliminar.'}),400
        conn.commit() # Se efectuan los cambios.
        return jsonify({'Mensaje' : 'la tarea se elimino con exito.'})
    # Manejo de errores.
    except psycopg2.errors.InternalError:
        conn.rollback() # Si se detecta el error se eliminan los cambios
        return jsonify({'Error' : 'error interno en la base de datos.'})
    except Exception as error:
        print(f'Error inespeado en el progrma {error}.')
    finally:
        cursor.close() # Cierre del cursor.
        conn.close() # Cierre de la conexion.