from Recuentos import Recuentos
from SeriesTiempo import SeriesTiempo
from TextoMensajes import TextoMensajes

class ProcesadorMensajes():
    
    def __init__(self, lista_mensajes):
        self.lista_mensajes = lista_mensajes
        self.series_tiempo = SeriesTiempo()
        self.texto_mensajes = TextoMensajes()
        self.recuentos = Recuentos()

    
    def procesar_mensajes(self):
        for mensaje in self.lista_mensajes:
            self.series_tiempo.añadir_mensaje(mensaje)

            self.texto_mensajes.añadir_mensaje(mensaje)

            self.recuentos.añadir_mensaje(mensaje)
        
        return {"recuentos_mensajes": self.recuentos.obtener_recuentos(),
                "series_tiempo": self.series_tiempo.obtener_series_tiempo(),
                "frecuencia_palabras": self.texto_mensajes.obtener_frecuencia_palabras(),
                "texto_mensajes": self.texto_mensajes.obtener_lista_mensajes()}