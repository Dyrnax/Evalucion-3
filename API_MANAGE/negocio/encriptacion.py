import hashlib


def encriptar(texto):
    return hashlib.sha256(texto.encode()).hexdigest()

def desencriptar(encriptado, original):
    return encriptar(original)
