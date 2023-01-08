#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 28/11/2022

@author: moise berthe
"""
import time
tps1 = time.time()

import pandas as pd
import preprocessing as pr

from document import RedditDocument, ArxivDocument
from author import Author
from corpus import Corpus

from scipy.sparse import csr_matrix

data = pd.read_csv("data/file.csv", header=None, sep=';')
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
corpus_docs = corpus.getDocs()

#  Transformer le texte en liste de mots
words = pr.process(all_texte)

#  Création du vocabulaire
#  On parcourt les mots sans doublons et on compte le nombre d'occurence de chacun d'eux
vocab = {}
for i, w in enumerate(set(words)):
    vocab[w] = { "id" : i, "occ" : words.count(w) , "ndoc": 0 }


mat_TF = []

for i, doc in enumerate(corpus_docs):
    mat = []
    doc_word = doc.getWords()
    length = len(doc_word)
    for word in vocab:
        tf = doc_word.count(word) / length
        idf = len(corpus_docs) 
        if tf > 0:
            vocab[word]['ndoc'] += 1
        mat.append(tf)
    mat_TF.append(mat)
mat_TF = csr_matrix(mat_TF)

import pickle

data = {"documents": corpus.getDocs(), "tf_idf" : mat_TF, "vocab" : vocab}
with open('data/mat_TF.pkl', 'wb') as file:
    pickle.dump(data, file)

tps2 = time.time()
print(f"Temps d'execution %2.fs" % (tps2 - tps1))