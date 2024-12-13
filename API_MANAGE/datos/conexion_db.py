import sqlite3
from auxiliares.constantes import DB_NAME
# Archivo: datos/conexion_db.py

class ConexionDB:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name

    # def ejecutar_query(self, query, parametros=None):
    #     with sqlite3.connect(self.db_name) as conn:
    #         cursor = conn.cursor()
    #         if parametros:
    #             cursor.execute(query, parametros)
    #         else:
    #             cursor.execute(query)
    #         conn.commit()

    # def consultar(self, query, parametros=None):
    #     with sqlite3.connect(self.db_name) as conn:
    #         cursor = conn.cursor()
    #         if parametros:
    #             cursor.execute(query, parametros)
    #         else:
    #             cursor.execute(query)
    #         return cursor.fetchall()
    def conectar(self):
        """Establece la conexión con la base de datos"""
        return sqlite3.connect(self.db_name)
    
    def ejecutar_query(self, query, parametros=()):
        """Ejecuta una consulta (INSERT, UPDATE, DELETE)"""
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(query, parametros)
            conn.commit()
    
    def obtener_resultados(self, query, parametros=()):
        """Ejecuta una consulta SELECT y retorna los resultados"""
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(query, parametros)
            return cursor.fetchall()
