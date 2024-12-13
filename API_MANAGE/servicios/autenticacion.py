import requests
from auxiliares.constantes import SERPER_API_URL, SERPER_API_KEY

class Autenticador:
    def buscar(self, termino):
        headers = {"Authorization": f"Bearer {SERPER_API_KEY}"}
        params = {"q": termino}
        respuesta = requests.get(SERPER_API_URL, headers=headers, params=params)
        return respuesta.json() if respuesta.status_code == 200 else []
