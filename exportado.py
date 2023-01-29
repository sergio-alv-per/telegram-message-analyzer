import os
import json


def exportar_datos_generados(datos_conversacion, analisis_conversacion, nombre_directorio="resultados"):

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
        with open(os.path.join(nombre_directorio, f"recuentos_mensajes_{emisor}.json"), "w", encoding="UTF-8") as archivo:
            json.dump(recuento, archivo, indent=4)


def exportar_series_tiempo(series_tiempo, nombre_directorio):
    for emisor, series in series_tiempo.items():
        for nombre_serie, serie in series.items():
            archivo = os.path.join(
                nombre_directorio, f"series_tiempo_{nombre_serie}_{emisor}.csv")
            serie.sort_index().to_csv(archivo, encoding="UTF-8", header=False)


def exportar_frecuencia_palabras(frecuencia_palabras, nombre_directorio):
    for emisor, frecuencias in frecuencia_palabras.items():
        archivo = os.path.join(
            nombre_directorio, f"frecuencia_palabras_{emisor}.csv")
        frecuencias.sort_index().to_csv(archivo, encoding="UTF-8")


def exportar_analisis_conversacion(analisis_conversacion, nombre_directorio):
    archivo = os.path.join(nombre_directorio, "analisis_conversacion.csv")
    analisis_conversacion["tf_idf_palabras"].to_csv(archivo, encoding="UTF-8")
