import csv
from pylab import *
import sys

if len(sys.argv) != 4:
    print('Error, ejecucion: python estadisticas.py <topico> <fecha_ini(yyyy-mm-dd)> <fecha_fin(yyyy-mm-dd)>')
    print('Para omitir un parametro dejar el valor \'\'')
    exit()


topico = str(sys.argv[1])   #str(input("ingrese topico: "))
date_ini = str(sys.argv[2])   #str(input("fecha de inicio (yyyy-mm-dd): "))
date_fin = str(sys.argv[3])   #str(input("fecha de fin (yyyy-mm-dd): "))

fecha_ini = int(date_ini.replace("-", "")+'000000')
fecha_fin = int(date_fin.replace("-", "")+'235959')

data_csv = open('tweets_nyctsubway.csv', 'r', encoding='latin1')
data = csv.reader(data_csv, delimiter=';', quotechar='\"')

comp = []
neg = []
neu = []
pos = []

a = 0
for row in data:

    if a == 0:
        a += 1
        continue

    tweet_date = int(row[2])

    if topico != '' and (fecha_fin == '235959' or fecha_ini == "000000"):
        if topico == row[1]:
            comp.append(float(row[3]))
            neg.append(float(row[4]))
            neu.append(float(row[5]))
            pos.append(float(row[6]))

    elif topico != '' and fecha_fin != '235959' and fecha_ini != "000000":
        if topico == row[1] and tweet_date <= fecha_fin and tweet_date >= fecha_ini:
            comp.append(float(row[3]))
            neg.append(float(row[4]))
            neu.append(float(row[5]))
            pos.append(float(row[6]))

    elif topico == '' and fecha_fin != '235959' and fecha_ini != "000000":
        if tweet_date <= fecha_fin and tweet_date >= fecha_ini:
            comp.append(float(row[3]))
            neg.append(float(row[4]))
            neu.append(float(row[5]))
            pos.append(float(row[6]))

if len(pos) == 0:
    print("No hay datos para los parametros usados.")
    exit()
else:
    print('Analizando', len(pos), 'tweets...')
    print('-> Positividad', sum(pos)/len(pos))
    print('-> Negatividad', sum(neg)/len(neg))
    print('-> Polaridad', sum(comp)/len(comp))

tot_pos = sum(pos)
tot_neg = sum(neg)
tot_neu = sum(neu)

ax = axes([0, 0, 0.9, 0.9])
labels = 'Positivos ', 'Negativos', 'Neutros'
fracs = [tot_pos, tot_neg, tot_neu]
pie(fracs, labels=labels, autopct='%10.0f%%', shadow=True)
legend()
title('Estadisticas de tweets', bbox={'facecolor': '0.8', 'pad': 5})
show()
