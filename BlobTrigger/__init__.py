import logging

import azure.functions as func


def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Nombre: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
    logging.info(f"OK prueba del READ")
    

    # model_id = os.environ["MODEL_ID_DOCUMENTOSID"]
    # endpoint = os.environ["ENDPOINT"]
    # azure_credential = os.environ["AZURE_CREDENTIAL"]
    # credential = AzureKeyCredential(azure_credential)
    # form_recognizer_client = FormRecognizerClient(endpoint, credential)

    form = myblob.read()
    logging.info(form)
    # for input_file in myblob.files.values():
    #     file_name = input_file.filename
    #     form = input_file.stream.read()
        
    #     print(file_name)
    #     print(form)

        # poller = form_recognizer_client.begin_recognize_custom_forms(
        #     model_id=model_id, form=form
        # )

        # result = poller.result()

        # logging.info(result)

