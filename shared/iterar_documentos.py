import logging
import os
import sys


dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from shared import metodos_formrecognizer, metodos_storage
from shared import validar_documentos
from shared import metodos_storage


def iterar_pdf_paginas(lista_paginas, carpeta_paginas):

    for pagina in lista_paginas:
        ruta_paginas = carpeta_paginas + "//" + pagina
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
            logging.info("ES NOTIFICACION, SE EXTRAE INFORMACION")
            lista_de_respuestas = metodos_formrecognizer.consultar_modelo(
                form, "extraccion"
            )

            entity = crear_entity(lista_de_respuestas, pagina)
            metodos_storage.agregar_entity(entity)


def crear_entity(lista_de_respuestas, pagina):
    entity = {}
    lista_keys = [
        "nombre_notificado",
        "direccion_territorial",
        "resolucion",
        "tipo_notificacion",
        "cedula_notificado",
        "fecha_notificacion",
    ]

    for respuesta in lista_de_respuestas:
        for key in lista_keys:
            if respuesta["label"] == key:
                entity[key] = respuesta["valor"]

    entity["PartitionKey"] = pagina
    entity["RowKey"] = entity["tipo_notificacion"]

    logging.info("Valores Extraidos")
    logging.info("+-+-+-+-+-+")
    logging.info(entity)
    logging.info("+-+-+-+-+-+")

    return entity
