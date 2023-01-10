"""
@authors: moise berthe, lina belhadj
"""

import praw
import datetime
import csv 


limit = 100
docs = []
query_word = 'all'
query_terms = ["clustering", "Dirichlet"]

#  Reddit
reddit = praw.Reddit(client_id='mXZ3f6Y8lPy7JCZJzCT7Iw', client_secret='XCPIKK12ow47wTqHrg6LZi1W1osdLQ', user_agent='TP3 WebScraping')
reddit_docs = reddit.subreddit('nosql').hot(limit=limit)
textes_Reddit = []


for doc in reddit_docs:
    if doc.selftext != "":
        date = datetime.datetime.fromtimestamp(doc.created_utc).strftime('%Y-%m-%d %H:%M:%S')
        docs.append([doc.title.replace("\n", " "), date, doc.url, doc.selftext.replace("\n", " "),  doc.author, doc.num_comments, 'Reddit'])
        

#  Arxiv
import urllib.request
import xmltodict 

textes_Arxiv = {}

url = 'http://export.arxiv.org/api/query?search_query=all:{}&start=0&max_results={}'.format("+".join(query_terms), limit)
data = urllib.request.urlopen(url)

data = xmltodict.parse(data.read().decode('utf-8'))
arxiv_docs = data['feed']['entry']

for doc in arxiv_docs:
    if(doc['summary'] != ''):
        try:
            authors = ", ".join([a["name"] for a in doc["author"]]) # On fait une liste d'auteurs, separes par une virgule
        except:
            authors = doc["author"]["name"]                         # Si l'auteur est seul, pas besoin de liste
            
        docs.append([doc['title'].replace("\n", " "), doc['published'], doc['link'][0]['@href'], doc['summary'].replace("\n", " "), authors, 0, 'Arxiv'])
        
        
with open('data/file2.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file, quoting=csv.QUOTE_ALL, delimiter=';')
    writer.writerows(docs)

print(f"{len(docs)} documents sauvegardes")