import matplotlib as mpl
import matplotlib.pyplot as plt

def generar_visualizaciones(datos_conversacion, analisis_conversacion, directorio="visualizaciones"):
    generar_grafica_recuentos_mensajes(datos_conversacion["recuentos_mensajes"], directorio)

def generar_subplot_barras_horizontales(ax, recuentos_mensajes, atributo):
    """ Genera un subplot de barras horizontales para un atributo de los mensajes. """
    emisor_1, emisor_2 = recuentos_mensajes.keys()

    total = recuentos_mensajes[emisor_1][atributo] + recuentos_mensajes[emisor_2][atributo]

    proporcion_1 = recuentos_mensajes[emisor_1][atributo]/total
    proporcion_2 = recuentos_mensajes[emisor_2][atributo]/total

    # Hacer que no se vean los ejes ni las etiquetas
    ax.axis("off")

    ax.barh(atributo, proporcion_1, color="blue")
    ax.barh(atributo, proporcion_2, left=proporcion_1, color="red")

    ax.text(0, -1, f"{recuentos_mensajes[emisor_1][atributo]} ({100*proporcion_1:.2f}%)")
    ax.text(1, -1, f"{recuentos_mensajes[emisor_2][atributo]} ({100*proporcion_2:.2f}%)", ha="right")
    ax.text(1, 1, f"{total}")
    
    

def generar_grafica_recuentos_mensajes(recuentos_mensajes, directorio):
    """ Se genera una gráfica que representa, para cada valor del que se ha hecho recuento,
    la proporción del valor asociada a cada emisor."""

    emisor_1, emisor_2 = recuentos_mensajes.keys()

    # Generar los subgráficos para las 8 barras
    fig, (ax_mensajes, ax_fotos,
    ax_videos, ax_stickers, ax_numero_notas_voz,
    ax_duracion_notas_voz, ax_numero_notas_video,
    ax_duracion_notas_video) = plt.subplots(8, 1)

    # Incrementar el espacio entre los subgráficos
    fig.subplots_adjust(hspace=2)    
    
    # TODO Generar subtítulo con los nombres de los emisores
    
    
    # Generar barra para número de mensajes
    ax_mensajes.set_title("Mensajes")
    generar_subplot_barras_horizontales(ax_mensajes, recuentos_mensajes, "num_mensajes")

    # Generar barra para número de fotos
    ax_fotos.set_title("Imágenes")
    generar_subplot_barras_horizontales(ax_fotos, recuentos_mensajes, "num_fotos")

    # Generar barra para número de vídeos
    ax_videos.set_title("Vídeos")
    generar_subplot_barras_horizontales(ax_videos, recuentos_mensajes, "num_videos")

    # Generar barra para número de stickers
    ax_stickers.set_title("Stickers")
    generar_subplot_barras_horizontales(ax_stickers, recuentos_mensajes, "num_stickers")

    # Generar barra para número de notas de voz
    ax_numero_notas_voz.set_title("Notas de voz")
    generar_subplot_barras_horizontales(ax_numero_notas_voz, recuentos_mensajes, "num_notas_voz")

    # Generar barra para tiempo de notas de voz
    ax_duracion_notas_voz.set_title("Duración de notas de voz")
    generar_subplot_barras_horizontales(ax_duracion_notas_voz, recuentos_mensajes, "duracion_notas_voz")

    # Generar barra para número de notas de vídeo
    ax_numero_notas_video.set_title("Notas de vídeo")
    generar_subplot_barras_horizontales(ax_numero_notas_video, recuentos_mensajes, "num_notas_video")

    # Generar barra para tiempo de notas de vídeo
    ax_duracion_notas_video.set_title("Duración de notas de vídeo")
    generar_subplot_barras_horizontales(ax_duracion_notas_video, recuentos_mensajes, "duracion_notas_video")

    plt.show()
