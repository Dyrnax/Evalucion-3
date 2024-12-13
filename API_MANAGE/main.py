import hashlib
import json
import requests
from datos.repositorio_publicaciones import RepositorioPublicaciones
from datos.repositorio_comentarios import RepositorioComentarios
from datos.conexion_db import DB_NAME
from negocio.encriptacion import encriptar, desencriptar
from datos.inicializar_db import inicializar_base_datos

def encriptar_contraseña():
    contraseña = input("Ingresa la contraseña para encriptar: ")
    contrasena_encriptada = encriptar(contraseña)
    print(f"Contraseña encriptada: {contrasena_encriptada}")
    
    # Desencriptar y comparar
    if desencriptar(contrasena_encriptada, contraseña):
        print("La contraseña desencriptada coincide con la original.")
    else:
        print("La contraseña desencriptada NO coincide con la original.")


def obtener_datos_api():
    url_posts = "https://jsonplaceholder.typicode.com/posts"
    url_comments = "https://jsonplaceholder.typicode.com/comments"

    # Obtener los datos de la API
    response_posts = requests.get(url_posts)
    response_comments = requests.get(url_comments)

    if response_posts.status_code == 200 and response_comments.status_code == 200:
        posts = response_posts.json()
        comments = response_comments.json()

        # Crear instancias de repositorios con el nombre de la base de datos
        repositorio_publicaciones = RepositorioPublicaciones(DB_NAME)
        for post in posts:
            repositorio_publicaciones.guardar(post)
            print("Publicación guardada:", post)

        repositorio_comentarios = RepositorioComentarios(DB_NAME)
        for comment in comments:
            repositorio_comentarios.guardar(comment)
            print("Comentario guardado:", comment)

        # Mostrar los datos almacenados
        print("\nDatos almacenados en la base de datos (Publicaciones):")
        publicaciones_guardadas = repositorio_publicaciones.obtener_todos()
        for publicacion in publicaciones_guardadas:
            print(publicacion)

        print("\nDatos almacenados en la base de datos (Comentarios):")
        comentarios_guardados = repositorio_comentarios.obtener_todos()
        for comentario in comentarios_guardados:
            print(comentario)

    else:
        print("Error al obtener datos desde la API.")


def enviar_datos_api():
    url_posts = "https://jsonplaceholder.typicode.com/posts"
    
    # Solicitar al usuario que ingrese los datos para una nueva publicación
    print("Ingresa los datos para una nueva publicación:")
    user_id = int(input("User ID: "))
    title = input("Title: ")
    body = input("Body: ")

    nuevo_post = {
        "userId": user_id,
        "title": title,
        "body": body
    }

    # Realizar el envío de datos a la API
    response = requests.post(url_posts, json=nuevo_post)
    
    if response.status_code == 201:
        print("Publicación enviada con éxito:", response.json())
    else:
        print("Error al enviar la publicación.")


def menu():
    while True:
        print("\n--- Menú ---")
        print("1. Encriptar y desencriptar contraseña")
        print("2. Obtener y mostrar datos de la API")
        print("3. Enviar nueva publicación a la API")
        print("4. Salir")

        opcion = input("Selecciona una opción (1/2/3/4): ")

        if opcion == "1":
            encriptar_contraseña()
        elif opcion == "2":
            obtener_datos_api()
        elif opcion == "3":
            enviar_datos_api()
        elif opcion == "4":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida, por favor elige otra.")


if __name__ == "__main__":
    inicializar_base_datos()
    menu()
