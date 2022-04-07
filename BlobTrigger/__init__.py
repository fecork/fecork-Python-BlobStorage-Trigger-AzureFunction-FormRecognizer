import logging
import os
import sys
import json


import azure.functions as func
from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from shared import metodos_respuesta


def main(myblob: func.InputStream):
    logging.info(
        f"Python blob trigger function processed blob \n"
        f"Nombre: {myblob.name}\n"
        f"Blob Size: {myblob.length} bytes"
    )
    logging.info("OK prueba del AZURE FUNCTION")

    # model_id = os.environ["MODEL_ID"]
    model_id = "f058c150-99f7-4348-8bd1-eaa6386b4fdd"
    # endpoint = os.environ["ENDPOINT"]
    endpoint = "https://cog-rut-np-sentencias.cognitiveservices.azure.com/"
    # azure_credential = os.environ["AZURE_CREDENTIAL"]
    azure_credential = "2b507d0b0135482ba7438bd57d1169f0"
    credential = AzureKeyCredential(azure_credential)
    form_recognizer_client = FormRecognizerClient(endpoint, credential)

    form = myblob.read()

    poller = form_recognizer_client.begin_recognize_custom_forms(
        model_id=model_id, form=form
    )

    result = poller.result()

    logging.info("RESULTADO")

    logging.info(result)

    for recognized_form in result:
        logging.info("Form type: {}".format(recognized_form.form_type))
        logging.info(
            "Form type confidence: {}".format(recognized_form.form_type_confidence)
        )
        logging.info(
            "Form was analyzed using model with ID: {}".format(recognized_form.model_id)
        )

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

    lista_de_respuestas = metodos_respuesta.organizar_respuesta(
        lista_de_valores, lista_de_names, lista_de_score, lista_de_labels
    )

    # metodos_monitoreo.monitoreo_score(lista_de_respuestas, file_name, form)

    respuesta = lista_de_respuestas
    logging.info("respuesta")
    logging.info(respuesta)

    # numero_etiquetas = 0
    # for etiqueta in respuesta:
    #     logging.info(etiqueta.valor)
    #     if etiqueta.valor is not None:
    #         numero_etiquetas += 1

    # logging.info(f"Se encontraro {numero_etiquetas} de 3 etiquetas de notificación")

    # return func.HttpResponse(json.dumps(respuesta))
