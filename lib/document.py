"""
@authors: moise berthe, lina belhadj
"""
import string
import re

class Document:
    
    indice=0
    
    def __init__(self, titre, date, url, texte):
        self.titre = titre
        self.date = date
        self.url = url
        self.texte = texte
        self.words = []
        self.type = self.__class__.__name__
        Document.indice += 1
        
        
    def getText(self):
        return str(self.texte)
    
    def getType(self):
        return self.type

    def describe(self):
        text = self.getText()
        return {
            "type"  : self.getType(),
            "nchar" : len(text),
            "nword" : len(text.split(" ")),
            "nsent" : len(text.split("."))
        }
    def getWords(self):
        if(len(self.words) == 0):
            self.words = Preprocessing.process(self.titre+" "+self.texte)
        return self.words

    def print(self):
        print("Titre: {}\nDate: {}\nUrl: {}\nTexte: {}".format(self.titre, self.date, self.url, self.texte, ))
     
    def __str__(self):
        return("Titre: "+self.titre+"\nDate: "+self.date+"\n")

    def __repr__(self):
        return("Titre: "+self.titre+"\nDate: "+self.date+"\n"+self.type)
    
    
class RedditDocument(Document):
    
    def __init__(self, titre, date, url, texte, auteur, nbCom):
        super().__init__(titre, date, url, texte)
        self.nbCom = nbCom
        self.auteur = auteur
        
        
    def getNbCom(self):
        return self.nbCom
    
    def setNbCom(self, nbCom):
        self.nbCom = nbCom
    
    def print(self):
        print("Titre: {}\nAuteur: {}\nDate: {}\nUrl: {}\nTexte: {}".format(self.titre, self.auteur, self.date, self.url, self.texte, ))
        

class ArxivDocument(Document):
    
    def __init__(self, titre, date, url, texte, auteurs):
        super().__init__(titre, date, url, texte)
        self.auteurs = auteurs
        
    def print(self):
        print("Titre: {}\nAuteur: {}\nDate: {}\nUrl: {}\nTexte: {}".format(self.titre, self.auteurs, self.date, self.url, self.texte, ))
        
        
class Preprocessing:
    
    @staticmethod
    def stopwords(): 
        return [
            'theirs', 'too', 'her', 'were', 'such', 'be', 'mustn', "needn't", 'over', 'both', 'itself', 'haven', 
            "hadn't", 'themselves', 'until', 'being', 'himself', 'is', 'weren', 'where', 'their', 'any', 't', 
            'been', 'so', 'through', 'above', 'more', 'the', "haven't", 'while', 'most', 'up', 'for', "you've", 
            'them', 'those', 'same', 'she', 'against', "shouldn't", 'shouldn', 'at', 'because', 'my', "wasn't", 
            'here', 'him', 'd', 'off', 'i', 'by', 'after', 'it', "won't", 'shan', 'which', 'should', 'its', 'from', 
            'than', 'do', 'then', 'once', 'yourself', 'what', 'herself', 'an', 'further', 'each', 'between', 
            "weren't", 's', "should've", "you'd", 'again', 'll', 'there', 'ain', "hasn't", "she's", 'a', 'yours',
            'with', 'has', 'some', 'are', 'm', 'your', 'now', 'have', 'that', 'but', 'if', 'y', 'our', 'does',
            'doing', 'wouldn', 'these', 'was', 'as', "aren't", 'about', "wouldn't", 'mightn', 'o', 'nor', 'needn',
            'when', 'before', 'other', 'can', 'few', 'he', "mustn't", 'during', 'just', "doesn't", 'wasn', 'very',
            'this', 'having', 'under', 'hers', 'why', "shan't", 're', 'doesn', "that'll", 'me', 'only', 'aren', 've',
            'not', 'will', 'we', 'in', 'whom', 'did', 'of', 'or', 'and', 'who', 'am', 'out', 'all', "isn't", 'ma', 
            'ourselves', 'on', 'yourselves', 'no', 'they', 'you', 'had', "don't", 'to', 'ours', "mightn't", 'into',
            'his', 'down', "couldn't", 'isn', 'myself', 'couldn', 'don', 'how', "didn't", 'own', 'won', 'hasn', 
            'hadn',"you're", "you'll", "it's", 'didn', 'below'
        ]

    @staticmethod
    def process(text):
        words = text.split()
        #  Suppression des ponctuations
        delpt = re.compile('[%s]' % re.escape(string.punctuation))
        words = [delpt.sub(' ', w) for w in words]

        #  Suppression des chaines initules, des chaines a un caratere et des nombre. Mise en miniscule
        words = [w.lower() for w in words if w not in Preprocessing.stopwords() and len(w) > 2 and w.isalpha()]
        words.sort()
        return words