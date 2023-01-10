# -*- coding: utf-8 -*-
"""
Created on 28/11/2022

@authors: moise berthe, lina belhadj
"""
import time
tps1 = time.time()

import pickle
import http.server
import webbrowser
import numpy as np
import pandas as pd

from lib.document import RedditDocument, ArxivDocument, Preprocessing
from lib.author import Author
from lib.corpus import Corpus

from math import log
from scipy.sparse import csr_matrix


data = pd.read_csv("data/file.csv", encoding="utf-8", header=None, sep=';')
docs = list(data.values)

id2doc = {}
id2aut = {}
all_texte = ""
for key, doc in enumerate(docs):
    doc_title   = str(doc[0])
    doc_date    = str(doc[1])
    doc_url     = str(doc[2])
    doc_text    = str(doc[3])
    doc_authors = str(doc[4]).split(",")
    doc_com     = int(doc[5])
    doc_source  = str(doc[-1])
    
    #  Chaine de caractere contenant tous les documents (titre + contenu)
    all_texte += " "+doc_title+" "+doc_text
    
    #  Si l'auteur est seul, pas besoin de liste
    if(len(doc_authors) == 1):
        doc_authors = doc_authors[0]

    #  Document provenant de Reddit
    if (doc_source == "Reddit"):
        document = RedditDocument(doc_title, doc_date, doc_url, doc_text, doc_authors, 12)
    
    #  Document provenant d'Arxiv
    if (doc_source == "Arxiv"):
        document = ArxivDocument(doc_title, doc_date, doc_url, doc_text, doc_authors)
    
    id2doc[key] = document

    #  Creation des auteurs
    for author in str(doc[4]).split(","):
        h = author.lower()
        if (h not in id2aut):
            id2aut[h] = Author(author, 1)
        
        #  Ajouter le document a la production d'un auteur
        id2aut[h].addDoc(document, h)
    
corpus = Corpus("Le corpus", id2aut, id2doc)
corpus.setText(all_texte)

#  Transformer le texte en liste de mots
words = Preprocessing.process(all_texte)

#  Stockage du vocabulaire dans un dictionnaire avec les mots en tant que valeur
vocab = {'mot': words}

#  Calcul de la fréquence des mots dans le corpus
df1=pd.DataFrame(vocab, columns=['mot'])
freq=df1.mot.value_counts()

#  Elimination des doublons et tri de la liste de vocabulaire
words = list(set(words))
words.sort()
#  Creation du dictionnaire vocab avec les mots en tant que clés et contenant un sous-dictionnaire avec l'id, et la fréquence du mot dans le corpus
vocab = {words[i]: {"id": i, "freq_corpus": freq[words[i]], "freq_documents": 0} for i in range(0, len(words))}


mat_TF = []
#  Calcul de la matrice TF
for i, doc in enumerate(corpus.getDocs()):
    texte = doc.getWords()
    mat = []
    for word in words:
        occ = texte.count(word)
        mat.append(texte.count(word)/len(texte))
        if occ > 0:
            vocab[word]["freq_documents"]+=1
    mat_TF.append(mat)


#  Calcul de la matrice TFxIDF
for i, doc in enumerate(corpus.getDocs()):
    for j, word in enumerate(words):
        cond = vocab[word]["freq_documents"] > 0
        IDF = log(len(corpus.id2doc)/vocab[word]["freq_documents"], 10) if cond else 0
        mat_TF[i][j] *= IDF

mat_TF = csr_matrix(mat_TF)

#  Stockage des docmuents du corpus, de la matrice tf-idf et du vocabulaire dans un fichier pickle
data = {"documents": corpus.getDocs(), "tf_idf" : mat_TF, "vocab" : vocab}
with open('data/mat_TFIDF.pkl', 'wb') as file:
    pickle.dump(data, file)


#  Lancement d'un server web avec l'interface graphique
port = 1236
address = ("", port)

server = http.server.HTTPServer

handler = http.server.CGIHTTPRequestHandler
handler.cgi_directories = ["/"]

httpd = server(address, handler)

print(f"Temps d'execution %2.fs" % (time.time() - tps1))
print (f"Serveur démarré sur le PORT {port}\nAdresse: http://127.0.0.1:{port}/index.py")
webbrowser.open(f'http://127.0.0.1:{port}/index.py', 2)
httpd. serve_forever()
