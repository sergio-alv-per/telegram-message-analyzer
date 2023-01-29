import json


def leer_archivo_exportado(nombre_archivo):
    """ Lee el archivo JSON generado por Telegram y devuelve un diccionario con los datos."""
    with open(nombre_archivo, encoding="UTF-8") as archivo:
        datos_coversaciones = json.load(archivo)
        return datos_coversaciones


def filtrar_mensajes_servicio(lista_mensajes):
    """ Devuelve una lista con los mensajes de la conversación, descartando mensajes de tipo "service"."""
    return [mensaje for mensaje in lista_mensajes if mensaje["type"] == "message"]


def preprocesado_archivo_exportado(nombre_archivo):
    """ Dado un nombre de archivo, devuelve una lista de mensajes de una conversación."""

    datos_archivo = leer_archivo_exportado(nombre_archivo)

    lista_mensajes = datos_archivo["messages"]

    return filtrar_mensajes_servicio(lista_mensajes)
