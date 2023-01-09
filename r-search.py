import pickle
import doc.preprocessing as pr
import numpy as np
from numpy.linalg import norm

with open('data/mat_TF.pkl', 'rb') as file:
    data = pickle.load(file)
vocab   = data["vocab"]
docs    = data["documents"]
mat_TF  = data["tf_idf"].toarray()


search_term = input("Saisisez votre recherche : ")
# search_term = "database nosql prometheus"
terms = pr.process(search_term)
t_mat = []
for j, word in enumerate(vocab):
    tf = terms.count(word)/len(terms)
    t_mat.append(tf)
t_mat = np.array([t_mat])[0]

similarities = {}
for i, doc in enumerate(mat_TF):
    cosine_similarity = np.dot(doc, t_mat)/(norm(doc) * norm(t_mat))
    if cosine_similarity > 0:
        similarities[i] = cosine_similarity

similarities = dict(sorted(similarities.items(), key=lambda item : item[1], reverse=True))

for key in similarities:
    print(f"%.2f" % similarities[key], docs[key].titre)