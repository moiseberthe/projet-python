import cgi
import cgitb
import doc.preprocessing as pr

cgitb.enable()
form = cgi.FieldStorage()

if form.getvalue("query"):
    search_term = form.getvalue("query")
else:
    raise Exception("Pseudo non disponible")
## Recherche
import pickle
# import preprocessing as pr
import numpy as np
from numpy.linalg import norm

with open('data/mat_TF.pkl', 'rb') as file:
    data = pickle.load(file)

vocab   = data["vocab"]
docs    = data["documents"]
mat_TF  = data["tf_idf"].toarray()


# search_term = input("Recherche : ")
# search_term = "database nosql prometheus"
terms = pr.process(search_term)
t_mat = []
for j, word in enumerate(vocab):
    tf = terms.count(word)/len(terms)
    t_mat.append(tf)
t_mat = np.array([t_mat])[0]

cos = {}
for i, doc in enumerate(mat_TF):
    cosine = np.dot(doc, t_mat)/(norm(doc) * norm(t_mat))
    if cosine > 0:
        cos[i] = cosine

cos = dict(sorted(cos.items(), key=lambda item: item[1], reverse=True))
## Fin

items = ""

print("Content-type: text/html; charset=utf-8")
style = """
.container{
    max-width: 80%;
    margin: auto;
}
.form-elt .search{
    padding: 16px;
    border: 1px solid #e4e4e4;
    border-radius: 32px;
    width: 100%;
    outline: none;
    font-size: 16px;
}
.form-elt .search:focus{
    box-shadow: 0 1px 6px rgb(32 33 36 / 28%);
}
.result{
    padding: 16px;
}
.result .link{
    text-decoration: none;
    font-size: 16px;
}
.r-content{
    color: #444;
}
.r-title {
    padding-bottom: 8px;
}
.separateur{
    width: 100%;
    height: 1px;
    background-color: #e4e4e4;
    margin: auto;
}
.main-title .title{
    font-size: 18px;
    color: #444;
    margin-bottom: 16px;
    padding: 0 16px;
    font-weight: 700;
}
"""
for key in cos:
    d = docs[key]
    items += """
            <div class="result">
                <a href="{url}" class="link">
                    <div class="r-title">{titre}</div>
                    <div class="r-content">{content}</div>
                </a>
            </div>
            <div class="separateur"></div>
            """.format(url=d.url, titre=d.titre, content=d.texte[:200])
html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Moteur de recherche | Resultat</title>
    <style>{style}</style>
</head>
<body>
    <div class="container">
        <form action="" class="form">
            <div class="form-elt">
                <input type="text" name="query" id="query" class="search" placeholder="Rechercher" value="{val}" >
            </div>
        </form>
        <div class="results">
            <div class="main-title">
                <p class="title">Environ {nbr} resultats (0,41 secondes)</p>
            </div>
            {items}
        </div>
    </div>
</body>
</html>
""".format(nbr=len(cos), style=style, val=search_term, items=items)
print(html)