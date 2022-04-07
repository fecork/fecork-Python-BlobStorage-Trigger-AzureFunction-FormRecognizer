def organizar_respuesta(
    lista_de_valores, lista_de_names, lista_de_score, lista_de_lables
):
    lista_de_respuestas = []
    for i in range(0, len(lista_de_valores)):
        es_establecimiento = "establecimiento" in str(lista_de_names[i])
        es_representacion = "representacion" in str(lista_de_names[i])

        if not es_establecimiento and not es_representacion:

            lista_de_respuestas.append(
                {
                    "label": lista_de_lables[i],
                    "valor": lista_de_valores[i],
                    "score": lista_de_score[i],
                }
            )

        if es_establecimiento or es_representacion:
            lista_de_respuestas.append(
                {
                    "label": lista_de_lables[i],
                    "valor": str(lista_de_valores[i]),
                    "score": lista_de_score[i],
                }
            )

    return lista_de_respuestas
