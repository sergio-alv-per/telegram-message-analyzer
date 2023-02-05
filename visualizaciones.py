import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import pandas as pd
import locale

COLOR_FONDO = "#F5F0F6"
COLOR_EMISOR_1 = "#385F71"
COLOR_EMISOR_2 = "#D7B377"
COLOR_TOTALES = "#90323D"


def generar_visualizaciones(datos_conversacion, analisis_conversacion, directorio="visualizaciones"):

    crear_directorio_si_no_existe(directorio)

    # Necesario para que las fechas se muestren en español
    establecer_idioma_es()

    recuentos_mensajes = datos_conversacion["recuentos_mensajes"]
    series_tiempo = datos_conversacion["series_tiempo"]
    tf_idf_palabras = analisis_conversacion["tf_idf_palabras"]

    generar_grafica_recuentos_mensajes(recuentos_mensajes, directorio)

    generar_grafica_mensajes_dia(series_tiempo, directorio)

    generar_grafica_mensajes_dia_año(series_tiempo, directorio)

    generar_grafica_mensajes_dia_semana(series_tiempo, directorio)

    generar_grafica_mensajes_hora(series_tiempo, directorio)

    generar_grafica_mensajes_minuto(series_tiempo, directorio)

    generar_grafica_tf_idf(tf_idf_palabras, directorio)


def crear_directorio_si_no_existe(directorio):
    if not os.path.exists(directorio):
        os.makedirs(directorio)


def establecer_idioma_es():
    locale.setlocale(locale.LC_ALL, "es_ES.UTF-8")

def guardar_grafica(fig, nombre_archivo, directorio, dpi=150):
    archivo = os.path.join(directorio, nombre_archivo)
    fig.savefig(archivo, dpi=dpi)
    plt.close(fig)

def configurar_grafica(tamaño, titulo, filas=1, columnas=1, color_fondo=COLOR_FONDO):
    fig, ax = plt.subplots(nrows=filas, ncols=columnas, figsize=tamaño)
    fig.suptitle(titulo)
    fig.set_facecolor(color_fondo)

    if filas == 1 and columnas == 1:
        ax.set_facecolor(color_fondo)
    else:
        for a in ax:
            a.set_facecolor(color_fondo)
    
    return fig, ax

def generar_grafica_recuentos_mensajes(recuentos_mensajes, directorio):
    """ Se genera una gráfica que representa, para cada valor del que se ha hecho recuento,
    la proporción del valor asociada a cada emisor."""

    emisor_1, emisor_2 = recuentos_mensajes.keys()

    fig, axs = configurar_grafica((6,7), f"Recuentos: {emisor_1} y {emisor_2}", filas=8)    

    # Generar los subgráficos para las 8 barras
    fig, axs = plt.subplots(8, 1, figsize=(6, 7))

    # Incrementar el espacio entre los subgráficos
    fig.subplots_adjust(hspace=2)


    titulos = ["Mensajes", "Imágenes", "Vídeos", "Stickers", "Notas de voz",
               "Duración de notas de voz", "Notas de vídeo", "Duración de notas de vídeo"]
    atributos = ["num_mensajes", "num_fotos", "num_videos", "num_stickers",
                 "num_notas_voz", "duracion_notas_voz", "num_notas_video", "duracion_notas_video"]

    # Generar las 8 gráficas de barras
    for titulo, atributo, ax in zip(titulos, atributos, axs):
        ax.set_title(titulo)
        generar_subplot_barras_horizontales(ax, recuentos_mensajes, atributo)

    guardar_grafica(fig, "recuentos.png", directorio)


def generar_subplot_barras_horizontales(ax, recuentos_mensajes, atributo):
    """ Genera un subplot de barras horizontales para un atributo de los mensajes. """
    emisor_1, emisor_2 = recuentos_mensajes.keys()

    total = recuentos_mensajes[emisor_1][atributo] + \
        recuentos_mensajes[emisor_2][atributo]

    proporcion_1 = recuentos_mensajes[emisor_1][atributo]/total
    proporcion_2 = recuentos_mensajes[emisor_2][atributo]/total

    # Ocultar los ejes
    ax.axis("off")

    # Representar las barras
    ax.barh(atributo, proporcion_1, color=COLOR_EMISOR_1)
    ax.barh(atributo, proporcion_2, left=proporcion_1, color=COLOR_EMISOR_2)

    # Etiquetas en las barras
    ax.text(
        0, -1, f"{recuentos_mensajes[emisor_1][atributo]} ({100*proporcion_1:.2f}%)")
    ax.text(
        1, -1, f"{recuentos_mensajes[emisor_2][atributo]} ({100*proporcion_2:.2f}%)", ha="right")
    ax.text(1.01, 0, total, ha="left", va="center")


def generar_grafica_mensajes_dia_semana(series_tiempo, directorio):
    """ Genera un gráfico de barras con el número de mensajes enviados en cada día de la semana. """

    emisor_1, emisor_2 = series_tiempo.keys()

    fig, ax = configurar_grafica((6, 3), f"Mensajes por día de la semana: {emisor_1} y {emisor_2}")

    # Ocultar los ejes
    ax.spines[:].set_visible(False)

    # Generar las barras
    dias_semana = ["Lunes", "Martes", "Miércoles",
                   "Jueves", "Viernes", "Sábado", "Domingo"]
    ax.bar(dias_semana, series_tiempo[emisor_1]
           ["mensajes_por_dia_semana"].values, color=COLOR_EMISOR_1)
    ax.bar(dias_semana, series_tiempo[emisor_2]["mensajes_por_dia_semana"].values,
           bottom=series_tiempo[emisor_1]["mensajes_por_dia_semana"].values, color=COLOR_EMISOR_2)

    guardar_grafica(fig, "mensajes_dia_semana.png", directorio)


def generar_grafica_mensajes_dia(series_tiempo, directorio, numero_dias=7):
    """ Genera un gráfico con una línea marcando el número de mensajes total
        enviados por ambos emisores de media los últimos numero_dias días.
    """
    emisor_1, emisor_2 = series_tiempo.keys()
    fig, ax = configurar_grafica((9, 4), f"Mensajes por día (media {numero_dias} días): {emisor_1} y {emisor_2}")

    mensajes_totales = series_tiempo[emisor_1]["mensajes_por_dia"].add(
        series_tiempo[emisor_2]["mensajes_por_dia"], fill_value=0)
    media_movimiento = mensajes_totales.rolling(numero_dias).mean()
    ax.plot(media_movimiento, color=COLOR_TOTALES)

    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=(4, 10)))

    ax.xaxis.set_major_formatter(
        mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))

    guardar_grafica(fig, "mensajes_dia.png", directorio)


def generar_grafica_mensajes_dia_año(series_tiempo, directorio):
    """Genera un gráfico con una línea marcando el número de mensajes total en un día del año."""
    emisor_1, emisor_2 = series_tiempo.keys()

    fig, ax = configurar_grafica((9, 4), f"Mensajes por día del año: {emisor_1} y {emisor_2}")

    mensajes_totales = series_tiempo[emisor_1]["mensajes_por_dia_año"].add(
        series_tiempo[emisor_2]["mensajes_por_dia_año"], fill_value=0)
    mensajes_totales.index = pd.to_datetime(
        mensajes_totales.index, format="%j")
    ax.plot(mensajes_totales, color=COLOR_TOTALES)

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    for label in ax.get_xticklabels(which='major'):
        label.set(rotation=30, horizontalalignment='right')

    guardar_grafica(fig, "mensajes_dia_año.png", directorio)


def generar_grafica_mensajes_hora(series_tiempo, directorio):
    """ Genera un gráfico de barras con el número de mensajes enviados en cada hora del día. """
    
    emisor_1, emisor_2 = series_tiempo.keys()

    fig, ax = configurar_grafica((10, 4), f"Mensajes por hora del día: {emisor_1} y {emisor_2}")

    fig.subplots_adjust(right=1, left=0.08, bottom=0.125)

    # Ocultar los ejes
    ax.spines[:].set_visible(False)

    # Generar las barras
    mensajes_totales = series_tiempo[emisor_1]["mensajes_por_hora"].add(
        series_tiempo[emisor_2]["mensajes_por_hora"], fill_value=0)
    mensajes_totales.index = pd.to_datetime(
        mensajes_totales.index, format="%H").strftime("%H:%M")
    ax.bar(mensajes_totales.index, mensajes_totales.values, color=COLOR_TOTALES)

    for label in ax.get_xticklabels():
        label.set(rotation=30, horizontalalignment='right')

    guardar_grafica(fig, "mensajes_hora.png", directorio)


def generar_grafica_mensajes_minuto(series_tiempo, directorio):
    """ Genera una línea con el número de mensajes enviados en cada minuto del día. """

    emisor_1, emisor_2 = series_tiempo.keys()
    
    fig, ax = configurar_grafica((12, 4), f"Mensajes por minuto del día: {emisor_1} y {emisor_2}")

    fig.subplots_adjust(right=0.99, left=0.05, bottom=0.125)
    ax.autoscale(enable=True, axis='x', tight=True)

    # Generar las barras
    mensajes_totales = series_tiempo[emisor_1]["mensajes_por_minuto"].add(
        series_tiempo[emisor_2]["mensajes_por_minuto"], fill_value=0)
    mensajes_totales.index = pd.to_datetime(
        mensajes_totales.index, format="%H:%M:%S")
    ax.plot(mensajes_totales, color=COLOR_TOTALES)

    ax.xaxis.set_major_locator(mdates.HourLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.xaxis.set_minor_locator(mdates.MinuteLocator(byminute=(0, 30)))

    for label in ax.get_xticklabels(which='major'):
        label.set(rotation=30, horizontalalignment='right')

    guardar_grafica(fig, "mensajes_minuto.png", directorio)


def generar_grafica_tf_idf(tf_idf, directorio, num_por_emisor=5):
    """ Genera un gráfico representando el TF-IDF de las palabras más utilizadas por cada emisor."""

    tf_idf.sort_values("Diferencia", inplace=True)

    minimos = tf_idf.iloc[:num_por_emisor].loc[:, "Diferencia"]
    maximos = tf_idf.iloc[-num_por_emisor:].loc[:, "Diferencia"]

    mas_relevantes = pd.concat([minimos, maximos])

    fig, axs = plt.subplots(2*num_por_emisor, 1, figsize=(7, 6))

    fig.subplots_adjust(right=0.8, left=0.2)

    fig.set_facecolor(COLOR_FONDO)

    emisor_1, emisor_2 = tf_idf.columns[:2]
    fig.suptitle(f"Palabras más utilizadas: {emisor_1} y {emisor_2}")

    for i, ax in enumerate(axs):
        ax.set_facecolor(COLOR_FONDO)
        ax.set_xlim(-1.05, 1.05)
        ax.axis("off")

        if i < num_por_emisor:
            lado = -1
            direccion = "right"
        else:
            lado = 1
            direccion = "left"

        ax.text(lado*1.05, 1, str(mas_relevantes.index[i]), ha=direccion,
                va="center", fontsize=12, fontname="Segoe UI Emoji")

        ax.hlines(1, -1, 1, color="black", linewidth=1)
        ax.vlines(0, 0.7, 1.3, linestyles="dashed",
                  color="black", linewidth=0.5)
        ax.eventplot([mas_relevantes.iloc[i]],
                     color=COLOR_TOTALES, linelength=0.3, linewidths=4)

    guardar_grafica(fig, "palabras.png", directorio)
