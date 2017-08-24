# tweetometro

Ejecución de twitter_streaming-jp.py:

> $ python twitter_streaming-jp.py

Se escribe automáticamente en el directorio tweets_chile_jp.

En Windows: cambiar mapa de carácteres de la consola (DOS o PowerShell):

> chcp 65001

Luego ejecutar el script:

> python twitter\_streaming-jp.py

El directorio tweets\_nyctsubway debe existir antes de ejecutar el script.

El script actualizar\_csv.py toma los tweets nuevos encontrados en tweets\_nyctsubway/bruto y los agrega al archivo del dataset tweets\_nyctsubway.csv con el formato correcto. Notar que la columna 'topico' del archivo CSV del dataset queda en blanco al momento de realizar la actualización, por lo que es necesario realizar la extracción de tópicos cada vez que se actualice el dataset.

Para extraer tópicos y asignar cada tweet a uno de ellos (a.k.a.: completar la columna 'topico' del archivo CSV del dataset) se debe ejecutar el script extractor\_topicos.py.

Una vez asignado un tópico a cada tweet, es posible obtener una visualización del dataset con la técnica t-SNE, ejecutar visualizador.py. El tiempo de ejecución es largo.
