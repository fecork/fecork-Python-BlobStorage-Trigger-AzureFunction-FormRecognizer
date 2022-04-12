import logging
import os
import sys

import azure.functions as func
import tempfile

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from shared import iterar_documentos
from shared import limpiar_ficheros
from shared import metodos_pdf


def main(myblob: func.InputStream):
    logging.info("VERSION: 1.0.7 Con Librería TEMP")
    logging.info("====================================================")
    logging.info(
        f"Se detecta nuevo archivo en el blob \n"
        f"Nombre: {myblob.name}\n"
        f"Blob Size: {myblob.length} bytes"
    )
    logging.info(tempfile.gettempdir())
    logging.info("====================================================")
    carpeta_temporal = tempfile.gettempdir()

    carpeta_paginas = carpeta_temporal
    carpeta_notificaciones = carpeta_temporal
    logging.warning(f"carpeta_paginas: {carpeta_paginas}")
    logging.warning(f"carpeta_notificaciones: {carpeta_notificaciones}")

    documento_stream = myblob.read()
    ubicacion_nombre = myblob.name.find("/")
    longitud_nombre = len(myblob.name)
    nombre_documento = myblob.name[ubicacion_nombre + 1 : longitud_nombre]
    metodos_pdf.obtener_pdf(documento_stream, nombre_documento, carpeta_notificaciones)
    metodos_pdf.dividir_pdf(nombre_documento, carpeta_notificaciones, carpeta_paginas)

    lista_paginas = os.listdir(carpeta_paginas)

    iterar_documentos.iterar_pdf_paginas(lista_paginas, carpeta_paginas)
    limpiar_ficheros.eliminar_archivos(carpeta_paginas)
    limpiar_ficheros.eliminar_archivos(carpeta_notificaciones)
    logging.warning("====================================================")
    logging.warning(f"Proceso de busqueda terminado para el documento {myblob.name}\n")
    logging.warning("====================================================")
