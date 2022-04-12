import logging


from PyPDF2 import PdfFileWriter, PdfFileReader


def obtener_pdf(str64, file_name, carpeta_notificaciones):
    ruta = carpeta_notificaciones + "/" + file_name
    logging.info(f"guardando en {ruta}")
    with open(ruta, "wb") as f:
        f.write(str64)
    logging.info(f"Archivo guardado en {ruta}")


def dividir_pdf(doc_name, carpeta_notificaciones, carpeta_paginas):
    ruta = carpeta_notificaciones + "/" + str(doc_name)
    pdf_reader = PdfFileReader(open(ruta, "rb"))
    page_num = pdf_reader.getNumPages()

    for page in range(page_num):
        pdf_reader = PdfFileReader(open(ruta, "rb"))
        pdf_writer = PdfFileWriter()
        logging.info(f"pagina {page}")
        pdf_writer.addPage(pdf_reader.getPage(page))
        extension = "_" + str(page) + ".pdf"
        file_name = doc_name.replace(".pdf", extension)
        ruta_paginas = carpeta_paginas + "/" + file_name

        with open(ruta_paginas, "wb") as f:
            pdf_writer.write(f)
