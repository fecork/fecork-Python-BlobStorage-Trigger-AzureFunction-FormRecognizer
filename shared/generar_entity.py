import logging
import re


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

    entity = limpiar_entity(entity)

    logging.info("Valores Extraidos")
    logging.info("+-+-+-+-+-+")
    logging.info(entity)
    logging.info("+-+-+-+-+-+")

    return entity


def limpiar_entity(entity):
    entity["nombre_notificado"] = re.sub(r"[^A-Z\s+]", "", entity["nombre_notificado"])
    entity["cedula_notificado"] = re.sub(r"[^0-9]", "", entity["cedula_notificado"])
    return entity
