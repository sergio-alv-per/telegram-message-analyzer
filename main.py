import argparse
from collections import Counter, defaultdict
from datetime import datetime
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

def fecha_a_dia_semana(fecha):
    """ Devuelve el día de la semana correspondiente a la fecha dada."""
    dias_semana = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    return dias_semana[datetime.strptime(fecha, "%Y-%m-%d").weekday()]

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

# Estructuras que alamacenarán los datos estadísticos de la conversación
informacion_mensajes = defaultdict(lambda: Counter())
series_tiempo = defaultdict(lambda: defaultdict(lambda: Counter()))
frecuencia_palabras = defaultdict(lambda: Counter())

for mensaje in lista_mensajes:
    autor_mensaje = mensaje["from"]

    series_tiempo[autor_mensaje]["mensajes_por_dia"][mensaje["date"].split("T")[0]] +=1
    series_tiempo[autor_mensaje]["mensajes_por_hora"][mensaje["date"].split("T")[1].split(":")[0]] +=1
    series_tiempo[autor_mensaje]["mensajes_por_minuto"][":".join(mensaje["date"].split("T")[1].split(":")[:2])] +=1
    series_tiempo[autor_mensaje]["mensajes_por_dia_año"]["-".join(mensaje["date"].split("T")[0].split("-")[1:])] +=1
    series_tiempo[autor_mensaje]["mensajes_por_dia_semana"][fecha_a_dia_semana(mensaje["date"].split("T")[0])] +=1

    informacion_mensajes[autor_mensaje]["num_mensajes"] += 1

    if "photo" in mensaje:
        informacion_mensajes[autor_mensaje]["num_fotos"] += 1
    
    if "media_type" in mensaje:
        if mensaje["media_type"] == "video_file":
            informacion_mensajes[autor_mensaje]["num_videos"] += 1
        elif mensaje["media_type"] == "voice_message":
            informacion_mensajes[autor_mensaje]["num_notas_voz"] += 1
            informacion_mensajes[autor_mensaje]["duracion_notas_voz"] += mensaje["duration_seconds"]
        elif mensaje["media_type"] == "video_message":
            informacion_mensajes[autor_mensaje]["num_notas_video"] += 1
            informacion_mensajes[autor_mensaje]["duracion_videos_video"] += mensaje["duration_seconds"]
        elif mensaje["media_type"] == "sticker":
            informacion_mensajes[autor_mensaje]["num_stickers"] += 1

    # El texto puede ser un string o una lista de strings y diccionarios
    # Los diccionarios representan texto de tipo especial (negrita, cursiva, links, etc.)
    # Solo se procesa el texto especial de tipo negrita y cursiva, el resto se descarta
    texto = ""
    tipos_texto_aceptados = {"italic", "bold"}

    if type(mensaje["text"]) == str:
        texto = mensaje["text"]
    else:
        for t in mensaje["text"]:
            if type(t) == str:
                texto += t
            else:
                if t["type"] in tipos_texto_aceptados:
                    texto += t["text"]

    # Se pasa el texto a minúsculas para evitar que se cuenten palabras repetidas
    palabras = texto.lower().split()

    for palabra in palabras:
        frecuencia_palabras[autor_mensaje][palabra] += 1
