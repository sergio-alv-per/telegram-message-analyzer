from collections import Counter, defaultdict
from datetime import datetime, date, time
import pandas as pd

class SeriesTiempo():
    """ Clase para almacenar los datos relativos a fechas y horas de los mensajes."""

    def __init__(self):
        self.series_tiempo = defaultdict(lambda: defaultdict(lambda: Counter()))

    def fecha(self, dt_mensaje):
        return dt_mensaje.date()

    def hora_del_dia(self, dt_mensaje):
        return dt_mensaje.time().hour

    def hora_y_minuto(self, dt_mensaje):
        hora = time(hour=dt_mensaje.time().hour, minute=dt_mensaje.time().minute)
        return hora

    def dia_del_año(self, dt_mensaje):
        return dt_mensaje.timetuple().tm_yday

    def dia_de_semana(self, dt_mensaje):
        return dt_mensaje.weekday()


    def añadir_mensaje(self, mensaje):
        """ Actualiza las series de tiempo según los datos del mensaje."""
        autor_mensaje = mensaje["from"]
        timestamp_mensaje = int(mensaje["date_unixtime"], 10)
        dt_mensaje = datetime.fromtimestamp(timestamp_mensaje)

        self.series_tiempo[autor_mensaje]["mensajes_por_dia"][self.fecha(dt_mensaje)] +=1
        self.series_tiempo[autor_mensaje]["mensajes_por_hora"][self.hora_del_dia(dt_mensaje)] +=1
        self.series_tiempo[autor_mensaje]["mensajes_por_minuto"][self.hora_y_minuto(dt_mensaje)] +=1
        self.series_tiempo[autor_mensaje]["mensajes_por_dia_año"][self.dia_del_año(dt_mensaje)] +=1
        self.series_tiempo[autor_mensaje]["mensajes_por_dia_semana"][self.dia_de_semana(dt_mensaje)] +=1

    def obtener_series_tiempo(self):
        """ Genera un diccionario con las series de tiempo de cada participante
            de la conversación en forma de Series o DataFrame.
        """
        
        series = {}

        for autor in self.series_tiempo:
            series[autor] = {}

            series[autor]["mensajes_por_dia"] = pd.Series(self.series_tiempo[autor]["mensajes_por_dia"])
            series[autor]["mensajes_por_hora"] = pd.Series(self.series_tiempo[autor]["mensajes_por_hora"])
            series[autor]["mensajes_por_minuto"] = pd.Series(self.series_tiempo[autor]["mensajes_por_minuto"])
            series[autor]["mensajes_por_dia_año"] = pd.Series(self.series_tiempo[autor]["mensajes_por_dia_año"])
            series[autor]["mensajes_por_dia_semana"] = pd.Series(self.series_tiempo[autor]["mensajes_por_dia_semana"])
        
        return series

    
