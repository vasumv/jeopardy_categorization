mport random
def euclidean_distance(prefs, vec1, vec2):
    si = {}
    for item in prefs[vec1]:
        if item in prefs[vec2]:
            si[item] = 1
    if len(si) == 0:
        return 0
    sum_of_squares = sum([pow(prefs[vec1][item] - prefs[vec2][item], 2) for item in si])
    return 1 / (1 + sqrt(sum_of_squares))

def pearson(prefs, vec1, vec2):
    si = {}
    for item in prefs[vec1]:
        if item in prefs[vec2]:
            si[item] = 1
    n = len(si)
    if n == 0:
        return 0
    sum1 = sum([prefs[vec1][item] for item in si])
    sum2 = sum([prefs[vec2][item] for item in si])
    sum1sq = sum([pow(prefs[vec1][item], 2) for item in si])
    sum2sq = sum([pow(prefs[vec2][item], 2) for item in si])
    p_sum = sum([prefs[vec1][item] * prefs[vec2][item] for item in si])
    num = p_sum - (sum1 * sum2 / n)
    den = sqrt((sum1sq - pow(sum1, 2) / n) * (sum2sq - pow(sum2, 2) / n))
    if den == 0:
        return 0
    r = num / den
    return r

def kcluster(rows,distance = pearson, k=3):
    ranges = [(min([row[i] for row in rows]), max([row[i] for row in rows])) for i in range(len(rows[0]))]
    clusters = [[random.random() * (ranges[i][1] - ranges[i][0]) + ranges[i][0] for i in range(len(rows[0]))] for j in range(k)]
    lastmatches = None
    for t in range(100):
        print 'Iteration %d' % t
        bestmatches = [[] for i in range(k)]
        for j in range(len(rows)):
            row = rows[j]
            bestmatch = 0
            for i in range(k):
                d = distance(clusters[bestmatch], row)
                if d < distance(clusters[bestmatch], row):
                    bestmatch = i
            bestmatches[bestmatch].append(j)
        if bestmatches == lastmatches:
            break
        lastmatches = bestmatches
    for i in range(k):
        avgs = [0.0] * len(rows[0])
        if len(bestmatches[i]) > 0:
            for rowid in bestmatches[i]:
                for m in range(len(rows[rowid])):
                    avgs[m] += rows[rowid][m]
            for j in range(len(avgs)):
                avgs[j] /= len(bestmatches[i])
            clusters[i] = avgs
    return bestmatches
