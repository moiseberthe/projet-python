class Author:

    def __init__(self, nom):
        self.__nom=nom
        self.__production={}
        self.__ndoc=0
        
    def add(self,document):
        self.__production[document.id]=document
        self.__ndoc+=1
        
        
    def getName(self):
        return self.__nom
        
    def getNbDocs(self):
        return self.__ndoc
    
    def tailleDocsMoy(self):
        taille=0
        for x in self.__production.values():
            taille+=x.tailleTexte()
        return taille/self.__ndoc
        
    def stats(self, nom):
        print("Nombre de documents publiés: " + str(self.getNbDocs())+
              "\nTaille moyenne des documents: " + str(self.tailleDocsMoy()))
        
    def __str__(self):
        return ("Nom: "+self.__nom+
                "\nNombre de documents publiés: "+str(self.__ndoc))
        
    def print(self):
        print ("Nom: "+self.__nom+
                "\nNombre de documents publiés: "+self.__ndoc)
        