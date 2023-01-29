from collections import Counter, defaultdict


class Recuentos():
    """Clase que contiene datos de la conversación en forma de recuentos
       (número de mensajes, número de fotos, etc.)."""

    def __init__(self):
        self.recuentos_mensajes = defaultdict(lambda: Counter())

    def añadir_mensaje(self, mensaje):
        autor_mensaje = mensaje["from"]

        # Diccionario de datos del autor del mensaje, se usará repetidamente
        diccionario_recuentos = self.recuentos_mensajes[autor_mensaje]

        diccionario_recuentos["num_mensajes"] += 1

        if "photo" in mensaje:
            diccionario_recuentos["num_fotos"] += 1

        if "media_type" in mensaje:
            if mensaje["media_type"] == "video_file":
                diccionario_recuentos["num_videos"] += 1
            elif mensaje["media_type"] == "sticker":
                diccionario_recuentos["num_stickers"] += 1
            elif mensaje["media_type"] == "voice_message":
                diccionario_recuentos["num_notas_voz"] += 1
                diccionario_recuentos["duracion_notas_voz"] += mensaje["duration_seconds"]
            elif mensaje["media_type"] == "video_message":
                diccionario_recuentos["num_notas_video"] += 1
                diccionario_recuentos["duracion_notas_video"] += mensaje["duration_seconds"]

    def obtener_recuentos(self):
        """ Devuelve un diccionario con los recuentos de cada participante."""

        return self.recuentos_mensajes
