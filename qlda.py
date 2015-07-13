import numpy as np
import lda
import sqlite3
import json
from sklearn.decomposition import TruncatedSVD
from vocab import Vocabulary
import MySQLdb as mdb
import sys
import random
import cPickle as pickle
from scipy.sparse import lil_matrix, csr_matrix
from path import Path
from argparse import ArgumentParser


def qbquery(num):
    con = mdb.connect(host='localhost', user='vasu', db='quizbowl', passwd='seleniumpython');
    with con:
        cur = con.cursor()
        cur.execute('use quizbowl')
        cur.execute('SELECT question FROM tossup')
        clues = cur.fetchall()
        clues = [c[0].decode('latin-1', 'ignore') for c in clues]
        return clues

def jeoquery(num):
    conn = sqlite3.connect("clues.db")
    c = conn.cursor()
    c.execute("SELECT clue FROM documents")
    clues = c.fetchall()
    clues = [ci[0].encode('ascii', 'ignore') for ci in clues]
    return clues

argparser = ArgumentParser()
argparser.add_argument('--qtype', default="jeo")
argparser.add_argument('--foldername', default="jeodata")
argparser.add_argument('--inputname', default="jeodata")
argparser.add_argument('--inputname2', default="qbdata")
args = argparser.parse_args()
inputpath = Path(args.inputname)
inputpath2 = Path(args.inputname2)
vocab = Vocabulary()

#if args.qtype == "jeo":
    #clues = jeoquery(20000)
#else:
    #clues = qbquery(20000)
clues1 = pickle.load(open(inputpath / "clues.pkl", "rb"))
clues2 = pickle.load(open(inputpath2 / "clues.pkl", "rb"))
oldclues = clues1 + clues2
clues = []
for i in clues1:
    if i not in clues:
        clues.append(i)
for clue in oldclues:
    vocab.add_question(clue)
path = Path(args.foldername)
if not path.exists():
    path.mkdir()
#vocab = Vocabulary.load(inputpath / "vocab.pkl")
vocab.save(path / "vocab.pkl")
print vocab.number
matrix = lil_matrix((len(clues), vocab.number + 1))
matrix = matrix.astype(np.int64)
i = 0
for clue in clues:
    vector = vocab.translate(clue)
    matrix[i] = vector
    i += 1
print matrix.shape
matrix = csr_matrix(matrix)
#svd = TruncatedSVD(n_components=700)
#docs = svd.fit_transform(matrix)
model = lda.LDA(n_topics=10, n_iter=10000)
docs = model.fit_transform(matrix)

top_words = 8

with open(path / "topicslist.txt", "w") as f:
    f.write("Combined List of 10 Topics \n\n")
for i, topic_dist in enumerate(model.topic_word_):
    words = [vocab.number_mapping[w] for w in topic_dist.argsort()[::-1][:top_words]]
    with open(path / "topicslist.txt", "a") as f:
        f.write("Topic %u: %s" % (i, ', '.join(words)) + "\n")
    print "Topic %u: %s" % (i, ', '.join(words))
np.save(path / "docs.npy", docs)
np.save(path / "topics.npy", model.topic_word_)
pickle.dump(clues, open(path / "clues.pkl", "wb"))
#with open(path / "qbtopics.txt", "w") as f:
    #f.write("Jeopardy Topics and Their Questions \n")
#for i in range(7):
    #with open(path / "qbtopics.txt", "a") as f2:
        #f2.write("Topic %d: \n\n" % i)
    #questions = np.argsort(docs.transpose()[i])[::-1][:10]
    #for question in questions:
        #output = clues[question].encode("ascii", "ignore") + "\n\n"
        #with open(path / "qbtopics.txt", "a") as f3:
            #f3.write(output)

