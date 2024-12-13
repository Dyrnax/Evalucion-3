import requests
from auxiliares.constantes import BASE_URL

class APIHandler:
    def obtener_datos(self, grupo):
        url = f"{BASE_URL}/{grupo}"
        respuesta = requests.get(url)
        return respuesta.json() if respuesta.status_code == 200 else []

    def enviar_datos(self, grupo, datos):
        url = f"{BASE_URL}/{grupo}"
        respuesta = requests.post(url, json=datos)
        return respuesta.json() if respuesta.status_code == 201 else {}
