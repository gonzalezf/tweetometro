import os
import re
from elasticsearch import Elasticsearch
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Paquetes para formato de fecha y hora
from datetime import datetime
import pytz

# función que cambia el formato de fecha y hora a uno admitido por Elastic
def formatear_fecha(fecha_tweet):
    d=datetime.strptime(fecha_tweet,'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
    mes = str(d.month)
    dia = str(d.day)
    hora = str(d.hour)
    minuto = str(d.minute)
    segundo = str(d.second)
    for valor in [mes,dia,hora,minuto,segundo]:
        if len(valor) < 2:
            valor = '0'+valor
    return str(d.year)+'/'+mes+'/'+dia+' '+hora+':'+minuto+':'+segundo

# Se asume Elasticsearch>=5.0.0 con su plugin lang-python instalado y corriendo en http://localhost:9200
# Se asume paquetes de Python 'elasticsearch' y 'nltk' instalados
# Requerido Python>=3.0.0 para no tener que cambiar la sintaxis de algunos comandos (mayoria son prints)

es = Elasticsearch()
sid = SentimentIntensityAnalyzer()

# crear indice 'tweetometro' desde cero
if es.indices.exists(index='tweetometro'):
    es.indices.delete(index='tweetometro')

if not es.indices.exists(index='tweetometro'):
    # mapping: modelado de la estructura del documento 'tweet' a indexar en el índice 'tweetometro' (análogo a la definición de una tabla llamada 'tweet' en una BD llamada 'tweetometro')
    # Info sobre mappings: https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html
    mapa_tuit = {
        'mappings': {
            'tweet': {
                'properties': {
                    'autor': {
                        'type': 'keyword',
                        'index': 'not_analyzed',
                    },
                    'fecha': {
                        'type': 'date',
                        'format': 'yyyy/MM/dd HH:mm:ss',
                    },
                    'text': {
                        'type': 'text',
                        'analyzer': 'english',
                    },
                    'polaridad': {
                        'type': 'nested',
                        'properties': {
                            'compound': {'type': 'double'},
                            'neg': {'type': 'double'},
                            'neu': {'type': 'double'},
                            'pos': {'type': 'double'},
                        }
                    }
                }
            }
        }
    }
    es.indices.create(index='tweetometro', body=mapa_tuit)

# Recorrer todos los archivos guardados en el directorio /tweets_nyctsubway/bruto.
# (cada archivo representa un tweet individual y tienen por nombre 'id_tweet.txt')
# 'id_tweet' será usado para identificarlos en Elasticsearch
cantidad_indexada = 0
vocabulario = []
for archivo_tuit in os.listdir('tweets_nyctsubway/bruto'):
    id_tuit = 0
    dicc = {}

    with open(os.getcwd()+'\\tweets_nyctsubway\\bruto\\'+archivo_tuit, 'rb') as f:
        id_tuit = int(archivo_tuit[:-4]) # <--- id del tweet es el nombre del archivo sin el '.txt' y luego formateado a int
        # evita intentar indexar tweets con la misma id
        if es.exists(index='tweetometro', doc_type='tweet', id=id_tuit):
            continue
        for linea in f:
            dicc = {}
            try:
                dicc = eval(linea) # <--- se interpreta o evalúa archivo de texto como diccionario de python
            except:
                print('Error:', archivo_tuit, ': archivo corrupto')
        if dicc == {}:
            continue # <--- saltar archivos que por alguna razon no pueden leerse (son pocos)

    # Quitar URLs con regex antes de meter tweet en Elastic
    texto = re.sub(r'https?:\/\/.*[\r\n]*', '', dicc['text'], flags=re.MULTILINE)

    # Hacer Sentiment Analysis de Vader en el tweet antes de meterlo en Elastic
    ss = sid.polarity_scores(texto)

    # Conversion de fecha: Formato Twitter -> datetime de Python -> formato yyyy/MM/dd HH:mm:ss
    fecha_tuit = formatear_fecha(dicc['created_at'])

    # tweet que finalmente se meterá a Elastic
    tuit = {
        'autor': dicc['user']['id'],
        'fecha': fecha_tuit,
        'text': texto,
        'polaridad' : {
            'compound': ss['compound'],
            'neg': ss['neg'],
            'neu': ss['neu'],
            'pos': ss['pos'],
        },
    }

    # Aplicar 'analyze()' al cuerpo del tweet para hacer proceso de normalización y stemming que Elastic haría de manera interna si lo indexaramos
    # Meter los tokens resultantes a una lista para ir generando el vocabulario  por nuestra cuenta
    res = es.indices.analyze(index='tweetometro', body={'text':texto, 'analyzer':'english'}, format='text')
    for analizado in res['tokens']:
        vocabulario.append(analizado['token'])

    # Aplicar 'index()' para finalmente indexar el tweet en Elastic
    res = es.index(index='tweetometro', doc_type='tweet', id=id_tuit, body=tuit)
    if(res['created']):
        cantidad_indexada += 1
        # Printeo de avance
        print('Indexado:', id_tuit)
        if cantidad_indexada%10 == 0:
            avance = round((100.0*cantidad_indexada)/len(os.listdir('tweets_nyctsubway/bruto')), 2)
            print('Tweets indexados: ', cantidad_indexada, ' - Porcentaje de avance: ', avance, '- Palabras en vocabulario: ', len(set(vocabulario)))

# ---------------------

# Almacenamiento en disco del vocabulario obtenido
# formato: vocabulario = {palabra1: n, palabra2: m, ...}

import pickle
from collections import Counter

cnt = Counter()
for palabra in vocabulario:
    cnt[palabra] += 1

with open('vocabulario.pickle', 'wb') as f:
    pickle.dump(cnt, f)

# Para cargar el diccionario con el vocabulario en la variable 'vocab':
# vocab.most_common(n) entrega un diccionario con las n palabras más comunes en orden descendente
'''
import pickle
with open('vocabulario.pickle', 'rb') as f:
    vocab = pickle.load(f)
'''
