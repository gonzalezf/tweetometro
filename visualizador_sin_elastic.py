import pickle
from collections import Counter
from scipy.sparse import csr_matrix # <--- Compressed Sparse Row (CSR) matrix: estructura de datos para almacenar y manipular eficientemente matrices con muchos ceros, lo que ocurre al vectorizar los tweets
from scipy.sparse import vstack # <--- para unir matrices CSR verticalmente
from sklearn.feature_extraction import text
from sklearn.manifold import TSNE
from sklearn.decomposition import TruncatedSVD

import sys
import os
import re
import matplotlib.pyplot as plt
import numpy as np

try:
    tuit_tf = pickle.load(open('tuit_tf.pickle', 'rb'))
except (OSError, IOError) as e:
    tuits = []
    i=0
    for archivo_tuit in os.listdir('tweets_nyctsubway/bruto'):
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
        texto = re.sub(r'https?:\/\/.*[\r\n]*', '', dicc['text'], flags=re.MULTILINE)
        tuits.append(texto)
        i += 1
        if i%100 == 0:
            print('Leidos', i, 'tweets')
            print(texto.encode('utf8'))

    # Preprocesador de texto y constructor de matriz de ocurrencias.
    count_vect = text.CountVectorizer(decode_error='replace',
                                        strip_accents='unicode',
                                        stop_words='english',
                                        ngram_range=(1, 4),
                                        max_df=0.95, min_df=2)

    print('Cantidad total tweets:', len(tuits))
    tuit_counts = count_vect.fit_transform(tuits) # <--- matriz de ocurrencias de palabras del vocabulario
    print('Shape vocabulario', tuit_counts.shape) # shape: (cantidad_tweets, tamano_vocabulario)

    tf_transformer = text.TfidfTransformer(use_idf=False)
    tuit_tf = tf_transformer.fit_transform(tuit_counts) # <--- matriz de frecuencia de términos del conjunto de tweets

    pickle.dump(tuit_tf, open('tuit_tf.pickle', 'wb'))

# Reduccón de dimensionalidad de matriz dispersa
print('Shape antes de Dim. Reduct.:', tuit_tf.shape)
svd = TruncatedSVD(n_components=10, n_iter=5)

print('Reduccion de dimensionalidad...')
tuit_tf_reducido = svd.fit_transform(tuit_tf)
print('Shape luego de Dim. Reduct.:', tuit_tf_reducido.shape)

# Eliminar tweets identicos (Retweets)
tuit_tf_reducido_unicos = np.unique(tuit_tf_reducido, axis=0)
print('Shape luego de eliminar tweets repetidos:', tuit_tf_reducido_unicos.shape)

# Clustering
tsne = TSNE(n_components=2, random_state=0, init='pca', verbose=2, n_iter=1000, perplexity=30,learning_rate=200.0)
tuit_test_2d = tsne.fit_transform(tuit_tf_reducido_unicos)

print('Cantidad de puntos:', len(list(enumerate(np.unique(tuit_test_2d, axis=0)))))

# color_map = {0: 'red', 1:'blue', 2:'lightgreen', 3:'purple', 4:'cyan'}

plt.figure()
for idx, cl in enumerate(np.unique(tuit_test_2d, axis=0)):
    plt.scatter(x=tuit_test_2d[idx, 0], y=tuit_test_2d[idx, 1])
plt.show()
