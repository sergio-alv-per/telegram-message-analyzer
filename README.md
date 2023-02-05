# 💬 Telegram Message Analyzer 

Programa escrito en Python para el análisis de conversaciones en Telegram. Utilizando esta herramienta podrás obtener diversos datos y gráficas sobre una conversación.

## ✨ Características
### 📝 Datos generados 
- Recuento de mensajes escritos en total y por persona.
- Recuento de archivos multimedia enviados en total y por persona.
- Recuento de mensajes enviados en cada día.
- Recuento de mensajes enviados en cada día del año.
- Recuento de mensajes enviados en cada día de la semana.
- Recuento de mensajes enviados en cada minuto del día.
- Frecuencia de uso de palabras.
- Palabras más utilizadas por una persona respecto a la otra.
- Tiempo total de notas de voz y notas de vídeo enviadas.

### 📊 Visualizaciones de los datos 
- Comparación entre el número de mensajes, fotos, vídeos, etc. enviados por cada persona.
- Visualización del número de mensajes enviados cada día, desde el inicio de la conversación.
- Visualización del número de mensajes enviados en cada día de la semana, cada día del año, cada hora del día y cada minuto del día.
- Visualización de las palabras más utilizadas por cada participante en la conversación respecto al otro.

## 🧑‍💻 Instalación y uso
1. Descargar el repositorio: `git clone https://github.com/sergio-alv-per/telegram-message-analyzer.git`
2. Obtener un archivo JSON con los datos de la conversación que se quiere analizar.
3. Ejecutar `main.py`, especificando el archivo dado por Telegram. Por ejemplo: `python main.py result.json`

### 📃 Obtención de un archivo con los datos de conversación
Para obtener un archivo JSON procesable por el programa es necesario usar [Telegram Desktop](https://desktop.telegram.org/).

1. Acceder a la conversación que se quiere analizar.
2. Hacer click en los tres puntos, y seleccionar **Exportar chat**.
3. En formato, seleccionar **JSON**. No es necesario incluir fotos u otras formas de contenido multimedia.
4. Hacer click en **Exportar**.

## ➕ Posibles mejoras
- Análisis de sentimiento de los mensajes usando NLTK o Spacy.
- Mejora del procesado del texto, actualmente el análisis es bastante limitado.
- Mejora de los métodos de visualización de los resultados.