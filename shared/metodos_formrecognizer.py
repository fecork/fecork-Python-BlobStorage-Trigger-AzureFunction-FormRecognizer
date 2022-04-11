import logging
import os
import sys

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from shared import metodos_respuesta


def iniciar_sesion():

    endpoint = os.environ["ENDPOINT"]
    azure_credential = os.environ["AZURE_CREDENTIAL"]
    credential = AzureKeyCredential(azure_credential)
    form_recognizer_client = DocumentAnalysisClient(endpoint, credential)
    return form_recognizer_client


def reconocer(form, modelo):

    if modelo == "clasificar":
        model_id = os.environ["MODEL_ID_CLASIFICADOR"]

    if modelo == "extraccion":
        model_id = os.environ["MODEL_ID_EXTRACCION"]

    form_recognizer_client = iniciar_sesion()

    poller = form_recognizer_client.begin_analyze_document(
        model=model_id, document=form
    )

    result = poller.result()

    for idx, document in enumerate(result.documents):
        logging.info("--------Analyzing document #{}--------".format(idx + 1))
        logging.info("Document has type {}".format(document.doc_type))
        logging.info("Document has confidence {}".format(document.confidence))
        logging.info(
            "Document was analyzed by model with ID {}".format(result.model_id)
        )
    for name, field in document.fields.items():
        field_value = field.value if field.value else field.content
        logging.info(
            "......found field of type '{}' with value '{}' and with confidence {}".format(
                field.value_type, field_value, field.confidence
            )
        )

    return document


def enlistar(recognized_form):

    lista_de_valores = []
    lista_de_score = []
    lista_de_labels = []
    lista_de_names = []
    for name, field in recognized_form.fields.items():

        logging.info(
            "Field '{}' has label '{}' with value '{}' and a confidence"
            " score of {}".format(
                name,
                name,
                field.value,
                field.confidence,
            )
        )

        lista_de_names.append(name)
        lista_de_valores.append(field.value)
        lista_de_score.append(field.confidence)
        lista_de_labels.append(name)

    return {
        "nombres": lista_de_names,
        "valores": lista_de_valores,
        "scores": lista_de_score,
        "labels": lista_de_labels,
    }


def consultar_modelo(form, modelo):
    recognized_form = reconocer(form, modelo)

    respuesta_organizada = enlistar(recognized_form)

    lista_de_respuestas = metodos_respuesta.organizar_respuesta(
        respuesta_organizada["valores"],
        respuesta_organizada["nombres"],
        respuesta_organizada["scores"],
        respuesta_organizada["labels"],
    )

    return lista_de_respuestas
