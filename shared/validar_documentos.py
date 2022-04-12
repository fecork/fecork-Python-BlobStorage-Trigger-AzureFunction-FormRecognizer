import logging
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from shared import metodos_storage


def validar_notificacion(lista_de_respuestas, pagina):
    logging.info("VALIDAR NOTIFICACION")
    score_validar = float(os.environ["SCORE_VALIDAR"])
    etiquetas_validar = int(os.environ["NUMERO_ETIQUETAS_VALIDACION"])

    numero_etiquetas = 0
    for etiqueta in lista_de_respuestas:

        valor = etiqueta["valor"]
        score = etiqueta["score"]

        if valor is not None and float(score) >= float(score_validar):
            numero_etiquetas += 1

        if (
            valor is not None
            and float(score) < score_validar
            and numero_etiquetas >= etiquetas_validar
        ):
            logging.info(f"{pagina} - {valor} - {score}")
            ruta = os.environ["CARPETA_PAGINAS"] + "//" + pagina
            metodos_storage.cargar_pdf(pagina, ruta)

    logging.warning(
        f"Se encontraron {numero_etiquetas} de 3 etiquetas de notificacion, en {pagina}"
    )

    if numero_etiquetas >= etiquetas_validar:
        logging.warning(f"el archivo {pagina} ES NOTIFICACION")
        return True
    else:
        logging.info(f"el archivo {pagina} NO ES NOTIFICACION")
        return False
