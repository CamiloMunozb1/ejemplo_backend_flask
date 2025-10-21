from flask import Blueprint, jsonify
from dotenv import load_dotenv
from backend.data import conexion
from pandas import pd
import psycopg2


eliminar_tarea = Blueprint('eliminar_tarea',__name__)

def conexion_bd():
    return conexion.conexion_db()

load_dotenv()

@eliminar_tarea.route('/show', methods = ['GET'])
def mostrar_tareas():
    try:
        conn = conexion_bd()
        if conn is None:
            return jsonify({'Error' : 'no se encontro conexion con la base de datos.'}),400
        df = pd.read_sql_query('''SELECT * FROM Lista_tareas''',conn)
        resultado = df.to_dict(['records'])
        if not resultado.empty():
            return jsonify({'Resultado' : {resultado}}),200
        else:
            return jsonify({'Mensaje' : 'no se encontraron datos para mostrar'}),200
    except psycopg2.errors.IntegrityError:
        return jsonify({'Error' : 'error de integridad en la base de datos'})
    except Exception as error:
        print(f'Error en la base de datos : {error}.')
    finally:
        conn.close()