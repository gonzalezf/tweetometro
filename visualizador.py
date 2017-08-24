from time import time

import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer, CountVectorizer
from sklearn.manifold import TSNE

import matplotlib.pyplot as plt
import matplotlib.colors as colors

n_features = 50 # <--- tamano del vocabulario a construir. Se descartan del vocabulario aquellas palabras con bajo Tf-Idf (aquellas que estadisticamente aportan menos significado). Probar varios valores para ver que tan bien resulta la extraccion de topicos

print("Loading dataset...")
t0 = time()
dataset = pd.read_csv('tweets_nyctsubway.csv', sep=';', encoding ='latin1')

cuerpo_tweets = dataset.texto.astype(str)
topico_por_tweet = dataset.topico.astype(str)


print("done in %0.3fs." % (time() - t0))

# Use tf (raw term count) features.
print("Extracting and scaling tf features...")
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2,
                                max_features=n_features,
                                stop_words='english')
t0 = time()
tf = tf_vectorizer.fit_transform(cuerpo_tweets)
tf_scaler = TfidfTransformer(use_idf=False)
scaled_tf = tf_scaler.fit_transform(tf)
print("done in %0.3fs." % (time() - t0))
print()

# t-SNE clustering
print('\nClustering de tweets')
t0 = time()


# Descomentar siguiente linea si se quiere entrenar t-SNE con tweets sin repetir
#scaled_tf = np.unique(scaled_tf)
'''
print(scaled_tf.shape)
dataset_muestra = []
for indice_topico, tuit in enumerate(cuerpo_tweets):
    if len(np.where(cuerpo_tweets == tuit)[0]) == 1:
        dataset_muestra.append( (topico_por_tweet[indice_topico], tuit) )
print(len(dataset_muestra))
'''
# Creacion de colores
color_map = plt.get_cmap('gist_rainbow')
topicos_unicos = np.unique(np.array(topico_por_tweet.tolist()))
print('Topicos distintos',topicos_unicos)
num_colores = len(topicos_unicos)
print('Cantidad colores:', num_colores)
colores_topicos = {}
for i in range(num_colores):
    colores_topicos[topicos_unicos[i]] = color_map(1.*i/num_colores)

# Definicion y entrenamiento
tsne = TSNE(n_components=2, init='pca', random_state=0, verbose=2, n_iter=1000)

tuits_tsne = tsne.fit_transform(scaled_tf.toarray())
print("done in %0.3fs." % (time() - t0))

# Plotting
plt.figure()
for idx, cl in enumerate(np.unique(tuits_tsne, axis=0)):
    plt.scatter(x=tuits_tsne[idx, 0], y=tuits_tsne[idx, 1], c=colores_topicos[ topico_por_tweet[ np.where(tuits_tsne == cl)[0][0] ] ])
plt.show()
