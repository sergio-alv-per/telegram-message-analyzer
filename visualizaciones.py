import matplotlib as mpl
import matplotlib.pyplot as plt
import os

COLOR_FONDO = "#F5F0F6"
COLOR_BARRAS_EMISOR_1 = "#385F71"
COLOR_BARRAS_EMISOR_2 = "#D7B377"

def generar_visualizaciones(datos_conversacion, analisis_conversacion, directorio="visualizaciones"):

    # Crear el directorio si no existe
    if not os.path.exists(directorio):
        os.makedirs(directorio)
    
    generar_grafica_recuentos_mensajes(datos_conversacion["recuentos_mensajes"], directorio)

def generar_subplot_barras_horizontales(ax, recuentos_mensajes, atributo):
    """ Genera un subplot de barras horizontales para un atributo de los mensajes. """
    emisor_1, emisor_2 = recuentos_mensajes.keys()

    total = recuentos_mensajes[emisor_1][atributo] + recuentos_mensajes[emisor_2][atributo]

    proporcion_1 = recuentos_mensajes[emisor_1][atributo]/total
    proporcion_2 = recuentos_mensajes[emisor_2][atributo]/total

    # Oclutar los ejes
    ax.axis("off")

    # Representar las barras
    ax.barh(atributo, proporcion_1, color=COLOR_BARRAS_EMISOR_1)
    ax.barh(atributo, proporcion_2, left=proporcion_1, color=COLOR_BARRAS_EMISOR_2)

    # Etiquetas en las barras
    ax.text(0, -1, f"{recuentos_mensajes[emisor_1][atributo]} ({100*proporcion_1:.2f}%)")
    ax.text(1, -1, f"{recuentos_mensajes[emisor_2][atributo]} ({100*proporcion_2:.2f}%)", ha="right")
    ax.text(1.01, 0, total, ha="left", va="center")    

def generar_grafica_recuentos_mensajes(recuentos_mensajes, directorio):
    """ Se genera una gráfica que representa, para cada valor del que se ha hecho recuento,
    la proporción del valor asociada a cada emisor."""

    # Generar los subgráficos para las 8 barras
    fig, (ax_mensajes, ax_fotos,
    ax_videos, ax_stickers, ax_numero_notas_voz,
    ax_duracion_notas_voz, ax_numero_notas_video,
    ax_duracion_notas_video) = plt.subplots(8, 1, figsize=(6, 7))

    # Incrementar el espacio entre los subgráficos
    fig.subplots_adjust(hspace=2)

    fig.set_facecolor(COLOR_FONDO)
    
    emisor_1, emisor_2 = recuentos_mensajes.keys()
    fig.suptitle(f"Recuentos: {emisor_1} vs {emisor_2}")

    ax_mensajes.set_title("Mensajes")
    generar_subplot_barras_horizontales(ax_mensajes, recuentos_mensajes, "num_mensajes")

    ax_fotos.set_title("Imágenes")
    generar_subplot_barras_horizontales(ax_fotos, recuentos_mensajes, "num_fotos")
    ax_videos.set_title("Vídeos")
    generar_subplot_barras_horizontales(ax_videos, recuentos_mensajes, "num_videos")

    ax_stickers.set_title("Stickers")
    generar_subplot_barras_horizontales(ax_stickers, recuentos_mensajes, "num_stickers")

    ax_numero_notas_voz.set_title("Notas de voz")
    generar_subplot_barras_horizontales(ax_numero_notas_voz, recuentos_mensajes, "num_notas_voz")

    ax_duracion_notas_voz.set_title("Duración de notas de voz")
    generar_subplot_barras_horizontales(ax_duracion_notas_voz, recuentos_mensajes, "duracion_notas_voz")

    ax_numero_notas_video.set_title("Notas de vídeo")
    generar_subplot_barras_horizontales(ax_numero_notas_video, recuentos_mensajes, "num_notas_video")

    ax_duracion_notas_video.set_title("Duración de notas de vídeo")
    generar_subplot_barras_horizontales(ax_duracion_notas_video, recuentos_mensajes, "duracion_notas_video")

    archivo = os.path.join(directorio, "recuentos.png")
    fig.savefig(archivo, dpi=150)
