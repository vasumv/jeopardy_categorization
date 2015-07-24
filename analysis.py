import numpy as np
import lda
import hungarian
import matplotlib.pyplot as plt
from sklearn.decomposition import TruncatedSVD, PCA
from sklearn.cluster import KMeans
from vocab import Vocabulary
from scipy.sparse import lil_matrix, csr_matrix
from path import Path
from argparse import ArgumentParser
from math import log
import cPickle as pickle

def euclidean_distance(vect1, vect2):
    return np.linalg.norm(vect1 - vect2)

def cross_entropy(vect1, vect2):
    entropy = 0
    for i in range(len(vect1)):
        entropy += (-1) * vect1[i] * log(vect2[i])
    return entropy

if __name__ == "__main__":

    argparser = ArgumentParser()
    argparser.add_argument('--qtype', default="qb")
    argparser.add_argument('--inputname', default="jeo_combined_naqt")
    argparser.add_argument('--inputname2', default="naqt_combined_jeo")
    argparser.add_argument('--inputname3', default="hungarian")
    argparser.add_argument('--foldername', default="hungarian_results")
    args = argparser.parse_args()
    path = Path(args.foldername)
    if not path.exists():
        path.mkdir()
    #with open("%s/clues.pkl" % args.inputname, "rb") as f:
        #clues = pickle.load(f)
    topics = np.load("%s/topics.npy" % args.inputname)
    topics2 = np.load("%s/topics.npy" % args.inputname2)
    print topics.shape, topics2.shape
    matrix = np.zeros((len(topics), len(topics2)))
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            #matrix[i][j] = euclidean_distance(topics[i], topics2[j])
            matrix[i][j] = cross_entropy(topics[i], topics2[j]) + cross_entropy(topics2[j], topics[i])
    matches = hungarian.lap(matrix)
    matches_dict = {}
    for i in range(len(matches[0])):
        matches_dict[i] = matches[0][i]
    print matches_dict
    #matches = pickle.load(open("%s/matches.pkl" % args.inputname3, "rb"))
    total  = 0
    for i in range(len(matches[0])):
        total += cross_entropy(topics[i], topics2[matches[0][i]]) + cross_entropy(topics2[matches[0][i]], topics[i])
    print total
