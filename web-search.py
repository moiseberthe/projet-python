"""
@authors: moise berthe, lina belhadj
"""
import cgi
import cgitb
import time
import pickle
import numpy as np

from lib.document import *

tps1 = time.time()

cgitb.enable()
form = cgi.FieldStorage()

if form.getvalue("query"):
    search_term = form.getvalue("query")
else:
    search_term = ""

# Recherche

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
    
    #  Ajout a l'interface graphique
    ndoc = len(doc2cos)
    if ndoc > 0:
        items = ""
        for key in doc2cos:
            d = docs[key]
            items += """
                    <div class="result">
                        <a href="{url}" class="link" target="_blank">
                            <div class="r-title">{titre}</div>
                            <div class="r-content">{content}</div>
                        </a>
                    </div>
                    <div class="separateur"></div>
                    """.format(url=d.url, titre=d.titre, content=d.texte[:200])


#  Affichage de l'interface graphique
resultat = "resultats" if ndoc > 1 else "resultat"
html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Moteur de recherche | Resultat</title>
    <link rel="stylesheet" href="web/search.css">
</head>
<body>
    <div class="container">
        <form action="" class="form">
            <div class="form-elt">
                <input type="text" name="query" id="query" class="search" placeholder="Rechercher" value="{val}" >
                <button type="submit" class="submit">Rechercher</button>
            </div>
        </form>
        <div class="results">
            <div class="main-title">
                <p class="title">Environ {nbr} {resultat} ({time:.2f} secondes)</p>
            </div>
            {items}
        </div>
    </div>
</body>
</html>
""".format(nbr=ndoc, val=search_term, items=items, resultat=resultat, time=time.time()-tps1)

print("Content-Type:text/html; charset=utf-8")
print()
print(html)