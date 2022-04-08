import os
import logging


def eliminar_archivos(carpeta):
    lista_archivos = os.listdir(carpeta)
    for archivo in lista_archivos:
        ruta = f"{carpeta}/{archivo}"
        logging.info(f"Eliminando archivo {ruta}")
        os.unlink(ruta)
