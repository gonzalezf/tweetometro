
import os
from elasticsearch import Elasticsearch
es = Elasticsearch()

contador = 0
for filename in os.listdir(os.getcwd()+'/tweets_chile'): #Leer archivos txt en tweets_chile
	f = open(os.getcwd()+'/tweets_chile/'+filename, 'r')
	content = f.read()
	print content
	contador+=1 #id del tweet a indexar
	res = es.index(index="test", doc_type='tweet', id=contador, body={'text': content}) #indexar cada tweet.
print "-----------------------"
print "Indexacion finalizada. "
print "-----------------------"
print "Ej, tweet con id = 200 es el siguiente"
print es.get(index='test',doc_type='tweet',id=200)
print "-----------------------"
print "Ej: devolver tweets relevantes que contengan la palabra chilenos"
print es.search(index='test',body={"query":{"match":{'text':'chilenos'}}})
print "Ej: devolver tweets relevantes que contengan la palabra 'el'"
print es.search(index='test',body={"query":{"match":{'text':'el'}}})