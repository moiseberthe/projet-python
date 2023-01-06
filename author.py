# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 14:27:35 2022

@author: mberthe5
"""

class Author:
    def __init__(self, name, ndoc):
        self.name = name
        self.ndoc = ndoc
        self.production = {}
    
    
    def addDoc(self, document, index):
        self.production[index] = document
        
    def __str__(self):
        return("Nom: "+self.name+"   Nombre de document: "+str(len(self.production))+"\n")
    def __repr__(self):
        return("Nom: "+self.name+"   Nombre de document: "+str(len(self.production))+"\n")
    
    def stat(self):
        temp = [len(doc.texte) for doc in self.production.values()]
        mean = 0 if len(temp) == 0 else (float(sum(temp)) / len(temp))
        print("Statistiques ({})\n\tNombre de documents produits: {} \n\tTaille moyenne des documents: {}\n".format(self.name, len(self.production), mean))