# Archivo: datos/repositorio_base.py
import sqlite3
from datos.conexion_db import ConexionDB

class RepositorioBase:
    def __init__(self, db_name):
        self.db = ConexionDB(db_name)

    def guardar(self, query, parametros):
        self.db.ejecutar_query(query, parametros)

    def obtener_todos(self, query):
        conexion = sqlite3.connect(self.db.db_name)
        cursor = conexion.cursor()
        cursor.execute(query)
        registros = cursor.fetchall()
        conexion.close()
        return registros
