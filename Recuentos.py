from collections import Counter, defaultdict


class Recuentos():
    """Clase que contiene datos de la conversación en forma de recuentos
       (número de mensajes, número de fotos, etc.)."""

    def __init__(self):
        self.recuentos_mensajes = defaultdict(lambda: Counter())
    
    def actualizar_numero_mensajes(self, autor_mensaje, mensaje):
        self.recuentos_mensajes[autor_mensaje]["num_mensajes"] += 1
    
    def actualizar_numero_fotos(self, autor_mensaje, mensaje):
        if "photo" in mensaje:
            self.recuentos_mensajes[autor_mensaje]["num_fotos"] += 1
    
    def actualizar_numero_multimedia(self, autor_mensaje, mensaje):
        """ Actualiza los recuentos en el caso de que el mensaje sea contenido
            multimedia (videos, stickers, notas de voz o de vídeo).
        """
        recuentos_autor_mensaje = self.recuentos_mensajes[autor_mensaje]

        if "media_type" in mensaje:
            if mensaje["media_type"] == "video_file":
                recuentos_autor_mensaje["num_videos"] += 1
            elif mensaje["media_type"] == "sticker":
                recuentos_autor_mensaje["num_stickers"] += 1
            elif mensaje["media_type"] == "voice_message":
                recuentos_autor_mensaje["num_notas_voz"] += 1
                recuentos_autor_mensaje["duracion_notas_voz"] += mensaje["duration_seconds"]
            elif mensaje["media_type"] == "video_message":
                recuentos_autor_mensaje["num_notas_video"] += 1
                recuentos_autor_mensaje["duracion_notas_video"] += mensaje["duration_seconds"]

    def añadir_mensaje(self, mensaje):
        autor_mensaje = mensaje["from"]

        self.actualizar_numero_mensajes(autor_mensaje, mensaje)
        self.actualizar_numero_fotos(autor_mensaje, mensaje)
        self.actualizar_numero_multimedia(autor_mensaje, mensaje)

    def obtener_recuentos(self):
        """ Devuelve un diccionario con los recuentos de cada participante."""

        return self.recuentos_mensajes
