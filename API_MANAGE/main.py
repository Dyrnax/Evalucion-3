import os
import requests
import pickle
from negocio.encriptacion import encriptar, desencriptar
from datos.repositorio_publicaciones import RepositorioPublicaciones
from datos.repositorio_comentarios import RepositorioComentarios
from datos.conexion_db import DB_NAME
from datos.inicializar_db import inicializar_base_datos

API_URL = "https://jsonplaceholder.typicode.com"
ARCHIVO_CONTRASENA = "datos/contrasena.bin"

def guardar_contraseña_encriptada():
    carpeta = os.path.dirname(ARCHIVO_CONTRASENA)
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    contraseña = input("Establece una contrasena para acceder al sistema: ")
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
        print("No se encontró una contrasena guardada.")
        guardar_contraseña_encriptada()
        return True

    intentos = 3
    while intentos > 0:
        contraseña_ingresada = input("Introduce la contrasena: ")
        if desencriptar(contraseña_ingresada, contraseña_guardada):
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

    url_posts = f"{API_URL}/posts"
    url_comments = f"{API_URL}/comments"

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

def post_dato(endpoint, datos):
    url = f"{API_URL}{endpoint}"
    try:
        response = requests.post(url, json=datos)
        if response.status_code == 201:
            print("Recurso creado con éxito:", response.json())
            return response.json()
        else:
            print(f"Error al crear el recurso: {response.status_code} {response.text}")
            return None
    except requests.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return None

def put_dato(endpoint, id_recurso, datos_actualizados):
    url = f"{API_URL}{endpoint}/{id_recurso}"
    try:
        response = requests.put(url, json=datos_actualizados)
        if response.status_code == 200:
            print("Recurso actualizado con éxito:", response.json())
            return response.json()
        else:
            print(f"Error al actualizar el recurso: {response.status_code} {response.text}")
            return None
    except requests.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return None

def delete_dato(endpoint, id_recurso):
    url = f"{API_URL}{endpoint}/{id_recurso}"
    try:
        response = requests.delete(url)
        if response.status_code == 200:
            print("Recurso eliminado con éxito.")
            return True
        else:
            print(f"Error al eliminar el recurso: {response.status_code} {response.text}")
            return False
    except requests.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return False

def enviar_datos_api():
    if not verificar_contraseña():
        return
    print("Ingresa los datos para una nueva publicación:")
    user_id = int(input("User ID: "))
    title = input("Title: ")
    body = input("Body: ")

    nuevo_post = {
        "userId": user_id,
        "title": title,
        "body": body
    }

    post_dato("/posts", nuevo_post)

def actualizar_datos_api():
    if not verificar_contraseña():
        return
    print("Actualiza los datos de una publicación existente:")
    post_id = int(input("ID del post a actualizar: "))
    title = input("Nuevo título: ")
    body = input("Nuevo contenido: ")

    datos_actualizados = {
        "title": title,
        "body": body
    }

    put_dato("/posts", post_id, datos_actualizados)

def eliminar_datos_api():
    if not verificar_contraseña():
        return
    post_id = int(input("ID del post a eliminar: "))
    delete_dato("/posts", post_id)

def menu():
    if not os.path.exists(ARCHIVO_CONTRASENA):
        guardar_contraseña_encriptada()
        
    if not verificar_contraseña():
        print("Acceso denegado. Saliendo del programa.")
        return

    while True:
        print("\n--- Menú ---")
        print("1. Obtener y mostrar datos de la API")
        print("2. Enviar nueva publicación (POST)")
        print("3. Actualizar una publicación (PUT)")
        print("4. Eliminar una publicación (DELETE)")
        print("5. Salir")

        opcion = input("Selecciona una opción (1/2/3/4/5): ")

        if opcion == "1":
            obtener_datos_api()
        elif opcion == "2":
            enviar_datos_api()
        elif opcion == "3":
            actualizar_datos_api()
        elif opcion == "4":
            eliminar_datos_api()
        elif opcion == "5":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida, por favor elige otra.")

if __name__ == "__main__":
    inicializar_base_datos()
    menu()
