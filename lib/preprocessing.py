"""
@authors: moise berthe, lina belhadj
"""
import string
import re

def stopwords(): 
    return [
        'theirs', 'too', 'her', 'were', 'such', 'be', 'mustn', "needn't", 'over', 'both', 'itself', 'haven', 
        "hadn't", 'themselves', 'until', 'being', 'himself', 'is', 'weren', 'where', 'their', 'any', 't', 
        'been', 'so', 'through', 'above', 'more', 'the', "haven't", 'while', 'most', 'up', 'for', "you've", 
        'them', 'those', 'same', 'she', 'against', "shouldn't", 'shouldn', 'at', 'because', 'my', "wasn't", 
        'here', 'him', 'd', 'off', 'i', 'by', 'after', 'it', "won't", 'shan', 'which', 'should', 'its', 'from', 
        'than', 'do', 'then', 'once', 'yourself', 'what', 'herself', 'an', 'further', 'each', 'between', 
        "weren't", 's', "should've", "you'd", 'again', 'll', 'there', 'ain', "hasn't", "she's", 'a', 'yours',
        'with', 'has', 'some', 'are', 'm', 'your', 'now', 'have', 'that', 'but', 'if', 'y', 'our', 'does',
        'doing', 'wouldn', 'these', 'was', 'as', "aren't", 'about', "wouldn't", 'mightn', 'o', 'nor', 'needn',
        'when', 'before', 'other', 'can', 'few', 'he', "mustn't", 'during', 'just', "doesn't", 'wasn', 'very',
        'this', 'having', 'under', 'hers', 'why', "shan't", 're', 'doesn', "that'll", 'me', 'only', 'aren', 've',
        'not', 'will', 'we', 'in', 'whom', 'did', 'of', 'or', 'and', 'who', 'am', 'out', 'all', "isn't", 'ma', 
        'ourselves', 'on', 'yourselves', 'no', 'they', 'you', 'had', "don't", 'to', 'ours', "mightn't", 'into',
        'his', 'down', "couldn't", 'isn', 'myself', 'couldn', 'don', 'how', "didn't", 'own', 'won', 'hasn', 
        'hadn',"you're", "you'll", "it's", 'didn', 'below'
    ]

def process(text):
    words = text.split()
    #  Suppression des ponctuations
    delpt = re.compile('[%s]' % re.escape(string.punctuation))
    words = [delpt.sub(' ', w) for w in words]

    #  Suppression des chaines initules, des chaines a un caratere et des nombre. Mise en miniscule
    words = [w.lower() for w in words if w not in stopwords() and len(w) > 2 and w.isalpha()]
    words.sort()
    return words