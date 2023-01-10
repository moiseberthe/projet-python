
import urllib
import praw
import xmltodict
import re
from praw.models import MoreComments
import pandas as pd
import datetime as dt
import Document as dc
import Author as at
import Corpus as cp
from importlib import reload
reload(dc)

docs=[]
id2doc={}
id2aut={}
#######################REDDIT######################
#Visual-Helicopter-77
#A55KJZiAuujE9zG

#Champs disponibles avec Praw: titres, posts, commentaires, descriptions subreddit

reddit = praw.Reddit(client_id='jWPEQQUR5r8K5wmrIbfQgw', 
                     client_secret='peazWPyYuh7m2iHQME7qZEZBSORdqw', 
                     user_agent='WebScraping')

"""try:
    with open("out.pkl", "rb") as f:
        corpus_plus100 = pickle.load(f)
except:
    subr = reddit.subreddit('Coronavirus')"""

# get 10 hot posts from the MachineLearning subreddit
hot_posts = reddit.subreddit('all').hot(limit=100)

#Remplissage de docs
for post in hot_posts:

    if post.selftext == "":  # Osef des posts sans texte
        pass
    #doc=dc.RedditDocument(post.subreddit, post.title, post.author.name, date, post.url, post.selftext)
    else : docs.append(("Reddit",post))
"""    id2doc[doc.id]=doc
    if not post.author.name in id2aut:
        aut=at.Author(post.author.name)
        id2aut[post.author.name]=aut
        id2aut[post.author.name].add(doc)
    else:
        id2aut[post.author.name].add(doc)"""
    #docs.append((post.title.replace("\n"," ")+post.selftext.replace("\n"," ")))


################ARXIV##################################

# Paramètres
query_terms = ["clustering", "Dirichlet"]
max_results = 20

# Requête
url = f'http://export.arxiv.org/api/query?search_query=all:{"+".join(query_terms)}&start=0&max_results={max_results}'
data = urllib.request.urlopen(url)

# Format dict (OrderedDict)
data = xmltodict.parse(data.read().decode('utf-8'))

#showDictStruct(data)

# Ajout résumés à la liste
for i, entry in enumerate(data["feed"]["entry"]):
    if i%10==0: print("ArXiv:", i, "/", 50)
    #docs.append(entry["summary"].replace("\n", ""))
    docs.append(("ArXiv", entry))
    #showDictStruct(entry)



##################CREATION DE DOCUMENTS########################

collection = []
for nature, doc in docs:
    if nature == "ArXiv":  # Les fichiers de ArXiv ou de Reddit sont pas formatés de la même manière à ce stade.
        #showDictStruct(doc)
        titre = doc["title"].replace('\n', '')  # On enlève les retours à la ligne
        auteurs = doc["author"]

        summary = doc["summary"].replace("\n", "")  # On enlève les retours à la ligne
        date = dt.datetime.strptime(doc["published"], "%Y-%m-%dT%H:%M:%SZ").strftime('%Y-%m-%d %H:%M:%S')  # Formatage de la date en année/mois/jour avec librairie datetime

        doc_classe = dc.ArxivDocument(titre, auteurs, date, doc["id"], summary)  # Création du Document
        collection.append(doc_classe)  # Ajout du Document à la liste.

    elif nature == "Reddit":
        #print("".join([f"{k}: {v}\n" for k, v in doc.__dict__.items()]))
        subreddit=doc.subreddit.name
        titre = doc.title.replace("\n", '')
        auteur = str(doc.author)
        date=dt.datetime.fromtimestamp(
        doc.created_utc
        ).strftime('%Y-%m-%d %H:%M:%S')
        url = "https://www.reddit.com/"+doc.permalink
        texte = doc.selftext.replace("\n", "")

        doc_classe = dc.RedditDocument(subreddit, titre, auteur, date, url, texte)
        collection.append(doc_classe)

# Création de l'index de documents
id2doc = {}
for i, doc in enumerate(collection):
    id2doc[i] = doc
#print(id2doc)


#####################AUTEURS#####################
for doc in collection:
    if not doc.auteur in id2aut:
        aut=at.Author(doc.auteur)
        id2aut[doc.auteur]=aut
        id2aut[doc.auteur].add(doc)
    else:
        id2aut[doc.auteur].add(doc)

corpus = cp.Corpus('corpus', id2aut, id2doc)
#corpus.print(10, 'title')
print(corpus.concorde('clustering', 20))

chaine = corpus.nettoyer_texte(id2doc[0].texte)
print(chaine)
vocabulaire = set()
for doc in corpus.id2doc.values():
    vocabulaire.add(re.split(" ", doc.texte))
print(vocabulaire)
#df = pd.DataFrame(c.__dict__ for t in things , columns=['titre', 'auteur', 'date', 'url', 'texte'])
#print(df)
#submission = reddit.submission(url="https://www.reddit.com/r/MapPorn/comments/a3p0uq/an_image_of_gps_tracking_of_multiple_wolves_in/")

#submission.comments.replace_more(limit=0)
#for comment in submission.comments.list():
#    print("\n"+comment.body)
"""
for post in id2doc.values():
    print(post)
    print("\n")
for aut in id2aut.values():
    print(aut)
    aut.stats(aut.getName())  
""" 

# =============== 2.9 : SAUVEGARDE ===============
"""import pickle

# Ouverture d'un fichier, puis écriture avec pickle
with open("corpus.pkl", "wb") as f:
    pickle.dump(corpus, f)

# Supression de la variable "corpus"
del corpus

# Ouverture du fichier, puis lecture avec pickle
with open("corpus.pkl", "rb") as f:
    corpus = pickle.load(f)"""
