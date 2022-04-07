import logging
from PyPDF2 import PdfFileWriter, PdfFileReader


def obtner_pdf(str64, file_name):
    # carpeta_notificaciones = os.environ["CARPETA_NOTIFICACIONES"]
    carpeta_notificaciones = "notificaciones"
    ruta = carpeta_notificaciones + "//" + file_name
    logging.info(f"guardando en {ruta}")
    with open(ruta, "wb") as f:
        f.write(str64)


def dividir_pdf(doc_name):
    # carpeta_notificaciones=os.environ["CARPETA_NOTIFICACIONES"]
    # carpeta_paginas=os.environ["CARPETA_PAGINAS"]

    carpeta_paginas = "paginas"
    carpeta_notificaciones = "notificaciones"
    ruta = carpeta_notificaciones + "//" + str(doc_name)
    pdf_reader = PdfFileReader(open(ruta, "rb"))
    pdf_writer = PdfFileWriter()
    page_num = pdf_reader.getNumPages()
    logging.info(page_num)

    for page in range(page_num):
        logging.info(f"pagina {page}")
        pdf_writer.addPage(pdf_reader.getPage(page))
        file_name = doc_name + "_" + str(page) + ".pdf"
        ruta_paginas = carpeta_paginas + "//" + file_name
        file = open(ruta_paginas, "wb")
        pdf_writer.write(file)
        pdf_writer = PdfFileWriter()
