from nltk import word_tokenize
from nltk.corpus import stopwords
import numpy as np
import lda
import sqlite3

counts = {}
conn = sqlite3.connect("clues.db")
c = conn.cursor()

c.execute("SELECT clue FROM documents")
clues = c.fetchall()
c.execute("SELECT answer FROM documents")
answers = c.fetchall()

stop = stopwords.words('english')
for clue in clues:
    counts[clue] = {}
    words = word_tokenize(clue[0])
    words = [x.encode('utf-8') for x in words if x.encode('utf-8').isalpha() and x.encode('utf-8') not in stop]
    for word in words:
        if word not in counts[clue]:
            counts[clue][word] = 0
        counts[clue][word] += 1

print counts
