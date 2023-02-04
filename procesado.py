from Recuentos import Recuentos
from SeriesTiempo import SeriesTiempo
from TextoMensajes import TextoMensajes


def procesar_mensajes(lista_mensajes):
    """ Procesa una lista de mensajes de Telegram, obteniendo datos de interés.
        Se devuelven estos datos en un diccionario.
    """

    series_tiempo = SeriesTiempo()
    texto_mensajes = TextoMensajes()
    recuentos = Recuentos()

    for mensaje in lista_mensajes:
        series_tiempo.añadir_mensaje(mensaje)

        texto_mensajes.añadir_mensaje(mensaje)

        recuentos.añadir_mensaje(mensaje)

    return {"recuentos_mensajes": recuentos.obtener_recuentos(),
            "series_tiempo": series_tiempo.obtener_series_tiempo(),
            "frecuencia_palabras": texto_mensajes.obtener_frecuencia_palabras(),
            "texto_mensajes": texto_mensajes.obtener_lista_mensajes()}
