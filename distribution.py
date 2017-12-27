# coding: utf-8

import networkx as nx
import numpy as np
import random
import pandas as pd
from scipy.spatial.distance import cosine
from tqdm import tqdm
from collections import Counter
from random_steiner_tree import random_steiner_tree
from random_steiner_tree.util import from_nx
from joblib import Parallel, delayed

# random.seed(1)
# np.random.seed(1)
# nx.florentine_families_graph().number_of_nodes()
# nx.davis_southern_women_graph().number_of_nodes()


# g = nx.karate_club_graph()
g = nx.florentine_families_graph()
g = nx.convert_node_labels_to_integers(g)

# add some random edges
n_rand_edges = 5
for i in range(n_rand_edges):
    while True:
        u, v = map(int, np.random.permutation(g.nodes())[:2])
        if not g.has_edge(u, v):
            g.add_edge(u, v)
            break
        # u, v = random.choice(g.nodes()), random.choice(g.nodes())

print(g.number_of_nodes(), g.number_of_edges())
for u, v in g.edges_iter():
    g[u][v]['weight'] = 1


def one_run(g, k, N):
    gi = from_nx(g)
    X = np.random.permutation(g.number_of_nodes())[:k]
    root = random.choice(g.nodes())
    # tree_sizes = [len(random_steiner_tree(gi, X, root))
    #               for i in tqdm(range(N))]

    def sort_edges(edges):
        return tuple(sorted(edges))

    tree_freq = Counter()
    # for i in tqdm(range(N)):
    for i in range(N):
        edges = sort_edges(random_steiner_tree(gi, X, root))
        tree_freq[edges] += 1

    def tree_proba(edges):
        prod = np.product([g.degree(u) for u, v in edges])
        return 1 / prod

    probas = np.array([tree_proba(t)
                       for t in tree_freq.keys()])
                       # for t in tqdm(tree_freq.keys(),
                       #               total=len(tree_freq.keys()))])
    probas /= probas.sum()
    actual_probas = np.array(list(tree_freq.values())) / N

    # print('using {} samples on {} terminals, the cosine similarity is {}'.format(
    #     N, k, 1-cosine(probas, actual_probas)))

    return 1-cosine(probas, actual_probas)

k = 5
N = 10000000
# N = 10000
n_rounds = 800
sims = Parallel(n_jobs=-1)(delayed(one_run)(g, k, N)
                           for i in range(n_rounds))


print(pd.Series(sims).describe())
