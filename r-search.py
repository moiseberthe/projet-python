import pickle
import preprocessing as pr
import numpy as np
from numpy.linalg import norm

with open('data/mat_TF.pkl', 'rb') as file:
    data = pickle.load(file)
vocab   = data["vocab"]
docs    = data["documents"]
mat_TF  = data["tf_idf"].toarray()


# search_term = input("Recherche : ")
search_term = "database nosql prometheus"
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

for key in cos:
    print(f"%.2f" % cos[key], docs[key].titre)