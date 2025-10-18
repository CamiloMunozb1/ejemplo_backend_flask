from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from backend.logic import conexion
import psycopg2

actualizar_tarea = Blueprint('actualizar_tarea',__name__)

def conexion_bd():
    return conexion.conexion_db()

load_dotenv()

@actualizar_tarea.route('/update', methods = ['POST'])
def actualizar_tarea():
    data = request.get_json()

    estado_tarea = data.get('estado','').strip()
    tarea_id = data.get('tarea_id',None)

    if not all([estado_tarea,tarea_id]):
        return jsonify({'Error' : 'el campo debe estar completos.'}),400
    
    conn = conexion_bd()
    if conn is None:
        return jsonify({'Error' : 'no se encontro la conexion con la base de datos.'}),400
    
    try:
        cursor = conn.cursor()
        cursor.execute('''UPDATE Lista_tareas SET estado_tarea = %s WHERE tarea_id = %s ''',(estado_tarea,tarea_id))
        if cursor.rowcount == 0:
            return jsonify({'Error' : 'No se econtro la tarea'})
        conn.commit()
        return jsonify({'Mensaje' : 'el estado de la tarea se ha completado con exito.'})
    except psycopg2.errors.InternalError:
        conn.rollback()
        return jsonify({'Error' : 'error interno en la base de datos'})
    except Exception as error:
        print(f'Error en la base de datos : {error}.')
    finally:
        cursor.close()
        conn.close()