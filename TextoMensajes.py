from collections import Counter, defaultdict
import pandas as pd
import string


class TextoMensajes():
    """ Clase para gestionar la frecuencia de uso de las palabras y los textos
        de los mensajes.
    """

    def __init__(self):
        self.frecuencia_palabras = defaultdict(lambda: Counter())
        self.texto_mensajes = defaultdict(lambda: [])
        self.tabla_traduccion_caracteres_especiales = str.maketrans(
            "", "", string.punctuation)

    def quitar_caracteres_especiales(self, texto):
        return texto.translate(self.tabla_traduccion_caracteres_especiales)

    def texto_mensaje_con_texto_especial(self, mensaje):
        """ Procesa el campo "text" de un mensaje, en el caso de que este
            contenga texto especial. Devuelve el texto del mensaje.
        """
        tipos_especiales_texto_aceptados = {"italic", "bold"}
        texto = []

        for t in mensaje["text"]:
            if type(t) == str:
                texto.append(t)
            else:
                if t["type"] in tipos_especiales_texto_aceptados:
                    texto.append(t["text"])

        return "".join(texto)

    def obtener_texto_mensaje(self, mensaje):
        """ Procesa el campo "text" de un mensaje. Este campo puede ser un
            string o una lista de strings y diccionarios. En este último caso,
            el mensaje contiene texto especial. Devuelve el texto del mensaje.
        """

        if type(mensaje["text"]) == str:
            texto = mensaje["text"]
        else:
            texto = self.texto_mensaje_con_texto_especial(mensaje)

        return texto

    def añadir_mensaje(self, mensaje):
        """ Actualiza los valores de frecuencia de uso de las palabras y el
            texto de los mensajes.
        """

        autor_mensaje = mensaje["from"]

        texto = self.obtener_texto_mensaje(mensaje)

        # Si el mensaje no tenía texto (por ejemplo, era un sticker), se ignora
        if texto:
            # Se pasa el texto a minúsculas para "nomalizarlo"
            texto = texto.lower()

            self.texto_mensajes[autor_mensaje].append(texto)

            palabras_mensaje = texto.split()

            for palabra in palabras_mensaje:
                palabra = self.quitar_caracteres_especiales(palabra)
                self.frecuencia_palabras[autor_mensaje][palabra] += 1

    def obtener_frecuencia_palabras(self):
        """ Genera un diccionario con la frecuencia de uso de las palabras.
            Cada elemento del diccionario se corresponde a un participante en la
            conversación. Cada participante tiene asociado un DataFrame con la
            frecuencia de uso de las palabras.
        """

        datos_frecuencia_palabras = {}

        for autor_mensaje, frecuencia_palabras in self.frecuencia_palabras.items():
            # Se genera un DataFrame para facilitar el tratamiento de los datos
            # Las filas del DataFrame son las palabras y la columna "Frecuencia"
            # contiene la frecuencia de uso de cada palabra
            df_frecuencias = pd.DataFrame.from_dict(
                frecuencia_palabras, orient="index", columns=["Frecuencia"])

            datos_frecuencia_palabras[autor_mensaje] = df_frecuencias

        return datos_frecuencia_palabras

    def obtener_lista_mensajes(self):
        """ Devuelve un diccionario con la lista de mensajes (en forma de texto)
            de cada participante.
        """

        return self.texto_mensajes
