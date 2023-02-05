from CalculadoraTfIdf import CalculadoraTfIdf


def analizar_datos_conversacion(datos_conversacion):
    """ Analiza los datos obtenidos de la conversación para obtener métricas,
        como el TF-IDF de las palabras utilizadas.
    """

    calculadora_tf_idf = CalculadoraTfIdf(datos_conversacion["frecuencia_palabras"])

    return {"tf_idf_palabras": calculadora_tf_idf.analisis_tf_idf_palabras()}
