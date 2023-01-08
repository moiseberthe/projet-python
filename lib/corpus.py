# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 14:24:38 2022

@authors: moise berthe, lina belhadj
"""
import re
class Corpus:
    instance = None
    def __init__(self, name, authors, id2doc):
        self.name = name
        self.authors = authors
        self.id2doc = id2doc
        self.ndoc = len(self.id2doc)
        self.naut = len(self.authors)
        self.text = ""
        
    def setText(self, text):
        self.text = text
    def getText(self):
        return self.text

    def describe(self):
        print(f"Corpus : {self.name}\t# documents {self.ndoc}\t#auteurs : {self.naut}\t#caracteres : {len(self.text)}")
        for i, doc in self.id2doc.items():
            doc = doc.describe()
            print(f"Document {i}\t# caracteres : {doc['nchar']}\t# mots : {doc['nword']} \t# phrases : {doc['nsent']}\t# type : {doc['type']}")
    
    def getDocs(self, byDate=True):
        newlist = list(self.id2doc.values())
        if (byDate):    
            newlist = sorted(newlist, key=lambda x: x.date, reverse=True)
        else:
            newlist = sorted(newlist, key=lambda x: x.titre, reverse=False)
        return newlist
    
    def getDocValues(self):
        return list(self.id2doc.values())
    
    @staticmethod
    def getInstance(name, authors, id2doc):
        if not Corpus.instance:
            Corpus.instance = Corpus(name, authors, id2doc)
        return Corpus.instance
            