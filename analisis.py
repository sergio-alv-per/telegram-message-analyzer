import math
import pandas as pd

def analizar_datos_conversacion(datos_conversacion):
    """ Analiza los datos obtenidos de la conversación para obtener nuevas métricas,
        como el TF-IDF de las palabras utilizadas.
    """
    return {"tf_idf_palabras": analisis_tf_idf_palabras(datos_conversacion["frecuencia_palabras"])}

def analisis_tf_idf_palabras(frecuencia_palabras):
    """ Se analiza el TF-IDF de cada palabra utilizada en la conversación.
        Se tendrán dos documentos, uno por cada emisor.

        El TF-IDF es una medida de la importancia de una palabra en un documento.
    """

    todas_palabras = set()
    for emisor in frecuencia_palabras:
        todas_palabras.update(frecuencia_palabras[emisor].index.tolist())
    
    datos_tf_idf_palabras = pd.DataFrame(index=sorted(list(todas_palabras)))

    for emisor in frecuencia_palabras:
        datos_tf_idf_palabras[emisor] = 0
        for palabra in todas_palabras:
            datos_tf_idf_palabras.loc[palabra, emisor] = tf_idf(palabra, emisor, frecuencia_palabras)
    
    datos_tf_idf_palabras["Diferencia"] = datos_tf_idf_palabras.iloc[:, 0] - datos_tf_idf_palabras.iloc[:, 1]
    return datos_tf_idf_palabras

def tf_idf(palabra, emisor, frecuencia_palabras):
    return tf(palabra, emisor, frecuencia_palabras) * idf(palabra, frecuencia_palabras)

def tf(palabra, emisor, frecuencia_palabras):
    try:
        numero_usos_de_palabra = frecuencia_palabras[emisor].at[palabra, "Frecuencia"]
    except KeyError:
        numero_usos_de_palabra = 0
    
    numero_palabras_total_emisor = frecuencia_palabras[emisor]["Frecuencia"].sum()
    return numero_usos_de_palabra / numero_palabras_total_emisor

def idf(palabra, frecuencia_palabras):
    num_conversaciones = len(frecuencia_palabras)
    num_conversaciones_donde_aparece_palabra = sum([1 for emisor in frecuencia_palabras if palabra in frecuencia_palabras[emisor].index])
    return math.log(num_conversaciones / num_conversaciones_donde_aparece_palabra)