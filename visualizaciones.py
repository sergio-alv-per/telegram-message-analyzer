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


def configuracion_inicial_figura(tamaño, titulo, filas=1, columnas=1, color_fondo=COLOR_FONDO):
    """ Configura la figura y los ejes según los parámetros dados. """

    fig, ax = plt.subplots(nrows=filas, ncols=columnas, figsize=tamaño)

    fig.suptitle(titulo)

    fig.set_facecolor(color_fondo)

    # Se colorea dependiendo de si se genera un solo eje o varios
    if filas == 1 and columnas == 1:
        ax.set_facecolor(color_fondo)
    else:
        for a in ax:
            a.set_facecolor(color_fondo)

    return fig, ax


def generar_grafica_recuentos_mensajes(recuentos_mensajes, directorio):
    """ Se genera una gráfica que representa, para cada valor del que se ha
        hecho recuento, la proporción del valor asociada a cada emisor.
    """

    emisor_1, emisor_2 = recuentos_mensajes.keys()

    titulo = f"Recuentos: {emisor_1} y {emisor_2}"

    fig, axs = configuracion_inicial_figura((6, 7), titulo, filas=8)

    # Configuración adicional específica para la gráfica de recuentos
    fig.subplots_adjust(hspace=2)

    generar_subgraficas_recuentos(axs, recuentos_mensajes)

    guardar_grafica(fig, "recuentos.png", directorio)


def generar_subgraficas_recuentos(axs, recuentos_mensajes):
    """ Genera las 8 subgráficas de la gráfica de recuentos. """
    titulos_subgraficas = ["Mensajes", "Imágenes", "Vídeos", "Stickers", "Notas de voz",
                           "Duración de notas de voz", "Notas de vídeo", "Duración de notas de vídeo"]
    atributos_subgraficas = ["num_mensajes", "num_fotos", "num_videos", "num_stickers",
                             "num_notas_voz", "duracion_notas_voz", "num_notas_video", "duracion_notas_video"]

    for titulo, atributo, ax in zip(titulos_subgraficas, atributos_subgraficas, axs):
        ax.set_title(titulo)
        generar_subgrafica_barras_horizontales(
            ax, recuentos_mensajes, atributo)


def generar_subgrafica_barras_horizontales(ax, recuentos_mensajes, atributo):
    """ Genera un subplot de barras horizontales para un cierto atributo,
        representando la proporción de dicho atributo para cada emisor.
    """

    emisor_1, emisor_2 = recuentos_mensajes.keys()

    total = recuentos_mensajes[emisor_1][atributo] + \
        recuentos_mensajes[emisor_2][atributo]

    proporcion_1 = recuentos_mensajes[emisor_1][atributo]/total
    proporcion_2 = recuentos_mensajes[emisor_2][atributo]/total

    # Se ocultan los ejes ya que no aportan información relevante
    ax.axis("off")

    ax.barh(atributo, proporcion_1, color=COLOR_EMISOR_1)
    ax.barh(atributo, proporcion_2, left=proporcion_1, color=COLOR_EMISOR_2)

    # Etiquetas de la forma "1234 (25.00%)"
    etiqueta_izquierda = f"{recuentos_mensajes[emisor_1][atributo]} ({100*proporcion_1:.2f}%)"
    etiqueta_derecha = f"{recuentos_mensajes[emisor_2][atributo]} ({100*proporcion_2:.2f}%)"

    añadir_etiquetas_subgrafica_barras_horizontales(ax, etiqueta_izquierda, etiqueta_derecha, total)


def añadir_etiquetas_subgrafica_barras_horizontales(ax, izquierda, derecha, total):
    """ Añade las etiquetas dadas como parámetros a la subgráfica de barras
        horizontales de ax.
    """

    ax.text(0, -1, izquierda)
    ax.text(1, -1, derecha, ha="right")
    ax.text(1.01, 0, total, ha="left", va="center")


def generar_grafica_mensajes_dia_semana(series_tiempo, directorio):
    """ Genera un gráfico de barras con el número de mensajes enviados en cada
        día de la semana.
    """

    emisor_1, emisor_2 = series_tiempo.keys()

    titulo = f"Mensajes por día de la semana: {emisor_1} y {emisor_2}"

    fig, ax = configuracion_inicial_figura((6, 3), titulo)

    # Se ocultan las líneas pero se mantienen las marcas de los ejes
    ax.spines[:].set_visible(False)

    dias_semana = ["Lunes", "Martes", "Miércoles",
                   "Jueves", "Viernes", "Sábado", "Domingo"]

    mensajes_totales = series_tiempo[emisor_1]["mensajes_por_dia_semana"].add(
        series_tiempo[emisor_2]["mensajes_por_dia_semana"], fill_value=0)

    ax.bar(dias_semana, mensajes_totales, color=COLOR_TOTALES)

    guardar_grafica(fig, "mensajes_dia_semana.png", directorio)


def configurar_ejes_grafica_mensajes_dia(ax):
    """ Configura los ejes de la gráfica, se muestran marcas grandes cada 6
        meses y pequeñas cada 3 meses.
    """
    marcas_bianuales = mdates.MonthLocator(bymonth=(1, 7))
    marcas_trimestrales = mdates.MonthLocator(bymonth=(4, 10))

    ax.xaxis.set_major_locator(marcas_bianuales)
    ax.xaxis.set_minor_locator(marcas_trimestrales)

    ax.xaxis.set_major_formatter(
        mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))


def generar_grafica_mensajes_dia(series_tiempo, directorio, numero_dias=7):
    """ Genera un gráfico representando la media móvil de los mensajes enviados
        por día. La amplitude de la media móvil está dada por el parámetro
        numero_dias.
    """

    emisor_1, emisor_2 = series_tiempo.keys()

    titulo = f"Mensajes por día (media móvil {numero_dias} días): {emisor_1} y {emisor_2}"

    fig, ax = configuracion_inicial_figura((9, 4), titulo)

    configurar_ejes_grafica_mensajes_dia(ax)

    mensajes_totales = series_tiempo[emisor_1]["mensajes_por_dia"].add(
        series_tiempo[emisor_2]["mensajes_por_dia"], fill_value=0)

    media_movil = mensajes_totales.rolling(numero_dias).mean()

    ax.plot(media_movil, color=COLOR_TOTALES)

    guardar_grafica(fig, "mensajes_dia.png", directorio)


def configurar_marcas_ejes_grafica_mensajes_dia_año(ax):
    """ Configura los ejes de la gráfica, se muestran marcas todos los meses.
        Además se rotan las etiquetas para que no se solapen.
    """

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

    for label in ax.get_xticklabels(which='major'):
        label.set(rotation=30, horizontalalignment='right')


def generar_grafica_mensajes_dia_año(series_tiempo, directorio):
    """Genera un gráfico representando el número de mensajes enviados por día
       del año.
    """

    emisor_1, emisor_2 = series_tiempo.keys()

    titulo = f"Mensajes por día del año: {emisor_1} y {emisor_2}"

    fig, ax = configuracion_inicial_figura((9, 4), titulo)

    configurar_marcas_ejes_grafica_mensajes_dia_año(ax)

    mensajes_totales = series_tiempo[emisor_1]["mensajes_por_dia_año"].add(
        series_tiempo[emisor_2]["mensajes_por_dia_año"], fill_value=0)

    # Se transforma de día del año (1-365) a fecha (objeto datetime) para que
    # matplotlib pueda representar las etiquetas correctamente.
    mensajes_totales.index = pd.to_datetime(
        mensajes_totales.index, format="%j")

    ax.plot(mensajes_totales, color=COLOR_TOTALES)

    guardar_grafica(fig, "mensajes_dia_año.png", directorio)


def generar_grafica_mensajes_hora(series_tiempo, directorio):
    """ Genera un gráfico de barras con el número de mensajes enviados en cada
        hora del día.
    """

    emisor_1, emisor_2 = series_tiempo.keys()

    titulo = f"Mensajes por hora del día: {emisor_1} y {emisor_2}"

    fig, ax = configuracion_inicial_figura((10, 4), titulo)

    configurar_ejes_grafica_mensajes_hora(ax)

    # Configuración adicional de la figura (márgenes)
    fig.subplots_adjust(right=1, left=0.08, bottom=0.125)

    # Ocultar los ejes
    ax.spines[:].set_visible(False)

    mensajes_totales = series_tiempo[emisor_1]["mensajes_por_hora"].add(
        series_tiempo[emisor_2]["mensajes_por_hora"], fill_value=0)

    # Se transforma de hora del día (0-23) a hora (objeto datetime) para que
    # matplotlib pueda representar las etiquetas correctamente.
    mensajes_totales.index = pd.to_datetime(
        mensajes_totales.index, format="%H").strftime("%H:%M")

    ax.bar(mensajes_totales.index, mensajes_totales.values, color=COLOR_TOTALES)

    guardar_grafica(fig, "mensajes_hora.png", directorio)


def configurar_ejes_grafica_mensajes_hora(ax):
    """ Se rotan las etiquetas de los ejes para que no se solapen. """
    for label in ax.get_xticklabels():
        label.set(rotation=30, horizontalalignment='right')


def generar_grafica_mensajes_minuto(series_tiempo, directorio):
    """ Genera una línea con el número de mensajes enviados en cada minuto del día. """

    emisor_1, emisor_2 = series_tiempo.keys()

    titulo = f"Mensajes por minuto del día: {emisor_1} y {emisor_2}"

    fig, ax = configuracion_inicial_figura((12, 4), titulo)

    configurar_ejes_grafica_mensajes_minuto(ax)

    # Configuración adicional de la figura
    fig.subplots_adjust(right=0.99, left=0.05, bottom=0.125)
    # Se ajusta el escalado para que no se muestren valores fuera de los
    # límites, ya que los minutos de un día están acotados (00:00 - 23:59)
    ax.autoscale(enable=True, axis='x', tight=True)

    mensajes_totales = series_tiempo[emisor_1]["mensajes_por_minuto"].add(
        series_tiempo[emisor_2]["mensajes_por_minuto"], fill_value=0)

    mensajes_totales.index = pd.to_datetime(
        mensajes_totales.index, format="%H:%M:%S")

    ax.plot(mensajes_totales, color=COLOR_TOTALES)

    guardar_grafica(fig, "mensajes_minuto.png", directorio)


def configurar_ejes_grafica_mensajes_minuto(ax):
    """ Configura los ejes de la gráfica de mensajes por minuto. Se marcan en
        grande las horas y en pequeño las medias horas. También se rotan las
        etiquetas de las horas para evitar que se solapen.
    """

    ax.xaxis.set_major_locator(mdates.HourLocator())

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    ax.xaxis.set_minor_locator(mdates.MinuteLocator(byminute=(30)))

    for label in ax.get_xticklabels(which='major'):
        label.set(rotation=30, horizontalalignment='right')


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
