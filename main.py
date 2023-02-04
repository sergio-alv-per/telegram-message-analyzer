import argparse
from preprocesado import preprocesado_archivo_exportado
from procesado import procesar_mensajes
from analisis import analizar_datos_conversacion
from exportado import exportar_datos_generados
from visualizaciones import generar_visualizaciones


# Lectura de argumentos por línea de comandos
parser = argparse.ArgumentParser()
parser.add_argument("archivo", help="Archivo que leer, el result.json generado por Telegram.",
                    type=argparse.FileType("r", encoding='UTF-8'))

args = parser.parse_args()

print("Preprocesando...")
lista_mensajes = preprocesado_archivo_exportado(args.archivo)

print("Procesando...")
datos_conversacion = procesar_mensajes(lista_mensajes)

print("Analizando...")
analisis_conversacion = analizar_datos_conversacion(datos_conversacion)

print("Exportando...")
exportar_datos_generados(datos_conversacion, analisis_conversacion)

print("Generando visualizaciones...")
generar_visualizaciones(datos_conversacion, analisis_conversacion)

print("¡Listo!")
