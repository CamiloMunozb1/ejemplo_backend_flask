from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from backend.data import conexion
from backend.logic import actualizar_tarea
from backend.logic import eliminar_tarea
from backend.logic import mostrar_tarea
import psycopg2

app = Flask(__name__)
CORS(app,origins='www.prueba.com',supports_credentials=True)
load_dotenv()

app.register_blueprint(actualizar_tarea)
app.register_blueprint(eliminar_tarea)
app.register_blueprint(mostrar_tarea)


def conexion_bd():
    return conexion.conexion_bd()

@app.route('/create', methods = ['POST'])
def crear_tarea():
    data = request.get_json()

    titulo_tarea = data.get('titulo','').strip()
    contenido_tarea = data.get('contenido','').strip()
    estado_tarea = data.get('estado','').strip()

    if not all([titulo_tarea,contenido_tarea,estado_tarea]):
        return jsonify({'Error' : 'todos los campos deben estar completos.'}),400
        
    conn = conexion_bd()
    if conn is None:
        return jsonify({'Error' : 'no se encontro la conexion con la base de datos.'}),400
    
    try:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO lista_tareas(nombre_tarea,contenido_tarea,estado_tarea) VALUES (%s,%s,%s) RETURNING tarea_id''',(titulo_tarea,contenido_tarea,estado_tarea))
        tarea_id = cursor.fetchone()[0]
        conn.commit()
        return jsonify({'Mensaje' : 'Tarea ingresada con exito', 'id' : tarea_id}),201
    except psycopg2.errors.InternalError:
        conn.rollback()
        return jsonify({'Error' : 'error interno de la base de datos.'}),400
    except Exception as error:
        print(f'Error en la base de datos: {error}.'),400
    finally:
        cursor.close()
        conn.close()

