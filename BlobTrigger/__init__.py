import logging

import azure.functions as func


def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Nombre: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
    logging.info(f"OK {myblob}")
