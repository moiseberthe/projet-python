"""
@authors: moise berthe, lina belhadj
"""
import lib.preprocessing as pr
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
            self.words = pr.process(self.texte+" "+self.texte)
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
        
        
        
        
        