import sqlite3
from auxiliares.constantes import DB_NAME

def inicializar_base_datos():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    # Crear tabla publicaciones
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS publicaciones (
        id INTEGER PRIMARY KEY,
        userId INTEGER NOT NULL,
        title TEXT NOT NULL,
        body TEXT NOT NULL
    );
    """)

    # Crear tabla comentarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comentarios (
        id INTEGER PRIMARY KEY,
        postId INTEGER NOT NULL,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        body TEXT NOT NULL,
        FOREIGN KEY (postId) REFERENCES publicaciones (id)
    );
    """)

    # Crear tabla albums
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS albums (
        id INTEGER PRIMARY KEY,
        userId INTEGER NOT NULL,
        title TEXT NOT NULL
    );
    """)

    # Crear tabla fotos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fotos (
        id INTEGER PRIMARY KEY,
        albumId INTEGER NOT NULL,
        title TEXT NOT NULL,
        url TEXT NOT NULL,
        thumbnailUrl TEXT NOT NULL,
        FOREIGN KEY (albumId) REFERENCES albums (id)
    );
    """)

    # Crear tabla usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        address TEXT NOT NULL,
        phone TEXT NOT NULL,
        website TEXT NOT NULL,
        company TEXT NOT NULL
    );
    """)

    # Crear tabla tareas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tareas (
        id INTEGER PRIMARY KEY,
        userId INTEGER NOT NULL,
        title TEXT NOT NULL,
        completed BOOLEAN NOT NULL,
        FOREIGN KEY (userId) REFERENCES usuarios (id)
    );
    """)

    conexion.commit()
    conexion.close()
    print("Base de datos inicializada correctamente con todas las tablas necesarias.")

if __name__ == "__main__":
    inicializar_base_datos()
