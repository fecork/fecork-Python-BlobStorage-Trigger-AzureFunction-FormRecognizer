import logging


def validar_notificacion(lista_de_respuestas, pagina):
    logging.info("VALIDAR NOTIFICACION")
    # score_validar = os.environ["SCORE_VALIDAR"]
    score_validar = 0.3
    numero_etiquetas = 0
    for etiqueta in lista_de_respuestas:

        valor = etiqueta["valor"]
        score = etiqueta["score"]

        if valor is not None and float(score) >= score_validar:
            numero_etiquetas += 1

    logging.info(
        f"Se encontraro {numero_etiquetas} de 3 etiquetas de notificacion, en {pagina}"
    )

    if numero_etiquetas >= 1:
        logging.info("ES NOTIFICACION")
        return True
    else:
        logging.info("NO ES NOTIFICACION")
        return False
