import logging
import os
import sys

from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from shared import metodos_respuesta


def iniciar_sesion():

    endpoint = os.environ["ENDPOINT"]
    azure_credential = os.environ["AZURE_CREDENTIAL"]
    credential = AzureKeyCredential(azure_credential)
    form_recognizer_client = FormRecognizerClient(endpoint, credential)
    return form_recognizer_client


def reconocer(form, modelo):

    if modelo == "clasificar":
        model_id = os.environ["MODEL_ID_CLASIFICADOR"]

    if modelo == "extraccion":
        model_id = os.environ["MODEL_ID_EXTRACCION"]

    form_recognizer_client = iniciar_sesion()

    poller = form_recognizer_client.begin_recognize_custom_forms(
        model_id=model_id, form=form
    )

    result = poller.result()

    for recognized_form in result:
        logging.info("Form type: {}".format(recognized_form.form_type))
        logging.info(
            "Form type confidence: {}".format(recognized_form.form_type_confidence)
        )
        logging.info(
            "Form was analyzed using model with ID: {}".format(recognized_form.model_id)
        )

    return recognized_form


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
                field.label_data.text if field.label_data else name,
                field.value,
                field.confidence,
            )
        )

        lista_de_names.append(name)
        lista_de_valores.append(field.value)
        lista_de_score.append(field.confidence)
        lista_de_labels.append(field.label_data.text if field.label_data else name)

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
