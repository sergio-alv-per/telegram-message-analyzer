from collections import defaultdict
import pandas as pd
import math


class CalculadoraTfIdf():
    """ Clase que calcula el TF-IDF de las palabras utilizadas en una conversación. """

    def __init__(self, frecuencia_palabras):
        self.frecuencia_palabras = frecuencia_palabras
        self.todas_palabras = self.todas_palabras_conversacion()
        self.total_palabras_emisor = self.total_palabras_por_emisor()
        self.datos_tf_idf = defaultdict(list)

    def todas_palabras_conversacion(self):
        """ Devuelve una lista ordenada con todas las palabras utilizadas en la
            conversación por cualquiera de los participantes.
        """
        todas_palabras = set()

        for emisor in self.frecuencia_palabras:
            todas_palabras.update(
                self.frecuencia_palabras[emisor].index.tolist())

        return sorted(list(todas_palabras))

    def total_palabras_por_emisor(self):
        """ Devuelve un diccionario con el número de palabras utilizadas por cada
            uno de los participantes.
        """
        total_palabras = {}

        for emisor in self.frecuencia_palabras:
            frec_palabras_emisor = self.frecuencia_palabras[emisor]["Frecuencia"]
            total_palabras[emisor] = frec_palabras_emisor.sum()

        return total_palabras

    def tf_idf(self, palabra, emisor):
        return self.tf(palabra, emisor) * self.idf(palabra)

    def tf(self, palabra, emisor,):
        """ Obtiene la frecuencia de uso de una palabra en un emisor."""
        try:
            numero_usos_palabra = self.frecuencia_palabras[emisor].at[palabra, "Frecuencia"]
        except KeyError:
            numero_usos_palabra = 0

        numero_palabras_total_emisor = self.total_palabras_emisor[emisor]

        return numero_usos_palabra / numero_palabras_total_emisor

    def idf(self, palabra):
        """ Obtiene el índice de frecuencia inversa de una palabra. """
        num_conversaciones = len(self.frecuencia_palabras)
        num_conversaciones_donde_aparece_palabra = sum(
            [1 for emisor in self.frecuencia_palabras if palabra in self.frecuencia_palabras[emisor].index])

        return math.log(num_conversaciones / num_conversaciones_donde_aparece_palabra)

    def normalizar_columna_menos_uno_uno(self, df, columna):
        """ Normaliza los valores de una columna de un DataFrame entre -1 y 1.
            Los valores negativos se normalizan entre -1 y 0, y los positivos entre 0 y 1.
        """
        df[columna] = (df[columna] - df[columna].min()) / \
            (df[columna].max() - df[columna].min())
        df[columna] = df[columna] * 2 - 1
        return df

    def generar_df_diferencias_tf_idf(self):
        """ Genera un DataFrame con las diferencias de TF-IDF entre los dos
            emisores, normalizadas entre -1 y 1.
        """
        df_tf_idf = pd.DataFrame(self.datos_tf_idf, index=self.todas_palabras)
        df_tf_idf["Diferencia"] = df_tf_idf.iloc[:, 1] - df_tf_idf.iloc[:, 0]
        df_tf_idf = self.normalizar_columna_menos_uno_uno(df_tf_idf, "Diferencia")

        return df_tf_idf

    def analisis_tf_idf_palabras(self):
        for emisor in self.frecuencia_palabras:
            for palabra in self.todas_palabras:
                self.datos_tf_idf[emisor].append(
                    self.tf_idf(palabra, emisor))

        return self.generar_df_diferencias_tf_idf()
