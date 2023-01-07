from collections import Counter, defaultdict
from datetime import datetime
import pandas as pd

class SeriesTiempo():
    """ Clase para almacenar los datos relativos a fechas y horas de los mensajes."""

    def __init__(self):
        self.series_tiempo = defaultdict(lambda: defaultdict(lambda: Counter()))

    def fecha(self, momento):
        """ Devuelve la fecha correspondiente al momento dado.
            Un momento es una cadena de texto con el formato: "2020-01-01T20:30:40"

            >>> fecha("2020-01-01T20:30:40")
            "2020-01-01"
        """
        return momento.split("T")[0]

    def hora(self, momento):
        """ Devuelve la hora correspondiente al momento dado.
            
            >>> fecha("2020-01-01T20:30:40")
            "20:30:40"
        """
        return momento.split("T")[1]

    def hora_del_dia(self, momento):
        """ Devuelve la hora del día correspondiente al momento dado.
            
            >>> fecha("2020-01-01T20:30:40")
            "20"
        """
        return momento.split("T")[1].split(":")[0]

    def hora_y_minuto(self, momento):
        """ Devuelve la hora y el minuto correspondientes al momento dado.
        
            >>> hora_y_minuto("2020-01-01T20:30:40")
            "20:30"
        """
        return ":".join(self.hora(momento).split(":")[:2])

    def dia_del_año(self, momento):
        """ Devuelve el día del año correspondiente al momento dado.
        
            >>> dia_del_año("2020-01-01T20:30:40")
            "01-01"
        """

        return "-".join(self.fecha(momento).split("-")[1:])

    def dia_de_semana(self, momento):
        """ Devuelve el día de la semana correspondiente al momento dado.
        
            >>> dia_de_semana("2020-01-01T20:30:40")
            "miércoles"
        """
        dias_semana = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        return dias_semana[datetime.strptime(self.fecha(momento), "%Y-%m-%d").weekday()]


    def añadir_mensaje(self, mensaje):
        """ Actualiza las series de tiempo según los datos del mensaje."""
        autor_mensaje = mensaje["from"]
        momento_mensaje = mensaje["date"]

        self.series_tiempo[autor_mensaje]["mensajes_por_dia"][self.fecha(momento_mensaje)] +=1
        self.series_tiempo[autor_mensaje]["mensajes_por_hora"][self.hora_del_dia(momento_mensaje)] +=1
        self.series_tiempo[autor_mensaje]["mensajes_por_minuto"][self.hora_y_minuto(momento_mensaje)] +=1
        self.series_tiempo[autor_mensaje]["mensajes_por_dia_año"][self.dia_del_año(momento_mensaje)] +=1
        self.series_tiempo[autor_mensaje]["mensajes_por_dia_semana"][self.dia_de_semana(momento_mensaje)] +=1

    def obtener_series_tiempo(self):
        """ Genera un diccionario con las series de tiempo de cada participante
            de la conversación en forma de Series o DataFrame.
        """
        
        series = {}

        for autor in self.series_tiempo:
            series[autor] = {}

            series[autor]["mensajes_por_dia"] = pd.Series(self.series_tiempo[autor]["mensajes_por_dia"])
            series[autor]["mensajes_por_dia"].index = pd.to_datetime(series[autor]["mensajes_por_dia"].index, format='%Y-%m-%d')

            series[autor]["mensajes_por_hora"] = pd.Series(self.series_tiempo[autor]["mensajes_por_hora"])
            series[autor]["mensajes_por_hora"].index = pd.to_datetime(series[autor]["mensajes_por_hora"].index, format='%H')

            series[autor]["mensajes_por_minuto"] = pd.Series(self.series_tiempo[autor]["mensajes_por_minuto"])
            series[autor]["mensajes_por_minuto"].index = pd.to_datetime(series[autor]["mensajes_por_minuto"].index, format='%H:%M')

            series[autor]["mensajes_por_dia_año"] = pd.Series(self.series_tiempo[autor]["mensajes_por_dia_año"])
            series[autor]["mensajes_por_dia_año"].index = pd.to_datetime(series[autor]["mensajes_por_dia_año"].index, format='%m-%d')

            series[autor]["mensajes_por_dia_semana"] = pd.DataFrame.from_dict(self.series_tiempo[autor]["mensajes_por_dia_semana"], orient="index", columns=["Numero_mensajes"])
            series[autor]["mensajes_por_dia_semana"].index = pd.CategoricalIndex(series[autor]["mensajes_por_dia_semana"].index, categories=["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"], ordered=True)
            series[autor]["mensajes_por_dia_semana"].sort_index(inplace=True)
        
        return series

    
