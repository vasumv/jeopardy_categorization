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
for id in clue_ids:
    c.execute(" SELECT clue FROM clues JOIN documents ON clues.id = documents.id WHERE clues.id = %d" % id)
    clues_id[id] = c.fetchone()[0]
stop = stopwords.words('english')
for id, clue in clues_id.items():
    counts[id] = {}
    words = word_tokenize(clue)
    words = [x.encode('utf-8') for x in words if x.encode('utf-8').isalpha() and x.encode('utf-8') not in stop]
    for word in words:
        if word not in counts[id]:
            counts[id][word] = 0
        counts[id][word] += 1
with open("counts.json", "w") as f:
    f.write(json.dumps(counts, sort_keys=True,indent=4, separators=(',', ': ')))
