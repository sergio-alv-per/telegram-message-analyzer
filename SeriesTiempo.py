from collections import Counter, defaultdict
from datetime import datetime
import pandas as pd


class SeriesTiempo():
    """ Clase para gestionar los datos relativos a tiempo (fechas y horas) de
        los mensajes.
    """

    def __init__(self):
        # Se usan dos diccionarios anidados. El primero tendrá por clave el
        # nombre del participante de la conversación.
        # Cada participante de la conversación tendrá un diccionario con clave
        # el tipo de serie de tiempo (mensajes_por_dia, mensajes_por_hora, etc.)
        # y como valor un objeto Counter.

        # A mayores, se usa un defaultdict para evitar tener que comprobar si
        # existen las claves en los diccionarios, ya que se conoce cual será su
        # valor por defecto.

        self.series_tiempo = defaultdict(
            lambda: defaultdict(lambda: Counter()))

    def actualizar_mensajes_por_dia(self, autor_mensaje, dt_mensaje):
        """ Actualiza la serie de tiempo de mensajes por día para el autor dado."""
        dia = dt_mensaje.date()
        self.series_tiempo[autor_mensaje]["mensajes_por_dia"][dia] += 1

    def actualizar_mensajes_por_hora(self, autor_mensaje, dt_mensaje):
        """ Actualiza la serie de tiempo de mensajes por hora."""
        hora = dt_mensaje.time().hour
        self.series_tiempo[autor_mensaje]["mensajes_por_hora"][hora] += 1

    def hora_y_minuto(self, dt_mensaje):
        """ Dado un objeto datetime, devuelve un objeto time con la hora y el
            minuto. Esto se hace para descartar la parte de los segundos.
        """
        return dt_mensaje.time().replace(second=0, microsecond=0)

    def actualizar_mensajes_por_minuto(self, autor_mensaje, dt_mensaje):
        """ Actualiza la serie de tiempo de mensajes por minuto."""
        hora_y_minuto = self.hora_y_minuto(dt_mensaje)

        self.series_tiempo[autor_mensaje]["mensajes_por_minuto"][hora_y_minuto] += 1

    def actualizar_mensajes_por_dia_año(self, autor_mensaje, dt_mensaje):
        """ Actualiza la serie de tiempo de mensajes por día del año."""
        dia_año = dt_mensaje.timetuple().tm_yday
        self.series_tiempo[autor_mensaje]["mensajes_por_dia_año"][dia_año] += 1

    def actualizar_mensajes_por_dia_semana(self, autor_mensaje, dt_mensaje):
        """ Actualiza la serie de tiempo de mensajes por día de la semana."""
        dia_semana = dt_mensaje.weekday()
        self.series_tiempo[autor_mensaje]["mensajes_por_dia_semana"][dia_semana] += 1

    def añadir_mensaje(self, mensaje):
        """ Actualiza las series de tiempo según la fecha y el autor del mensaje."""
        autor_mensaje = mensaje["from"]
        timestamp_mensaje = int(mensaje["date_unixtime"], 10)
        dt_mensaje = datetime.fromtimestamp(timestamp_mensaje)

        self.actualizar_mensajes_por_dia(autor_mensaje, dt_mensaje)
        self.actualizar_mensajes_por_hora(autor_mensaje, dt_mensaje)
        self.actualizar_mensajes_por_minuto(autor_mensaje, dt_mensaje)
        self.actualizar_mensajes_por_dia_año(autor_mensaje, dt_mensaje)
        self.actualizar_mensajes_por_dia_semana(autor_mensaje, dt_mensaje)

    def obtener_series_tiempo(self):
        """ Genera un diccionario con las series de tiempo de cada participante
            de la conversación en forma de Series de pandas.
        """

        series = {}

        for autor in self.series_tiempo:
            series[autor] = {}

            series[autor]["mensajes_por_dia"] = pd.Series(
                self.series_tiempo[autor]["mensajes_por_dia"])

            series[autor]["mensajes_por_hora"] = pd.Series(
                self.series_tiempo[autor]["mensajes_por_hora"])

            series[autor]["mensajes_por_minuto"] = pd.Series(
                self.series_tiempo[autor]["mensajes_por_minuto"])

            series[autor]["mensajes_por_dia_año"] = pd.Series(
                self.series_tiempo[autor]["mensajes_por_dia_año"])

            series[autor]["mensajes_por_dia_semana"] = pd.Series(
                self.series_tiempo[autor]["mensajes_por_dia_semana"])

        return series
