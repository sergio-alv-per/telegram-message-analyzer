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

def generar_grafica_recuentos_mensajes(recuentos_mensajes, directorio):
    """ Se genera una gráfica que representa, para cada valor del que se ha hecho recuento,
    la proporción del valor asociada a cada emisor."""

    # Generar los subgráficos para las 8 barras
    fig, axs = plt.subplots(8, 1, figsize=(6, 7))

    # Incrementar el espacio entre los subgráficos
    fig.subplots_adjust(hspace=2)

    fig.set_facecolor(COLOR_FONDO)
    
    emisor_1, emisor_2 = recuentos_mensajes.keys()
    fig.suptitle(f"Recuentos: {emisor_1} vs {emisor_2}")

    titulos = ["Mensajes", "Imágenes", "Vídeos", "Stickers", "Notas de voz", "Duración de notas de voz", "Noas de vídeo", "Duración de notas de vídeo"]
    atributos = ["num_mensajes", "num_fotos", "num_videos", "num_stickers", "num_notas_voz", "duracion_notas_voz", "num_notas_video", "duracion_notas_video"]

    # Generar las 8 gráficas de barras
    for titulo, atributo, ax in zip(titulos, atributos, axs):
        ax.set_title(titulo)
        generar_subplot_barras_horizontales(ax, recuentos_mensajes, atributo)

    archivo = os.path.join(directorio, "recuentos.png")
    fig.savefig(archivo, dpi=150)

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