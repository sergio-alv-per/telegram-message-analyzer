from collections import Counter, defaultdict
import pandas as pd

class TextoMensajes():
    """ Clase para almacenar la frecuencia de uso de las palabras y los textos de los mensajes."""
    
    def __init__(self):
        self.frecuencia_palabras = defaultdict(lambda: Counter())
        self.texto_mensajes = defaultdict(lambda: [])
    
    def quitar_caracteres_especiales(self, texto):
        return texto.translate({ord(i): None for i in '¡!¿?.,;:"\n\'()[]{}'})
    
    def obtener_texto_mensaje(self, mensaje):
        """ Procesa el campo "text" de un mensaje. Este campo puede ser un string o una lista de strings y diccionarios.
            Los diccionarios representan texto de tipo especial (negrita, cursiva, links, etc.).
            Solo se procesa el texto especial de tipo negrita y cursiva, el resto se descarta.
        """

        texto = ""
        tipos_especiales_texto_aceptados = {"italic", "bold"}

        if type(mensaje["text"]) == str:
            texto = mensaje["text"]
        else:
            for t in mensaje["text"]:
                if type(t) == str:
                    texto += t
                else:
                    if t["type"] in tipos_especiales_texto_aceptados:
                        texto += t["text"]

        return texto
    
    def añadir_mensaje(self, mensaje):
        """ Actualiza los valores de la lista de mensaje y la frecuencia de uso de las palabras."""
        
        autor_mensaje = mensaje["from"]

        texto = self.obtener_texto_mensaje(mensaje)

        # Si el mensaje no tenía texto (por ejemplo, era un sticker), se ignora
        if texto:
            # Se pasa el texto a minúsculas para "nomalizarlo"
            texto = texto.lower()

            self.texto_mensajes[autor_mensaje].append(texto)

            palabras = texto.split()

            for palabra in palabras:
                palabra = self.quitar_caracteres_especiales(palabra)
                self.frecuencia_palabras[autor_mensaje][palabra] += 1

    def obtener_frecuencia_palabras(self):
        """ Genera un diccionario con la frecuencia de uso de las palabras.
            Cada elemento del diccionario se corresponde a un participante en la conversación.
            Cada participante tiene asociado un DataFrame con la frecuencia de uso de las palabras.
        """

        datos_frecuencia_palabras = {}

        for autor_mensaje, frecuencia_palabras in self.frecuencia_palabras.items():
            df_frecuencias = pd.DataFrame.from_dict(frecuencia_palabras, orient="index", columns=["Frecuencia"])
            datos_frecuencia_palabras[autor_mensaje] = df_frecuencias

        return datos_frecuencia_palabras

    def obtener_lista_mensajes(self):
        """ Devuelve un diccionario con la lista de mensjaes (en forma de texto) de cada participante. """
        
        return self.texto_mensajes
