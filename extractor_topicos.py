from time import time

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.datasets import fetch_20newsgroups

n_features = 50 # <--- tamano del vocabulario a construir. Se descartan del vocabulario aquellas palabras con bajo Tf-Idf (aquellas que estadisticamente aportan menos significado). Probar varios valores para ver que tan bien resulta la extraccion de topicos
n_components = 7 # <--- Cantidad de Tópicos a definir por los algoritmos. Probar variar este valor.
n_top_words = 20 # <--- Cantidad de palabras pertenecientes a cada tópico definido


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i]+'('+str(round(topic[i],3))+')'
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
    print()

print("Loading dataset...")
t0 = time()

def topicos_tweets(documentos, feature_names, modelo):
    resultado = []
    for doc in documentos:
        puntajes_por_topico = np.array([0]*len(modelo.components_))
        for idx_topico, topico in enumerate(modelo.components_):
            for palabra in doc.split():
                if palabra in feature_names:
                    puntajes_por_topico[idx_topico] += topico[feature_names.index(palabra)]
        indice_topico = puntajes_por_topico.argsort()[-1]
        indice_nombre_topico = modelo.components_[indice_topico].argsort()[-1]
        resultado.append(feature_names[indice_nombre_topico])
    return resultado


dataset = pd.read_csv('tweets_nyctsubway.csv',encoding ='latin1').texto

data_samples = np.unique(dataset.astype(str))
n_samples = len(data_samples)
print("done in %0.3fs." % (time() - t0))

# Use tf-idf features for NMF.
print("Extracting tf-idf features for NMF...")
tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2,
                                   stop_words='english')
t0 = time()
tfidf = tfidf_vectorizer.fit_transform(data_samples)
print("done in %0.3fs." % (time() - t0))

# Use tf (raw term count) features for LDA.
print("Extracting tf features for LDA...")
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2,
                                max_features=n_features,
                                stop_words='english')
t0 = time()
tf = tf_vectorizer.fit_transform(data_samples)
print("done in %0.3fs." % (time() - t0))
print()

# Fit the NMF model
print("Fitting the NMF model (Frobenius norm) with tf-idf features, "
      "n_samples=%d and n_features=%d..."
      % (n_samples, n_features))
t0 = time()
nmf = NMF(n_components=n_components, random_state=1,
          alpha=.1, l1_ratio=.5).fit(tfidf)
print("done in %0.3fs." % (time() - t0))

print("\nTopics in NMF model (Frobenius norm):")
tfidf_feature_names = tfidf_vectorizer.get_feature_names()
print_top_words(nmf, tfidf_feature_names, n_top_words)

# Fit the NMF model
print("Fitting the NMF model (generalized Kullback-Leibler divergence) with "
      "tf-idf features, n_samples=%d and n_features=%d..."
      % (n_samples, n_features))
t0 = time()
nmf = NMF(n_components=n_components, random_state=1,
          beta_loss='kullback-leibler', solver='mu', max_iter=1000, alpha=.1,
          l1_ratio=.5).fit(tfidf)
print("done in %0.3fs." % (time() - t0))

print("\nTopics in NMF model (generalized Kullback-Leibler divergence):")
tfidf_feature_names = tfidf_vectorizer.get_feature_names()
print_top_words(nmf, tfidf_feature_names, n_top_words)

print("Fitting LDA models with tf features, "
      "n_samples=%d and n_features=%d..."
      % (n_samples, n_features))
lda = LatentDirichletAllocation(n_components=n_components, max_iter=5,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)
t0 = time()
lda.fit(tf)
print("done in %0.3fs." % (time() - t0))

print("\nTopics in LDA model:")
tf_feature_names = tf_vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, n_top_words)

# Usar modelo 'lda' para asignar un topico a cada tweet en el archivo csv
write_df = pd.Series(topicos_tweets(dataset.astype(str), tf_feature_names, lda))

with open('tweets_nyctsubway.csv', 'a', encoding='utf8') as f:
    write_df.to_csv(f, columns=['topico'], index=False, header=False)
