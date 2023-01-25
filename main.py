import argparse
from preprocesado import preprocesado_archivo_exportado
from ProcesadorMensajes import ProcesadorMensajes
from analisis import analizar_datos_conversacion
from exportado import exportar_datos_generados
from visualizaciones import generar_visualizaciones


# Lectura de argumentos por línea de comandos
parser = argparse.ArgumentParser()
parser.add_argument("archivo", help="Archivo a leer, el result.json generado por Telegram.")

args = parser.parse_args()

lista_mensajes = preprocesado_archivo_exportado(args.archivo)

datos_conversacion = ProcesadorMensajes(lista_mensajes).procesar_mensajes()

analisis_conversacion = analizar_datos_conversacion(datos_conversacion)

exportar_datos_generados(datos_conversacion, analisis_conversacion)

generar_visualizaciones(datos_conversacion, analisis_conversacion)