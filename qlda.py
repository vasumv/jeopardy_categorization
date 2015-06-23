import numpy as np
import lda
import sqlite3
import json
from sklearn.decomposition import TruncatedSVD
from vocab import Vocabulary
import MySQLdb as mdb
import sys
import random
from scipy.sparse import lil_matrix, csr_matrix


def qbquery(num):
    con = mdb.connect(host='localhost', user='vasu', db='quizbowl', passwd='seleniumpython');
    with con:
        cur = con.cursor()
        cur.execute('use quizbowl')
        cur.execute('SELECT question FROM tossup LIMIT %d' % num)
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

vocab = Vocabulary()

clues = jeoquery(20000)
for clue in clues:
    vocab.add_question(clue)
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

for i, topic_dist in enumerate(model.topic_word_):
    words = [vocab.number_mapping[w] for w in topic_dist.argsort()[::-1][:top_words]]
    print "Topic %u: %s" % (i, ', '.join(words))
