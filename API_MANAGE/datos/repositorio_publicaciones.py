
from datos.conexion_db import ConexionDB

# Archivo: datos/repositorio_publicaciones.py

# Archivo: datos/repositorio_publicaciones.py

class RepositorioPublicaciones:
    def __init__(self, db_name):
        self.db = ConexionDB(db_name)
    
    def guardar(self, publicacion):
        # Verificar si la publicación ya existe
        query_check = "SELECT COUNT(*) FROM publicaciones WHERE id = ?"
        count = self.db.obtener_resultados(query_check, (publicacion['id'],))
        
        if count[0][0] == 0:  # No existe, entonces insertamos
            query = "INSERT INTO publicaciones (id, userId, title, body) VALUES (?, ?, ?, ?)"
            self.db.ejecutar_query(query, (publicacion['id'], publicacion['userId'], publicacion['title'], publicacion['body']))
        else:
            print(f"Publicación con id {publicacion['id']} ya existe.")
    
    def mostrar(self):
        query = "SELECT * FROM publicaciones"
        resultados = self.db.obtener_resultados(query)
        for resultado in resultados:
            print(resultado)

    def obtener_todos(self):
        query = "SELECT * FROM publicaciones"
        resultados = self.db.obtener_resultados(query)
        
        publicaciones = []
        for resultado in resultados:
            publicaciones.append({
                'id': resultado[0],
                'userId': resultado[1],
                'title': resultado[2],
                'body': resultado[3]
            })
        return publicaciones

