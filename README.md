# tweetometro

Ejecución de twitter_streaming-jp.py:

> $ python twitter_streaming-jp.py

Se escribe automáticamente en el directorio tweets_chile_jp.

En Windows:

Cambiar mapa de carácteres de la consola (DOS o PowerShell):

> chcp 65001

Luego ejecutar el script:

> python twitter\_streaming-jp.py

El directorio tweets\_nyctsubway debe existir antes de ejecutar el script.

El script 'indexador.py' toma los tweets almacenados en tweets\_nyctsubway/bruto, y por cada tweet realiza lo siguiente:

> 1. Quita las URLs del cuerpo del tweet
>
> 2. Realiza Sent. Analysis con Vader de NLTK para obtener 4 indicadores de polaridad: compound, neg, neu, pos.
>
> 3. Indexa el tweet en la instancia local de Elasticsearch. El servicio Elastic debe estar ejecutándose en localhost:9200.

Al finalizar, el script genera el vocabulario de los tweets un archivo llamado 'vocabulario.pickle'. Para cargarlo,
revisar el código al fondo del script.
