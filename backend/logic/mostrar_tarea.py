# Importacion de las librerias necesarias junto con el Blueprint para la modularidad de la aplicacion y pandas para la visualizacion de los datos.
from flask import Blueprint, jsonify
from dotenv import load_dotenv
from backend.data import conexion
from pandas import pd
import psycopg2

# Registro del Blueprint.
eliminar_tarea = Blueprint('eliminar_tarea',__name__)

# Conexion con la base de datos.
def conexion_bd():
    return conexion.conexion_db()

load_dotenv() # Carga de las variables de entorno.

# Enrutador del Blueprint con el metodo 'GET'
@eliminar_tarea.route('/show', methods = ['GET'])
def mostrar_tareas():
    try:
        # Campo de verificacion de la conexion con la base de datos.
        conn = conexion_bd()
        if conn is None:
            return jsonify({'Error' : 'no se encontro conexion con la base de datos.'}),400
        df = pd.read_sql_query('''SELECT * FROM Lista_tareas''',conn) # Consulta para tomar la tabla del registro
        resultado = df.to_dict(['records']) # Conversion del archivo Json a un diccionario.
        if not resultado:
            return jsonify({'Resultado' : {resultado}}),200 # Mutesra los registros
        else:
            return jsonify({'Mensaje' : 'no se encontraron datos para mostrar'}),200
    # Manejo de errores.
    except psycopg2.errors.IntegrityError:
        return jsonify({'Error' : 'error de integridad en la base de datos'})
    except Exception as error:
        print(f'Error en la base de datos : {error}.')
    finally:
        conn.close() # Cierre de la conexion.