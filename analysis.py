import numpy as np
import lda
from sklearn.decomposition import TruncatedSVD
from vocab import Vocabulary
from scipy.sparse import lil_matrix, csr_matrix
from path import Path
from argparse import ArgumentParser
from math import log
import cPickle as pickle
def cross_entropy(vect1, vect2):
    entropy = 0
    for i in range(len(vect1)):
        entropy += (-1) * vect1[i] * log(vect2[i])
    return entropy

if __name == "__main__":

    argparser = ArgumentParser()
    argparser.add_argument('--qtype', default="qb")
    argparser.add_argument('--inputname', default="combined_jeo")
    argparser.add_argument('--inputname2', default="combined_both")
    argparser.add_argument('--foldername', default="qbsub7")
    args = argparser.parse_args()
    path = Path(args.foldername)
    if not path.exists():
        path.mkdir()
    with open("%s/clues.pkl" % args.inputname, "rb") as f:
        clues = pickle.load(f)
    topics = np.load("%s/topics.npy" % args.inputname)
    topics2 = np.load("%s/topics.npy" % args.inputname2)
    vect1 = topics[]

