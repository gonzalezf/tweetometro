import csv
import matplotlib.pyplot as plt
import numpy as np

data_csv = open('tweets_nyctsubway.csv', 'r', encoding='latin1')
data = csv.reader(data_csv, delimiter=';', quotechar='\"')

comp = {}
neg = {}
neu = {}
pos = {}

a = 0
for row in data:

    if a == 0:
        a += 1
        continue

    if row[1] not in comp:
        comp[row[1]] = []
        neg[row[1]] = []
        pos[row[1]] = []
        neu[row[1]] = []

    comp[row[1]].append(float(row[3]))
    neg[row[1]].append(float(row[4]))
    neu[row[1]].append(float(row[5]))
    pos[row[1]].append(float(row[6]))

#grafico de positividad
pos_top = []
pos_val = []

for topico, values in pos.items():
    pos_top.append(topico)
    pos_val.append(sum(values)/len(values))

#grafico de neg
neg_top = []
neg_val = []

for topico, values in neg.items():
    neg_top.append(topico)
    neg_val.append(sum(values)/len(values))

fig, ax = plt.subplots()
bar_width = 0.35
opacity = 0.8
positivos = plt.bar(np.arange(len(pos_val)), pos_val, bar_width, alpha=opacity, label="Positivo") 
negativos = plt.bar(np.arange(len(neg_val))+bar_width, neg_val, bar_width, alpha=opacity, label="Negativo") 
plt.title('Analisis de Sentimientos por topico')
plt.xticks(range(len(pos_top)), pos_top)
plt.legend()
plt.tight_layout()
plt.show()
plt.close()

#grafico de neg
comp_top = []
comp_val = []

for topico, values in comp.items():
    comp_top.append(topico)
    comp_val.append(sum(values)/len(values))


fig, ax = plt.subplots()
comportamiento = plt.bar(np.arange(len(comp_val)), comp_val) 
plt.title('Analisis de polaridad por topico')
plt.xticks(range(len(comp_top)), comp_top)
plt.tight_layout()
plt.show()
plt.close()
