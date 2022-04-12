import os
import logging


def eliminar_archivos(carpeta):
    lista_archivos = os.listdir(carpeta)
    formato = ".pdf"
    lista_busqueda = []

    for valor in lista_archivos:
        if formato in valor:
            lista_busqueda.append(valor)

    for archivo in lista_busqueda:
        ruta = f"{carpeta}/{archivo}"
        logging.info(f"Eliminando archivo {ruta}")
        os.unlink(ruta)
