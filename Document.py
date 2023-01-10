class Document:
    
    id=0
    
    def __init__(self, titre, auteur, date, url, texte):
        self.titre=titre
        self.auteur=auteur
        self.date=date
        self.url=url
        self.texte=texte
        Document.id+=1
        
        
    def tailleTexte(self):
        return len(self.texte)
        
        
    def __str__(self):
        return f"{self.titre}, par {self.auteur}\n"
    
    def __repr__(self):
        return("Titre: " + self.titre +
              "\nAuteur: " + self.auteur+
              "\nDate: " + self.date+
              "\nUrl: " + self.url+
              "\nTexte: " + self.texte+
              "\n")
    
class RedditDocument(Document):
    
    def __init__(self, subreddit, titre, auteur, date, url, texte):
        super().__init__(titre, auteur, date, url, texte)
        self.subreddit=subreddit
        
    def getSubreddit(self):
        return self.__subreddit
    def setSubreddit(self, subreddit):
        self.subreddit=subreddit
        
    def getType(self):
        return 'reddit'
        
    def __str__(self):
        return f"{Document.__str__(self)}, dans le subreddit {self.subreddit}"


class ArxivDocument(Document):
    
    def __init__(self, titre, auteurs, date, url, texte):
        try:
            auteurs = ", ".join([a["name"] for a in auteurs])  # On fait une liste d'auteurs, séparés par une virgule
        except:
            auteurs = auteurs["name"]  # Si l'auteur est seul, pas besoin de liste
        super().__init__(titre, auteurs, date, url, texte)
       
        
    def getType(self):
        return 'arxiv'
        

class DocumentGenerator:
    @staticmethod
    def factory(type, titre, auteur, date, url, texte, subreddit="none"):
        if(type=="reddit"):
            return RedditDocument(subreddit, titre, auteur, date, url, texte)
        elif(type=="arxiv"):
            return ArxivDocument(titre, auteur, date, url, texte)
        else:
            return Document(titre, auteur, date, url, texte)