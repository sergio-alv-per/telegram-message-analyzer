import argparse
from preprocesado import preprocesado_archivo_exportado
from ProcesadorMensajes import ProcesadorMensajes


# Lectura de argumentos por línea de comandos
parser = argparse.ArgumentParser()
parser.add_argument("archivo", help="Archivo a leer, el result.json generado por Telegram.")
parser.add_argument("-c", "--chat", help="Nombre de contacto correspondiente a la conversación que se quiere analizar.")

args = parser.parse_args()

lista_mensajes = preprocesado_archivo_exportado(args.archivo, nombre_conversacion=args.chat)

datos_conversacion = ProcesadorMensajes(lista_mensajes).procesar_mensajes()

