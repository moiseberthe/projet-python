"""
@authors: moise berthe, lina belhadj
"""
import pickle
import numpy as np
from lib.document import Preprocessing

with open('data/mat_TFIDF.pkl', 'rb') as file:
    data = pickle.load(file)
vocab   = data["vocab"]
docs    = data["documents"]
mat_TF  = data["tf_idf"].toarray()


search_term = input("Saisissez votre recherche : ")
terms =  Preprocessing.process(search_term)
items = '<div class="result"><h3>Aucune correspondance.</h3></div>'
ndoc = 0

if len(terms) > 0:
    
    #  Recuperation des docmuents du corpus, de la matrice tf-idf et du vocabulaire a partir du fichier pickle
    with open('data/mat_TFIDF.pkl', 'rb') as file:
        data = pickle.load(file)

    vocab       = data["vocab"]
    docs        = data["documents"]
    mat_TFIDF   = data["tf_idf"].toarray()


    #  Transformation des mots-clefs de recherche sous la forme d’un vecteur sur le vocabulaire
    t_mat = []
    for j, word in enumerate(vocab):
        tf = terms.count(word)/len(terms)
        t_mat.append(tf)
    t_mat = np.array(t_mat)
    
    #  Calcul de la similarité entre le vecteur des mots-clefs et tous les documents à l'aide de la Similarité cosinus
    doc2cos = {}    #  Dictionnaire avec comme clef l'index du document et comme valeur la similarité
    seuil = 0       #  Seuil de simularité
    for i, doc in enumerate(mat_TFIDF):
        cosine = np.dot(doc, t_mat)/(np.linalg.norm(doc) * np.linalg.norm(t_mat))
        if cosine > seuil:
            doc2cos[i] = cosine
    
    #  Trie suivant les valeurs de similarité
    doc2cos = dict(sorted(doc2cos.items(), key=lambda item: item[1], reverse=True))
    ndoc = len(doc2cos)
if(ndoc > 0):
    for key in doc2cos:
        print(f"%.2f" % doc2cos[key], docs[key].titre)
else:
    print("Aucune correspondance")