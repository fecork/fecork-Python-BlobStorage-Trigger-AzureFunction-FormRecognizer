import logging
import os
import sys


dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from shared import metodos_formrecognizer, metodos_storage
from shared import validar_documentos
from shared import metodos_storage
from shared import generar_entity


def iterar_pdf_paginas(lista_paginas, carpeta_paginas):

    formato = ".pdf"
    separador = "_"
    lista_busqueda = []

    for valor in lista_paginas:
        if formato in valor and separador in valor:
            lista_busqueda.append(valor)

    logging.info(f"Lista de archivos a buscar: {lista_busqueda}")
    for pagina in lista_busqueda:
        logging.info(lista_busqueda)
        logging.info(carpeta_paginas)
        logging.info(pagina)
        ruta_paginas = carpeta_paginas + "/" + pagina
        logging.info(ruta_paginas)
        with open(ruta_paginas, "rb") as fd:
            form = fd.read()

        lista_de_respuestas = metodos_formrecognizer.consultar_modelo(
            form, "clasificar"
        )

        # # metodos_monitoreo.monitoreo_score(lista_de_respuestas, file_name, form)

        es_notificacion = validar_documentos.validar_notificacion(
            lista_de_respuestas, pagina
        )

        if es_notificacion:
            logging.warning("ES NOTIFICACION, SE EXTRAE INFORMACION")
            lista_de_respuestas = metodos_formrecognizer.consultar_modelo(
                form, "extraccion"
            )

            entity = generar_entity.crear_entity(lista_de_respuestas, pagina)
            metodos_storage.agregar_entity(entity)
