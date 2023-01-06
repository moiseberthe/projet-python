#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 08/05/2020

@author: moise berthe
"""

import pandas as pd
import re

from document import RedditDocument, ArxivDocument
from author import Author
from corpus import Corpus

data = pd.read_csv("data/file.csv", header=None, sep=';')
docs = list(data.values)

id2doc = {}
id2aut = {}
all_texte = ""
k=1
for doc in docs:
    doc_title   = str(doc[0])
    doc_date    = str(doc[1])
    doc_url     = str(doc[2])
    doc_text    = str(doc[3])
    doc_authors = str(doc[4]).split(",")
    doc_source  = str(doc[-1])
    
    #  Chaine de caractere contenant tous les documents
    all_texte += " "+doc_text
    
    #  Si l'auteur est seul, pas besoin de liste
    if(len(doc_authors) == 1):
        doc_authors = doc_authors[0]

    #  Document provenant de Reddit
    if (doc_source == "Reddit"):
        document = RedditDocument(doc_title, doc_date, doc_url, doc_text, doc_authors, 12)
    
    #  Document provenant d'Arxiv
    if (doc_source == "Arxiv"):
        document = ArxivDocument(doc_title, doc_date, doc_url, doc_text, doc_authors)
    
    id2doc[k] = document
    k+=1

    #  Creation des auteurs
    for author in str(doc[4]).split(","):
        h = author.lower()
        if (h not in id2aut):
            id2aut[h] = Author(author, 1)
        
        #  Ajouter le document a la production d'un auteur
        id2aut[h].addDoc(document, h)
    
corpus = Corpus("Le corpus", id2aut, id2doc)
corpus.setText(all_texte)

words = re.sub("\(|\[|\)\]", " ", corpus.getText())
words = re.split(' |\t|,', words)
words = list(set(words))

print(words)
# for i in corpus.id2doc.values():
#     for j in words:
#         pass