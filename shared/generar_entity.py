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

    for key in lista_keys:
        entity[key] = None

    for respuesta in lista_de_respuestas:
        for key in lista_keys:
            if respuesta["label"] == key:
                entity[key] = respuesta["valor"]

    entity = limpiar_entity(entity)

    entity["PartitionKey"] = pagina
    if entity["tipo_notificacion"] is not None:
        entity["RowKey"] = entity["tipo_notificacion"]
    else:
        entity["RowKey"] = "SIN TIPO"

    logging.info("Valores Extraidos")
    logging.info("+-+-+-+-+-+")
    logging.info(entity)
    logging.info("+-+-+-+-+-+")

    return entity


def limpiar_entity(entity):
    if entity["nombre_notificado"] is not None:
        entity["nombre_notificado"] = entity["nombre_notificado"].upper()
        lista_stops = ["EL", "LA", "SEÑOR", "SEÑORA"]
        for palabra in lista_stops:
            entity["nombre_notificado"] = entity["nombre_notificado"].replace(
                palabra, ""
            )
        # entity["nombre_notificado"] = re.sub(r"[^A-Z\s+]", "", entity["nombre_notificado"])

    if entity["cedula_notificado"] is not None:
        entity["cedula_notificado"] = re.sub(r"[^0-9]", "", entity["cedula_notificado"])

    if entity["tipo_notificacion"] is not None:
        entity["tipo_notificacion"] = re.sub(
            r"[^A-Z_ÑÁÉÍÓÚ\s+]", "", entity["tipo_notificacion"]
        )
        entity["tipo_notificacion"] = entity["tipo_notificacion"].upper()
    return entity
