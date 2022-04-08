import logging
import os
import sys

import azure.functions as func

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from shared import metodos_formrecognizer


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

    carpeta_paginas = "paginas"
    lista_paginas = os.listdir(carpeta_paginas)
    logging.info(lista_paginas)

    iterar_pdf_paginas(lista_paginas, carpeta_paginas)


def iterar_pdf_paginas(lista_paginas, carpeta_paginas):

    for pagina in lista_paginas:
        ruta_paginas = carpeta_paginas + "//" + pagina
        logging.info(ruta_paginas)
        with open(ruta_paginas, "rb") as fd:
            form = fd.read()

        lista_de_respuestas = metodos_formrecognizer.consultar_modelo(
            form, "clasificar"
        )

        # # metodos_monitoreo.monitoreo_score(lista_de_respuestas, file_name, form)

        es_notificacion = validar_notificacion(lista_de_respuestas, pagina)

        if es_notificacion:
            logging.info("ES NOTIFICACION, SE EXTRAE INFORMACION")
            lista_de_respuestas = metodos_formrecognizer.consultar_modelo(
                form, "extraccion"
            )
            logging.info("VALORES EXTRAIDOS")
            logging.info("===============================")
            logging.info(lista_de_respuestas)
            logging.info("===============================")
