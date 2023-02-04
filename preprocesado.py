import json


def leer_archivo_exportado(archivo):
    """ Dado un archivo JSON abierto con una conversación de Telegram, devuelve
        un diccionario con los datos de la conversación.
    """

    try:
        datos_coversaciones = json.load(archivo)
        return datos_coversaciones
    except json.decoder.JSONDecodeError:
        print("Error: El archivo no es un archivo JSON válido.")
        archivo.close()
        exit(1)


def filtrar_mensajes_servicio(lista_mensajes):
    """ Devuelve una lista con los mensajes de la conversación, descartando
        mensajes que no son de tipo "message", específicamente los de tipo
        "service" que son generados por Telegram en ciertas ocasiones y no
        contienen texto relevante.
    """
    return [mensaje for mensaje in lista_mensajes if mensaje["type"] == "message"]


def preprocesado_archivo_exportado(archivo):
    """ Dado un archivo JSON abierto con una conversación de Telegram, devuelve
        una lista con los mensajes de la conversación y cierra el archivo.
    """

    datos_archivo = leer_archivo_exportado(archivo)

    lista_mensajes = datos_archivo["messages"]

    archivo.close()

    return filtrar_mensajes_servicio(lista_mensajes)
