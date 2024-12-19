import bcrypt

def encriptar(contraseña: str) -> str:
    """
    Encripta una contraseña utilizando bcrypt.
    
    Args:
        contraseña (str): Contraseña en texto plano que se desea encriptar.
    
    Returns:
        str: Contraseña encriptada como un string codificado en base64.
    """
    # Generar el hash de la contraseña
    return bcrypt.hashpw(contraseña.encode(), bcrypt.gensalt()).decode()

def desencriptar(contraseña_ingresada: str, contraseña_guardada: str) -> bool:
    """
    Verifica si una contraseña ingresada coincide con la contraseña encriptada almacenada.
    
    Args:
        contraseña_ingresada (str): Contraseña en texto plano ingresada por el usuario.
        contraseña_guardada (str): Contraseña previamente encriptada almacenada.
    
    Returns:
        bool: True si coinciden, False en caso contrario.
    """
    # Comparar la contraseña ingresada con la almacenada
    return bcrypt.checkpw(contraseña_ingresada.encode(), contraseña_guardada.encode())