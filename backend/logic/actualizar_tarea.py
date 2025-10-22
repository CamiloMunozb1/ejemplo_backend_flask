# Importacion de las librerias necesarias junto al Blueprint para la modularidad de la aplicacion.
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from backend.data import conexion
import psycopg2

# Registro del Blueprint
actualizar_tarea = Blueprint('actualizar_tarea',__name__)

# Conexion con la base de datos para realizar las acciones correspondientes.
def conexion_bd():
    return conexion.conexion_db()

load_dotenv() # Carga de las variables de entorno

# Entrutador del Blueprint con el metodo 'POST'
@actualizar_tarea.route('/update', methods = ['POST'])
def actualizar_tarea():
    data = request.get_json() # Convierte la informacion pasada por el usuario a un archivo Json.

    # Ingreso del nuevo estado de la tarea .
    estado_tarea = data.get('estado','').strip()
    tarea_id = data.get('tarea_id',None) # Id de la tarea para su busqueda en la base de datos.

    # Validacion de campos.
    if not all([estado_tarea,tarea_id]):
        return jsonify({'Error' : 'el campo debe estar completos.'}),400
    
    # Validacion de conexion con la base de datos.
    conn = conexion_bd()
    if conn is None:
        return jsonify({'Error' : 'no se encontro la conexion con la base de datos.'}),400
    
    try:
        cursor = conn.cursor() # Creacion del cursor para manejo de la base de datos.
        cursor.execute('''UPDATE Lista_tareas SET estado_tarea = %s WHERE tarea_id = %s ''',(estado_tarea,tarea_id)) # Consulta para la actualizacion del estado de la tarea.
        if cursor.rowcount == 0: # Busqueda del id de la tarea.
            return jsonify({'Error' : 'No se econtro la tarea'})
        conn.commit() # Subida de los cambios a la base de datos.
        return jsonify({'Mensaje' : 'el estado de la tarea se ha completado con exito.'})
    # Manejo de errores.
    except psycopg2.errors.InternalError:
        conn.rollback() # Si falla se eliminan los cambios de la base de datos.
        return jsonify({'Error' : 'error interno en la base de datos'})
    except Exception as error:
        print(f'Error en la base de datos : {error}.')
    finally:
        cursor.close() # Cierre del cursor.
        conn.close() # cierre de la conexion con la base de datos.