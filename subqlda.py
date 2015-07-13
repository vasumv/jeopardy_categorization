import numpy as np
import lda
from sklearn.decomposition import TruncatedSVD
from vocab import Vocabulary
from scipy.sparse import lil_matrix, csr_matrix
from path import Path
from argparse import ArgumentParser
import cPickle as pickle

argparser = ArgumentParser()
argparser.add_argument('--qtype', default="qb")
argparser.add_argument('--inputname', default="qbdata7")
argparser.add_argument('--foldername', default="qbsub7")
argparser.add_argument('--numtopics', default=10)
args = argparser.parse_args()
path = Path(args.foldername)
if not path.exists():
    path.mkdir()
with open("%s/clues.pkl" % args.inputname, "rb") as f:
    clues = pickle.load(f)
docs = np.load("%s/docs.npy" % args.inputname)
topics = np.load("%s/topics.npy" % args.inputname)
for i in range(int(args.numtopics)):
    print "ITERATION %d" % i
    subclues = []
    for num in np.argsort(docs.transpose()[i])[::-1]:
        if docs.transpose()[i][num] < 0.5:
            continue
        subclues.append(clues[num])
    newvocab = Vocabulary()
    for clue in subclues:
        newvocab.add_question(clue)
    print newvocab.number
    matrix = lil_matrix((len(subclues), newvocab.number + 1))
    matrix = matrix.astype(np.int64)
    j = 0
    for clue in subclues:
        vector = newvocab.translate(clue)
        matrix[j] = vector
        j += 1
    print matrix.shape
    matrix = csr_matrix(matrix)
    #svd = TruncatedSVD(n_components=700)
    #docs = svd.fit_transform(matrix)
    model = lda.LDA(n_topics=10, n_iter=10000)
    subdocs = model.fit_transform(matrix)
    top_words = 8
    with open(path / "topic%s.txt" % i, "w") as f:
        f.write("List of Subtopics \n\n")
    for k, topic_dist in enumerate(model.topic_word_):
        words = [newvocab.number_mapping[w] for w in topic_dist.argsort()[::-1][:top_words]]
        with open(path / "topic%s.txt" % i, "a") as f:
            f.write("Topic %u: %s" % (k, ', '.join(words)))
            f.write("\n")
    #np.save(path / "docs.npy", subdocs)
    #np.save(path / "topics.npy", model.topic_word_)
#with open(path / "topicslist.txt", "w") as f:
    #f.write("Quizbowl Topics and Their Questions \n")
#for i in range(10):
    #with open("topicslist.txt", "a") as f2:
        #f2.write("Topic %d: \n\n" % i)
    #questions = np.argsort(subdocs.transpose()[i])[::-1][:10]
    #for question in questions:
        #output = subclues[question].encode("ascii", "ignore") + "\n\n"
        #with open("topicslist.txt", "a") as f3:
            #f3.write(output)
