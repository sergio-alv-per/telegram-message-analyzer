import matplotlib as mpl
import matplotlib.pyplot as plt
import os

COLOR_FONDO = "#F5F0F6"
COLOR_EMISOR_1 = "#385F71"
COLOR_EMISOR_2 = "#D7B377"
COLOR_TOTALES = "#90323D"


def generar_visualizaciones(datos_conversacion, analisis_conversacion, directorio="visualizaciones"):

    # Crear el directorio si no existe
    if not os.path.exists(directorio):
        os.makedirs(directorio)
    
    generar_grafica_recuentos_mensajes(datos_conversacion["recuentos_mensajes"], directorio)
    generar_grafica_mensajes_dia(datos_conversacion["series_tiempo"], directorio)
    generar_grafica_mensajes_dia_año(datos_conversacion["series_tiempo"], directorio)
    generar_grafica_mensajes_dia_semana(datos_conversacion["series_tiempo"], directorio)
    generar_grafica_mensajes_hora(datos_conversacion["series_tiempo"], directorio)
    generar_grafica_mensajes_minuto(datos_conversacion["series_tiempo"], directorio)


    plt.show()

def generar_grafica_recuentos_mensajes(recuentos_mensajes, directorio):
    """ Se genera una gráfica que representa, para cada valor del que se ha hecho recuento,
    la proporción del valor asociada a cada emisor."""

    # Generar los subgráficos para las 8 barras
    fig, axs = plt.subplots(8, 1, figsize=(6, 7))

    # Incrementar el espacio entre los subgráficos
    fig.subplots_adjust(hspace=2)

    fig.set_facecolor(COLOR_FONDO)
    
    emisor_1, emisor_2 = recuentos_mensajes.keys()
    fig.suptitle(f"Recuentos: {emisor_1} y {emisor_2}")

    titulos = ["Mensajes", "Imágenes", "Vídeos", "Stickers", "Notas de voz", "Duración de notas de voz", "Noats de vídeo", "Duración de notas de vídeo"]
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
    ax.barh(atributo, proporcion_1, color=COLOR_EMISOR_1)
    ax.barh(atributo, proporcion_2, left=proporcion_1, color=COLOR_EMISOR_2)

    # Etiquetas en las barras
    ax.text(0, -1, f"{recuentos_mensajes[emisor_1][atributo]} ({100*proporcion_1:.2f}%)")
    ax.text(1, -1, f"{recuentos_mensajes[emisor_2][atributo]} ({100*proporcion_2:.2f}%)", ha="right")
    ax.text(1.01, 0, total, ha="left", va="center")

def generar_grafica_mensajes_dia_semana(series_tiempo, directorio):
    """ Genera un gráfico de barras con el número de mensajes enviados en cada día de la semana. """
    fig, ax = plt.subplots(figsize=(6, 3))

    fig.set_facecolor(COLOR_FONDO)
    ax.set_facecolor(COLOR_FONDO)

    emisor_1, emisor_2 = series_tiempo.keys() 
    ax.set_title(f"Mensajes por día de la semana: {emisor_1} y {emisor_2}")

    # Ocultar los ejes
    ax.spines[:].set_visible(False)

    emisor_1, emisor_2 = series_tiempo.keys()

    # Generar las barras
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    ax.bar(dias_semana, series_tiempo[emisor_1]["mensajes_por_dia_semana"].values, color=COLOR_EMISOR_1)
    ax.bar(dias_semana, series_tiempo[emisor_2]["mensajes_por_dia_semana"].values, bottom=series_tiempo[emisor_1]["mensajes_por_dia_semana"].values, color=COLOR_EMISOR_2)

    archivo = os.path.join(directorio, "mensajes_dia_semana.png")
    fig.savefig(archivo, dpi=150)

def generar_grafica_mensajes_dia(series_tiempo, directorio, numero_dias=7):
    """ Genera un gráfico con una línea marcando el número de mensajes total
        enviados por ambos emisores de media los últimos numero_dias días.
    """
    fig, ax = plt.subplots(figsize=(6, 4))

    fig.set_facecolor(COLOR_FONDO)
    ax.set_facecolor(COLOR_FONDO)

    fig.subplots_adjust(bottom=0.23)

    emisor_1, emisor_2 = series_tiempo.keys() 
    ax.set_title(f"Mensajes por día (media {numero_dias} días): {emisor_1} y {emisor_2}")

    mensajes_totales = series_tiempo[emisor_1]["mensajes_por_dia"].add(series_tiempo[emisor_2]["mensajes_por_dia"], fill_value=0)
    media_movimiento = mensajes_totales.rolling(numero_dias).mean()
    ax.plot(media_movimiento, color=COLOR_TOTALES)

    ax.tick_params(axis='x', rotation=45)

    archivo = os.path.join(directorio, "mensajes_dia.png")
    fig.savefig(archivo, dpi=150)

def generar_grafica_mensajes_dia_año(series_tiempo, directorio):
    pass

def generar_grafica_mensajes_hora(series_tiempo, directorio):
    pass

def generar_grafica_mensajes_minuto(series_tiempo, directorio):
    pass