import argparse
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

def escoger_conversacion(conversaciones_personales):
    """ Muestra las conversaciones disponibles y devuelve el nombre de la conversación escogida."""
    print("Conversaciones: ")
    for i, conversacion in enumerate(conversaciones_personales):
        print(f"({i}) {conversacion['name']}")
    
    num_conversacion_escogida = int(input("Elige una conversación: "))

    return conversaciones_personales[num_conversacion_escogida]["name"]

def filtrar_mensajes_conversacion(lista_mensajes):
    """ Devuelve una lista con los mensajes de la conversación, descartando mensajes de tipo "service"."""
    return [mensaje for mensaje in lista_mensajes if mensaje["type"] == "message"]

# Lectura de argumentos por línea de comandos
parser = argparse.ArgumentParser()
parser.add_argument("archivo", help="Archivo a leer, el result.json generado por Telegram.")
parser.add_argument("-c", "--chat", help="Nombre de contacto correspondiente a la conversación que se quiere analizar.")

args = parser.parse_args()

# Lectura del archivo JSON, quitando las conversaciones que no son personales
datos_conversaciones = filtrar_conversaciones_personales(leer_archivo_exportado(args.archivo))

# Escoger una conversación y obtener sus datos
if args.chat:
    nombre_conversacion = args.chat
else:
    nombre_conversacion = escoger_conversacion(datos_conversaciones)

lista_mensajes = None
for conversacion in datos_conversaciones:
    if conversacion["name"] == nombre_conversacion:
        lista_mensajes = conversacion["messages"]
        break

lista_mensajes = filtrar_mensajes_conversacion(lista_mensajes)
# Se considera A como el usuario que ejecuta el script y B al otro usuario de la conversación
mensajes_a = 0
mensajes_b = 0

for mensaje in lista_mensajes:
    if mensaje["from"] == nombre_conversacion:
        mensajes_b += 1
    else:
        mensajes_a += 1

print(f"El usuario A ha enviado {mensajes_a} mensajes y el usuario B ({nombre_conversacion}) {mensajes_b}.")
    