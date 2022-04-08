import logging
import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)


from shared import metodos_storage


def monitoreo_score(lista_de_respuestas, file_name, form):
    score_monitor = os.environ["SCORE_MONITOR"]
    for respuestas in lista_de_respuestas:
        if float(respuestas["score"]) < float(score_monitor):
            print("se envía a la base de datos")
            entity = {
                "PartitionKey": respuestas["label"],
                "RowKey": file_name,
                "score": str(respuestas["score"]),
                "valor": respuestas["valor"],
            }
            metodos_storage.agregar_entity(entity)
            metodos_storage.cargar_pdf(file_name, form)
