## Ejemplo de Backend :  Lista de Tareas (To-Do List) con Flask y PostgreSQL
Este repositorio contiene el código de un backend para una aplicación simple de Lista de Tareas, construida con el framework Flask de Python, utilizando PostgreSQL como base de datos, y siguiendo principios de modularidad con Blueprints.

## Tecnologias utilizadas
-Python: Lenguaje de programación principal.
-Flask: Micro-framework para la creación de la API.
-PostgreSQL: Sistema de gestión de bases de datos relacional (DBMS).
-Psycopg2: Adaptador de PostgreSQL para Python.
-Pandas: Utilizado para la lectura de datos SQL y conversión a JSON (ruta /show).
-Flask-CORS: Para manejar las políticas de Cross-Origin Resource Sharing.
-python-dotenv: Para la gestión segura de variables de entorno.

## Estructura del Proyecto
El proyecto está organizado de manera modular para separar la lógica de negocio de la configuración de la aplicación:
                    lista_tareas/
                    ├── backend/
                    │   ├── data/
                    │   │   └── conexion.py   # Módulo que establece la conexión a PostgreSQL.
                    │   └── logic/
                    │       └── tareas_bp.py  # Blueprint con todas las rutas CRUD de Tareas.
                    ├── app.py                # Archivo principal: inicializa Flask, CORS y registra Blueprints.
                    ├── .env.example          # Plantilla para las variables de entorno.
                    └── README.md

##  Configuración del Entorno
Sigue estos pasos para configurar y ejecutar el proyecto localmente.
1. Clonar el Repositorio
          git clone [https://github.com/CamiloMunozb1/ejemplo_backend_flask.git](https://github.com/CamiloMunozb1/ejemplo_backend_flask.git)
   
2.Crear Entorno Virtual e Instalar Dependencias
     # Crear el entorno virtual (venv)
        python3 -m venv venv
  
     # Activar el entorno virtual
        source venv/bin/activate  # Linux/macOS
      .\venv\Scripts\activate   # Windows

    # Instalar las dependencias de Python
    pip install Flask flask-cors python-dotenv psycopg2-binary pandas

3. Configurar la Base de Datos (PostgreSQL)
        Crear la tabla Lista_tareas:
            CREATE TABLE Lista_tareas (
           tarea_id SERIAL PRIMARY KEY,
           nombre_tarea VARCHAR(255) NOT NULL,
           contenido_tarea TEXT,
           estado_tarea VARCHAR(50) NOT NULL -- Ej: 'Pendiente', 'En Progreso', 'Completada'
        );

4. Configurar Variables de Entorno
   Crea un archivo llamado .env en la raíz del proyecto (a la misma altura que app.py) y rellena los siguientes datos con tus credenciales de PostgreSQL:
            DB_HOST=localhost
            DB_NAME=nombre_de_tu_db
            DB_USER=tu_usuario
            DB_PASSWORD=tu_contraseña
            DB_PORT=5432
            DB_SSL=disable

## Autor
  Este proyecto fue creado por Juan Camilo Muñoz bautista.

## License
  Este proyecto esta bajo una licencia MIT.



  


