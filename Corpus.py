import re
import pandas
def singleton(cls):
    instance = [None]
    def wrapper(*args, **kwargs):
        if instance[0] is None:
            instance[0] = cls(*args, **kwargs)
        return instance[0]
    return wrapper

@singleton
class Corpus:
    
    ndoc=0
    naut=0
    
    def __init__(self, nom, auteurs, id2doc):
        self.nom=nom
        self.auteurs=auteurs
        self.id2doc=id2doc
        self.ndoc=len(id2doc)
        self.naut=len(auteurs)

    def docDate(self, doc):
        return self.id2doc['date']

    def docTitre(self,doc):
        return self.id2doc['titre']

    def printSortDate(self):
        doc=self.id2doc
        sorted(doc.items())
        print()


    def print(self, ndocs, sort):
        if(sort=='title'):
            doc=self.id2doc
            doc=sorted(list(doc.values()), key=lambda doc:doc.titre, reverse=False)               
        elif(sort=='date'):
            doc=self.id2doc
            doc=sorted(list(doc.values()), key=lambda doc:doc.date, reverse=False)   
        for i in range(0,ndocs):
            print (f"{doc[i]}, Source: {doc[i].getType()}")       

    def __repr__(self, ndocs):
        return self.id2doc[:ndocs]

    
    def search(self, clef):
        txt = ''.join(map(str,self.id2doc.values()))
        p = re.compile(clef)
        res = p.finditer(txt)
        for r in res:
            (i, j) = r.span()
            print (f"Trouvé en pos {i} : {txt[i:j]}")
        return


    def concorde(self, clef, contexte):
        txt = ''.join(map(str,self.id2doc.values()))
        p = re.compile(clef)
        res = p.finditer(txt)
        df = pandas.DataFrame(columns = ['Contexte gauche', 'Motif trouvé', 'Contexte droit'])
        for r in res:
            (i, j) = r.span()
            #df=df.append({'Contexte gauche' : txt[i-contexte:i] , 'Motif trouvé' : txt[i:j], 'Contexte droit' : txt[j:j+contexte]} , ignore_index=True)
            df.loc[len(df.index)] = [txt[i-contexte:i],  txt[i:j], txt[j:j+contexte]]     
        return df

    def nettoyer_texte(self, chaine):
        
        return (re.sub("[^A-z\ ]", '', chaine.lower()))
