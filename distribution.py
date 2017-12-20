# coding: utf-8

import networkx as nx
import numpy as np
import random
from scipy.spatial.distance import cosine
from tqdm import tqdm
from collections import Counter
from random_steiner_tree import random_steiner_tree
from random_steiner_tree.util import from_nx

# nx.florentine_families_graph().number_of_nodes()
# nx.davis_southern_women_graph().number_of_nodes()


g = nx.karate_club_graph()
# g = nx.florentine_families_graph()
# g = nx.convert_node_labels_to_integers(g)
print(g.number_of_nodes(), g.number_of_edges())
for u, v in g.edges_iter():
    g[u][v]['weight'] = 1


gi = from_nx(g)


k = 5
X = np.random.permutation(g.number_of_nodes())[:k]
root = random.choice(g.nodes())


N = 100000000
# N = 1000

tree_sizes = [len(random_steiner_tree(gi, X, root))
              for i in tqdm(range(N))]

# df = pd.Series(tree_sizes).to_frame()

def sort_edges(edges):
    return tuple(sorted(edges))

tree_freq = Counter()
for i in tqdm(range(N)):
    edges = sort_edges(random_steiner_tree(gi, X, root))
    tree_freq[edges] += 1


def tree_proba(edges):
    prod = np.product([g.degree(u) for u, v in edges])
    return 1 / prod


probas = np.array([tree_proba(t)
                   for t in tqdm(tree_freq.keys(),
                                 total=len(tree_freq.keys()))])


actual_probas = np.array(list(tree_freq.values())) / N


print('using {} samples on {} terminals, the cosine similarity is {}'.format(
    N, k, 1-cosine(probas, actual_probas)))

