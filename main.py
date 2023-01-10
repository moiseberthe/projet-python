"""
@author: lina belhadj
"""
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
import time
tps1 = time.time()
docs=[]
id2doc={}
id2aut={}

#  Certains morceaux de code, notamment dans la récupération des publications Reddit et Arxiv, ont été repris de la correction
#######################REDDIT######################

reddit = praw.Reddit(client_id='jWPEQQUR5r8K5wmrIbfQgw', 
                     client_secret='peazWPyYuh7m2iHQME7qZEZBSORdqw', 
                     user_agent='WebScraping')


#  Récupération des 100 posts les plus populaires Reddit
hot_posts = reddit.subreddit('all').hot(limit=100)

#  Remplissage de docs
for post in hot_posts:

    if post.selftext != "":
        docs.append(("Reddit",post))


################ARXIV##################################

# Paramètres
query_terms = ["clustering", "Dirichlet"]
max_results = 20

# Requête
url = f'http://export.arxiv.org/api/query?search_query=all:{"+".join(query_terms)}&start=0&max_results={max_results}'
data = urllib.request.urlopen(url)

# Format dict (OrderedDict)
data = xmltodict.parse(data.read().decode('utf-8'))

# Ajout résumés à la liste
for i, entry in enumerate(data["feed"]["entry"]):
    docs.append(("ArXiv", entry))


##################CREATION DE DOCUMENTS########################

collection = []
for nature, doc in docs:
    if nature == "ArXiv":  # Les fichiers de ArXiv ou de Reddit sont pas formatés de la même manière à ce stade.
        titre = doc["title"].replace('\n', '')  # On enlève les retours à la ligne
        auteurs = doc["author"]

        summary = doc["summary"].replace("\n", "")  # On enlève les retours à la ligne
        date = dt.datetime.strptime(doc["published"], "%Y-%m-%dT%H:%M:%SZ").strftime('%Y-%m-%d %H:%M:%S')  # Formatage de la date en année/mois/jour avec librairie datetime

        doc_classe = dc.ArxivDocument(titre, auteurs, date, doc["id"], summary)  # Création du Document
        collection.append(doc_classe)  # Ajout du Document à la liste.

    elif nature == "Reddit":
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

#####################AUTEURS#####################
for doc in collection:
    if not doc.auteur in id2aut:
        aut=at.Author(doc.auteur)
        id2aut[doc.auteur]=aut
        id2aut[doc.auteur].add(doc)
    else:
        id2aut[doc.auteur].add(doc)

corpus = cp.Corpus('corpus', id2aut, id2doc)

print("Fonction concorde: \n",corpus.concorde('clustering', 20))

chaine = corpus.nettoyer_texte(id2doc[0].texte)
vocabulaire = list()
vocabulaire=re.split(" ", doc.texte)

vocabulaire=list(set(vocabulaire))
print("Vocabulaire : \n",vocabulaire)

print(f"Temps d'execution %2.fs" % (time.time() - tps1))

