import pickle
import numpy as np
from numpy.linalg import norm

with open('data/mat_TF.pkl', 'rb') as file:
    data = pickle.load(file)

docs    = data["documents"]

for i in docs:
    print(i.titre)