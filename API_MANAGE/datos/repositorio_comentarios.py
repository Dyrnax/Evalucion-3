# Archivo: datos/repositorio_comentarios.py
from datos.conexion_db import ConexionDB

# Archivo: datos/repositorio_comentarios.py

class RepositorioComentarios:
    def __init__(self, db_name):
        self.db = ConexionDB(db_name)
    
    def guardar(self, comentario):
        # Verificar si el comentario ya existe
        query_check = "SELECT COUNT(*) FROM comentarios WHERE id = ?"
        count = self.db.obtener_resultados(query_check, (comentario['id'],))
        
        if count[0][0] == 0:  # No existe, entonces insertamos
            query = "INSERT INTO comentarios (id, postId, name, email, body) VALUES (?, ?, ?, ?, ?)"
            self.db.ejecutar_query(query, (comentario['id'], comentario['postId'], comentario['name'], comentario['email'], comentario['body']))
        else:
            print(f"Comentario con id {comentario['id']} ya existe.")
    
    def mostrar(self):
        query = "SELECT * FROM comentarios"
        resultados = self.db.obtener_resultados(query)
        for resultado in resultados:
            print(resultado)

    def obtener_todos(self):
        query = "SELECT * FROM comentarios"
        resultados = self.db.obtener_resultados(query)
        
        comentarios = []
        for resultado in resultados:
            comentarios.append({
                'id': resultado[0],
                'postId': resultado[1],
                'name': resultado[2],
                'email': resultado[3],
                'body': resultado[4]
            })
        return comentarios

