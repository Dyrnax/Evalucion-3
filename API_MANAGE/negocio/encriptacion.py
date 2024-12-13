import bcrypt

def encriptar(contraseña):

    return bcrypt.hashpw(contraseña.encode(), bcrypt.gensalt()).decode()

def verificar_contraseña(contraseña_ingresada, contraseña_guardada):

    return bcrypt.checkpw(contraseña_ingresada.encode(), contraseña_guardada.encode())