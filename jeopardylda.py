from nltk import word_tokenize
from nltk.corpus import stopwords
import numpy as np
import lda
import sqlite3
import json

counts = {}
conn = sqlite3.connect("clues.db")
c = conn.cursor()
clues_id = {}
c.execute("SELECT clues.id FROM clues")
clue_ids = c.fetchall()
clue_ids = [x[0] for x in clue_ids]
c.execute("SELECT answer FROM documents")
answers = c.fetchall()
clues = []
#for id in clue_ids:
    #c.execute(" SELECT clue FROM clues JOIN documents ON clues.id = documents.id WHERE clues.id = %d" % id)
    #clues_id[id] = c.fetchone()[0]
#stop = stopwords.words('english')
#for id, clue in clues_id.items()[0:500]:
    #counts[id] = {}
    #words = word_tokenize(clue)
    #words = [x.encode('utf-8') for x in words if x.encode('utf-8').isalpha() and x.encode('utf-8') not in stop]
    #for word in words:
        #if word not in counts[id]:
            #counts[id][word] = 0
        #counts[id][word] += 1
with open("lesscounts.json", "r") as fp:
    counts = json.loads(fp.read())
#less = {k:v for k, v in counts.items()[0:500]}
#with open("lesscounts.json", "w") as f:
    #f.write(json.dumps(less, sort_keys=True,indent=4, separators=(',', ': ')))
total = 0
for id in counts:
    total += len(counts[id].values())
matrix = np.zeros([len(counts.keys()), total])
for row in matrix:
    for id in counts:
        row[0:len(counts[id].values())] = counts[id].values()
U, s, V = np.linalg.svd(matrix, full_matrices=True)
print U.shape, s.shape, V.shape
#with open("counts.json", "w") as f:
    #f.write(json.dumps(counts, sort_keys=True,indent=4, separators=(',', ': ')))p
