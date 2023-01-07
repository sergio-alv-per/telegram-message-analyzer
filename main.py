import argparse
from collections import Counter, defaultdict
from datetime import datetime
from preprocesado import preprocesado_archivo_exportado

def fecha(momento):
    """ Devuelve la fecha correspondiente al momento dado.
        Un momento es una cadena de texto con el formato: "2020-01-01T20:30:40"

        >>> fecha("2020-01-01T20:30:40")
        "2020-01-01"
    """
    return momento.split("T")[0]

def hora(momento):
    """ Devuelve la hora correspondiente al momento dado.
        
        >>> fecha("2020-01-01T20:30:40")
        "20:30:40"
    """
    return momento.split("T")[1]

def hora_del_dia(momento):
    """ Devuelve la hora del día correspondiente al momento dado.
        
        >>> fecha("2020-01-01T20:30:40")
        "20"
    """
    return momento.split("T")[1].split(":")[0]

def hora_y_minuto(momento):
    """ Devuelve la hora y el minuto correspondientes al momento dado.
    
        >>> hora_y_minuto("2020-01-01T20:30:40")
        "20:30"
    """
    return ":".join(hora(momento).split(":")[:2])

def dia_del_año(momento):
    """ Devuelve el día del año correspondiente al momento dado.
    
        >>> dia_del_año("2020-01-01T20:30:40")
        "01-01"
    """

    return "-".join(fecha(momento).split("-")[1:])

def dia_de_semana(momento):
    """ Devuelve el día de la semana correspondiente al momento dado.
    
        >>> dia_de_semana("2020-01-01T20:30:40")
        "miércoles"
    """
    dias_semana = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    return dias_semana[datetime.strptime(fecha(momento), "%Y-%m-%d").weekday()]

# Lectura de argumentos por línea de comandos
parser = argparse.ArgumentParser()
parser.add_argument("archivo", help="Archivo a leer, el result.json generado por Telegram.")
parser.add_argument("-c", "--chat", help="Nombre de contacto correspondiente a la conversación que se quiere analizar.")

args = parser.parse_args()

lista_mensajes = preprocesado_archivo_exportado(args.archivo, args.chat)

# Estructuras que alamacenarán los datos estadísticos de la conversación
informacion_mensajes = defaultdict(lambda: Counter())
series_tiempo = defaultdict(lambda: defaultdict(lambda: Counter()))
frecuencia_palabras = defaultdict(lambda: Counter())
texto_mensajes = defaultdict(lambda: [])

for mensaje in lista_mensajes:
    autor_mensaje = mensaje["from"]
    momento_mensaje = mensaje["date"]

    series_tiempo[autor_mensaje]["mensajes_por_dia"][fecha(momento_mensaje)] +=1
    series_tiempo[autor_mensaje]["mensajes_por_hora"][hora_del_dia(momento_mensaje)] +=1
    series_tiempo[autor_mensaje]["mensajes_por_minuto"][hora_y_minuto(momento_mensaje)] +=1
    series_tiempo[autor_mensaje]["mensajes_por_dia_año"][dia_del_año(momento_mensaje)] +=1
    series_tiempo[autor_mensaje]["mensajes_por_dia_semana"][dia_de_semana(momento_mensaje)] +=1

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
            informacion_mensajes[autor_mensaje]["duracion_notas_video"] += mensaje["duration_seconds"]
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

    # Si el mensaje no tenía texto (por ejemplo, era un sticker), se ignora
    if texto:
        # Se pasa el texto a minúsculas para "nomalizarlo"
        texto = texto.lower()

        texto_mensajes[autor_mensaje].append(texto)

        palabras = texto.split()

        for palabra in palabras:
            frecuencia_palabras[autor_mensaje][palabra] += 1
