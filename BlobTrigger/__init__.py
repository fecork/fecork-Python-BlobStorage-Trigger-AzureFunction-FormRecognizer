import logging
import os
import sys

import azure.functions as func

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from shared import iterar_documentos


def main(myblob: func.InputStream):
    logging.info(
        f"Python blob trigger function processed blob \n"
        f"Nombre: {myblob.name}\n"
        f"Blob Size: {myblob.length} bytes"
    )
    logging.info("OK prueba del AZURE FUNCTION")

    form = myblob.read()

    logging.info(type(form))

    ubicacion_nombre = myblob.name.find("/")
    longitud_nombre = len(myblob.name)
    nombre = myblob.name[ubicacion_nombre + 1 : longitud_nombre]
    logging.info(nombre)
    # metodos_pdf.obtener_pdf(form, nombre)
    # metodos_pdf.dividir_pdf(nombre)

    # TODO: guardar datos de extracción en una tabla.

    # carpeta_paginas=os.environ["CARPETA_PAGINAS"]
    carpeta_paginas = "paginas"
    lista_paginas = os.listdir(carpeta_paginas)
    logging.info(lista_paginas)

    iterar_documentos.iterar_pdf_paginas(lista_paginas, carpeta_paginas)
