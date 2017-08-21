import os
import pandas as pd
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# Paquetes para formato de fecha y hora
from datetime import datetime
import pytz

# función que cambia el formato de fecha a entero
def formatear_fecha(fecha_tweet):
    d=datetime.strptime(fecha_tweet,'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
    anno = d.year*10000000000
    mes = d.month*100000000
    dia = d.day*1000000
    hora = d.hour*10000
    minuto = d.minute*100
    segundo = d.second
    return anno+mes+dia+hora+minuto+segundo

tweets_bruto = sorted(os.listdir('tweets_nyctsubway/bruto'))
print('Hay', len(tweets_bruto), 'tweets en bruto.')
read_df = None
if os.path.isfile('tweets_nyctsubway.csv'):
    print('\n\n\n*Encontrado archivo CSV de tweets*\n\n\n')
    read_df = pd.read_csv('tweets_nyctsubway.csv', encoding ='latin1', usecols=['id'], squeeze=True).values
    print('Hay', len(read_df), 'tweets en el CSV.')
else:
    print('\n\n\n*No hay archivo CSV de tweets*\n\n\n')
# Escribir tweets nuevos ubicados en tweets_nyctsubway/bruto a archivo csv
sid = SentimentIntensityAnalyzer()
tuits = []
ya_guardados = 0
nuevos_guardados = 0
for archivo_tuit in tweets_bruto:
    if read_df is not None:
        if int(archivo_tuit[:-7]) in read_df:
            ya_guardados += 1
            continue

    nuevos_guardados += 1
    with open(os.getcwd()+'\\tweets_nyctsubway\\bruto\\'+archivo_tuit, 'rb') as f:
        dicc= {}
        for linea in f:
            try:
                dicc = eval(linea) # <--- se interpreta o evalúa archivo de texto como diccionario de python
            except:
                print('Error:', archivo_tuit, ': archivo corrupto')
        if dicc == {}:
            continue # <--- saltar archivos que por alguna razon no pueden leerse (son pocos)

    # Quitar URLs con regex
    dicc['text'] = re.sub(r'https?:\/\/.*[\r\n]*', '', dicc['text'], flags=re.MULTILINE)
    if (ya_guardados + nuevos_guardados)%100 == 0:
        print('Leidos', ya_guardados + nuevos_guardados, 'tweets')
        print(str(dicc['text']).encode('utf8'))

    # Sent. Analysis sobre tweet
    ss = sid.polarity_scores(dicc['text'])
    tuits.append([
        int(archivo_tuit[:-7]), # Parte numerica del nombre del archivo de origen (Ej.: 880040485041168384) menos los tres ultimos digitos, ya que con el resto es suficiente para diferenciar
        '', # Topico del tweet (se debe determinar en conjunto con todos los tweets una vez leidos, por eso se deja vacio)
        formatear_fecha(dicc['created_at']),
        ss['compound'],
        ss['neg'],
        ss['neu'],
        ss['pos'],
        dicc['text']
    ])

# Generar archivo CSV/añadir al existente
if len(tuits) > 0:
    write_df = pd.DataFrame(tuits, columns=['id','topico','fecha','comp','neg','neu','pos','texto'])
    if not os.path.isfile('tweets_nyctsubway.csv'):
        write_df.to_csv('tweets_nyctsubway.csv', index=False)
    else:
        with open('tweets_nyctsubway.csv', 'a') as f:
            write_df.to_csv(f, index=False, header=False)
print('Agregados', nuevos_guardados, 'nuevos tweets al archivo tweets_nyctsubway.csv; ya se habian guardado', ya_guardados)
