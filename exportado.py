import os
import json


def exportar_datos_generados(datos_conversacion, analisis_conversacion, nombre_directorio="resultados"):
    """ Exporta los datos generados por el programa a archivos JSON y CSV,
        en el directorio especificado.
    """

    if not os.path.exists(nombre_directorio):
        os.mkdir(nombre_directorio)

    exportar_datos_conversacion(datos_conversacion, nombre_directorio)
    exportar_analisis_conversacion(analisis_conversacion, nombre_directorio)


def exportar_datos_conversacion(datos_conversacion, nombre_directorio):
    exportar_recuentos_mensajes(
        datos_conversacion["recuentos_mensajes"], nombre_directorio)
    exportar_series_tiempo(
        datos_conversacion["series_tiempo"], nombre_directorio)
    exportar_frecuencia_palabras(
        datos_conversacion["frecuencia_palabras"], nombre_directorio)


def exportar_recuentos_mensajes(recuentos_mensajes, nombre_directorio):
    for emisor, recuento in recuentos_mensajes.items():
        nombre_archivo = f"recuentos_mensajes_{emisor}.json"
        ruta_archivo = os.path.join(nombre_directorio, nombre_archivo)
        with open(ruta_archivo, "w", encoding="UTF-8") as archivo:
            json.dump(recuento, archivo, indent=4)


def exportar_series_tiempo(series_tiempo, nombre_directorio):
    for emisor, series in series_tiempo.items():
        for nombre_serie, serie in series.items():
            nombre_archivo = f"series_tiempo_{nombre_serie}_{emisor}.csv"
            ruta_archivo = os.path.join(nombre_directorio, nombre_archivo)
            serie.sort_index().to_csv(ruta_archivo, encoding="UTF-8", header=False)


def exportar_frecuencia_palabras(frecuencia_palabras, nombre_directorio):
    for emisor, frecuencias in frecuencia_palabras.items():
        nombre_archivo = f"frecuencia_palabras_{emisor}.csv"
        ruta_archivo = os.path.join(nombre_directorio, nombre_archivo)
        frecuencias.sort_index().to_csv(ruta_archivo, encoding="UTF-8")


def exportar_analisis_conversacion(analisis_conversacion, nombre_directorio):
    for nombre_analsis, analisis in analisis_conversacion.items():
        nombre_archivo = f"analisis_conversacion_{nombre_analsis}.csv"
        ruta_archivo = os.path.join(nombre_directorio, nombre_archivo)

        analisis.to_csv(ruta_archivo, encoding="UTF-8")
