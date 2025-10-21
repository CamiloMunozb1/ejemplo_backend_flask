# Importacion de las librerias necesarias para las acciones de la coenexion,
from flask import Flask,jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import psycopg2
import os

# Se integra como aplicacion principal de conexion.
app = Flask(__name__)
# Se habilita conexion con la pagina para el manejo de los datos ingresados por el usuario.
CORS(app,origins='www.ejemplo.com',supports_credentials=True)
load_dotenv() # Carga de las variables de entorno.


def conexion_bd():
    try:
        # Conexion con la base de datos junto con las variables de entorno de estas.
        conn = psycopg2.connect(
            host = os.getenv('DB_HOST'),
            dbname = os.getenv('DB_NAME'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            port = os.getenv('DB_PORT'),
            sslmode = os.getenv('DB_SSL')
        )
        return conn # Retornamos la conexion.
    # manejo de errores
    except Exception as error:
        print(f'Error inesperado en la base de datos : {error}.')
    except psycopg2.IntegrityError:
        return jsonify({'Error' : 'Error de integridad en la base de datos.'}),400
