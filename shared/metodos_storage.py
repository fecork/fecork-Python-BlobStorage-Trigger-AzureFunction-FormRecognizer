import logging
import os

from azure.storage.blob import BlobServiceClient
from azure.storage.blob import ContainerClient
from azure.data.tables import TableClient
from azure.core.exceptions import ResourceExistsError


def crear_container():

    # Step 3: Retrieve the account's primary access key and generate a connection string.
    logging.info("CONSULTANDO CREDENCIALES")
    RESOURCE_GROUP_NAME = "AZ-EPM-NP-RG-BASECONOCIMIENTOFACTURACION"
    STORAGE_ACCOUNT_NAME = "azsaepmnptipodocident"
    storage_client = StorageManagementClient(credential, subscription_id)

    keys = storage_client.storage_accounts.list_keys(
        RESOURCE_GROUP_NAME, STORAGE_ACCOUNT_NAME
    )

    logging.info(f"Primary key for storage account: {keys.keys[0].value}")

    conn_string = f"DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName={STORAGE_ACCOUNT_NAME};AccountKey={keys.keys[0].value}"

    logging.info(f"Connection string: {conn_string}")
    logging.info("Creando Contenedor")

    connection_string = os.environ["CONNECTION_STRING"]
    container = ContainerClient.from_connection_string(connection_string, "monitoreo")

    try:
        container_properties = container.get_container_properties()
        logging.info("El contenedor ya existe")
        logging.info(container_properties)
        # Container foo exists. You can now use it.

    except Exception as e:
        # Container foo does not exist. You can now create it.
        logging.info(e)
        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )
        container_client = blob_service_client.create_container("monitoreo")
        logging.info("Se crea el contenedor")
        logging.info(container_client)


def agregar_entity(entity):
    logging.info("Creando entidad")
    table_name = os.environ["TABLE_NAME"]
    connection_string = os.environ["CONNECTION_STRING"]
    with TableClient.from_connection_string(
        connection_string, table_name
    ) as table_client:

        try:
            resp = table_client.create_entity(entity)
            logging.info(resp)
        except ResourceExistsError:
            logging.info(f"Entity ya existe en la tabla {table_name}")


def cargar_pdf(blob_name, blob):
    connection_string = os.environ["CONNECTION_STRING"]
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    # crear_container()
    container_name = "notificadormonitoreo"
    path_container = "{}/{}".format(container_name, "datos reentrenamiento")
    file_name = blob_name
    blob_client = blob_service_client.get_blob_client(
        container=path_container, blob=blob_name
    )
    try:
        blob_client.upload_blob(blob)
        logging.info("cargando archivo " + file_name)
    except Exception as e:
        logging.info(f"{file_name} ya exisge en el contenedor {container_name}")
        logging.info(e)
