from flask import Flask,jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import psycopg2
import os

app = Flask(__name__)
CORS(app,origins='',supports_credentials=True)
load_dotenv()


def conexion_bd():
    try:
        conn = psycopg2.connect(
            host = os.getenv('DB_HOST'),
            dbname = os.getenv('DB_NAME'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            port = os.getenv('DB_PORT'),
            sslmode = os.getenv('DB_SSL')
        )
        return conn
    except Exception as error:
        print(f'Error inesperado en la base de datos : {error}.')
    except psycopg2.IntegrityError:
        return jsonify({'Error' : 'Error de integridad en la base de datos.'})
