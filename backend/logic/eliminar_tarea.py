from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from backend.logic import conexion
import psycopg2


eliminar_tarea = Blueprint('eliminar_tarea',__name__)

def conexion_bd():
    return conexion.conexion_db()

load_dotenv()


@eliminar_tarea.route('/delete', methods = ['POST'])
def eliminar_tarea():
    data = request.get_json()
    eliminar_tarea = int(data.get('eliminar',''))

    if not eliminar_tarea:
        return jsonify({'Error' : 'el campo debe estar completo'}),400
    
    conn = conexion_bd()
    if conn is None:
        return jsonify({'Error' : 'no se encontro conexion con la base de datos.'}),400
    
    try:
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM Lista_tareas WHERE tarea_id = %s''',(eliminar_tarea,))
        if cursor.fetchone() is None:
            return jsonify({'Error' : 'no se encontro la tarea.'}),400
        cursor.execute('''DELETE FROM lista_tareas WHERE tarea_id = %s''',(eliminar_tarea,))
        if cursor.rowcount == 0:
            return jsonify({'Error' : 'No se encontro la tarea a eliminar.'})
        conn.commit()
        return jsonify({'Mensaje' : 'la tarea se elimino con exito.'})
    except psycopg2.errors.InternalError:
        conn.rollback()
        return jsonify({'Error' : 'error interno en la base de datos.'})
    except Exception as error:
        print(f'Error inespeado en el progrma {error}.')
    finally:
        cursor.close()
        conn.close()