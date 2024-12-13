import os
import requests
import pickle
from negocio.encriptacion import encriptar, desencriptar
from datos.repositorio_publicaciones import RepositorioPublicaciones
from datos.repositorio_comentarios import RepositorioComentarios
from datos.conexion_db import DB_NAME
from datos.inicializar_db import inicializar_base_datos

ARCHIVO_CONTRASENA = "datos/contrasena.bin"

def guardar_contraseña_encriptada():
    carpeta = os.path.dirname(ARCHIVO_CONTRASENA)
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    contraseña = input("Establece una contraseña para acceder al sistema: ")
    contraseña_encriptada = encriptar(contraseña)
    with open(ARCHIVO_CONTRASENA, 'wb') as archivo:
        pickle.dump(contraseña_encriptada, archivo)
    print("Contraseña establecida con éxito.")

def cargar_contraseña_encriptada():
    if not os.path.exists(ARCHIVO_CONTRASENA):
        return None

    try:
        with open(ARCHIVO_CONTRASENA, 'rb') as archivo:
            return pickle.load(archivo)
    except (pickle.UnpicklingError, EOFError):
        print("El archivo de contraseña está corrupto. Se eliminará y se pedirá una nueva contraseña.")
        os.remove(ARCHIVO_CONTRASENA)
        return None
    
def verificar_contraseña():
    contraseña_guardada = cargar_contraseña_encriptada()

    if contraseña_guardada is None:
        print("No se encontró una contraseña guardada.")
        guardar_contraseña_encriptada()
        return True

    intentos = 3
    while intentos > 0:
        contraseña_ingresada = input("Introduce la contraseña: ")
        if desencriptar(contraseña_guardada, contraseña_ingresada):
            print("Contraseña correcta. Acceso permitido.")
            return True
        else:
            intentos -= 1
            print(f"Contraseña incorrecta. Te quedan {intentos} intentos.")

    print("Has excedido el número de intentos. Acceso denegado.")
    return False



def obtener_datos_api():
    if not verificar_contraseña():
        return

    url_posts = "https://jsonplaceholder.typicode.com/posts"
    url_comments = "https://jsonplaceholder.typicode.com/comments"

    # Obtener los datos de la API
    response_posts = requests.get(url_posts)
    response_comments = requests.get(url_comments)

    if response_posts.status_code == 200 and response_comments.status_code == 200:
        posts = response_posts.json()
        comments = response_comments.json()

        repositorio_publicaciones = RepositorioPublicaciones(DB_NAME)
        for post in posts:
            repositorio_publicaciones.guardar(post)
            print("Publicación guardada:", post)

        repositorio_comentarios = RepositorioComentarios(DB_NAME)
        for comment in comments:
            repositorio_comentarios.guardar(comment)
            print("Comentario guardado:", comment)

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
    """
    Envía datos a la API.
    """
    if not verificar_contraseña():
        return
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
    """
    Muestra el menú principal.
    """
    if not os.path.exists(ARCHIVO_CONTRASENA):
        guardar_contraseña_encriptada()
        
    if not verificar_contraseña():
        print("Acceso denegado. Saliendo del programa.")
        return

    while True:
        print("\n--- Menú ---")
        print("1. Obtener y mostrar datos de la API (requiere contraseña)")
        print("2. Enviar nueva publicación a la API (requiere contraseña)")
        print("3. Salir")

        opcion = input("Selecciona una opción (1/2/3): ")

        if opcion == "1":
            obtener_datos_api()
        elif opcion == "2":
            enviar_datos_api()
        elif opcion == "3":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida, por favor elige otra.")

if __name__ == "__main__":
    inicializar_base_datos()
    menu()

