class ProcesadorPublicaciones:
    def procesar(self, publicaciones):
        return [pub.title.upper() for pub in publicaciones]
