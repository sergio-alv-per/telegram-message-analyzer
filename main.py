import argparse
from preprocesado import preprocesado_archivo_exportado
from procesado import obtener_datos_conversacion



# Lectura de argumentos por línea de comandos
parser = argparse.ArgumentParser()
parser.add_argument("archivo", help="Archivo a leer, el result.json generado por Telegram.")
parser.add_argument("-c", "--chat", help="Nombre de contacto correspondiente a la conversación que se quiere analizar.")

args = parser.parse_args()

lista_mensajes = preprocesado_archivo_exportado(args.archivo, args.chat)

datos_conversacion = obtener_datos_conversacion(lista_mensajes)

