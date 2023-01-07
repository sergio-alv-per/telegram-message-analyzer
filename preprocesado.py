import json

def leer_archivo_exportado(nombre_archivo):
    """ Lee el archivo JSON generado por Telegram y devuelve un diccionario con los datos."""
    with open(nombre_archivo, encoding="UTF-8") as archivo:
        datos_coversaciones = json.load(archivo)
        return datos_coversaciones

def filtrar_conversaciones_personales(datos_conversaciones):
    """ Devuelve una lista con las conversaciones personales, es decir, excluye los grupos y otros tipos de conversaciones."""
    conversaciones_personales = []
    for conversacion in datos_conversaciones["chats"]["list"]:
        if conversacion["type"] == "personal_chat":
            conversaciones_personales.append(conversacion)
    return conversaciones_personales

def escoger_conversacion_interactivo(conversaciones_personales):
    """ Muestra las conversaciones disponibles y devuelve el nombre de la conversación escogida."""
    print("Conversaciones: ")
    for i, conversacion in enumerate(conversaciones_personales):
        print(f"({i}) {conversacion['name']}")
    
    num_conversacion_escogida = int(input("Elige una conversación: "))

    return conversaciones_personales[num_conversacion_escogida]["name"]

def filtrar_mensajes_servicio(lista_mensajes):
    """ Devuelve una lista con los mensajes de la conversación, descartando mensajes de tipo "service"."""
    return [mensaje for mensaje in lista_mensajes if mensaje["type"] == "message"]

def preprocesado_archivo_exportado(nombre_archivo, nombre_conversacion=None):
    """ Dado un nombre de archivo, devuelve una lista de mensajes de una conversación.

        Para ello:
        1. Lee el archivo exportado de Telegram
        2. Filtra las conversaciones personales
        3. Escoge una conversación, si no se especifica ninguna se obtiene
            de manera interactiva preguntando al usuario.
        4. Filtra los mensajes de la conversación, descartando los que no
            son de tipo "message".
    """

    datos_archivo = leer_archivo_exportado(nombre_archivo)

    datos_conversaciones = filtrar_conversaciones_personales(datos_archivo)

    if not nombre_conversacion:
        nombre_conversacion = escoger_conversacion_interactivo(datos_conversaciones)

    # Se obtiene la lista de mensajes de la conversación escogida
    lista_mensajes = None
    for conversacion in datos_conversaciones:
        if conversacion["name"] == nombre_conversacion:
            lista_mensajes = conversacion["messages"]
            break

    lista_mensajes = filtrar_mensajes_servicio(lista_mensajes)

    return lista_mensajes
