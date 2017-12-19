import numpy as np
import networkx as nx
from util import from_nx
from interface import get_random_steiner_tree


g = nx.karate_club_graph()
for u, v in g.edges_iter():
    g[u][v]['weight'] = 1

X = list(map(int, np.random.permutation(g.number_of_nodes())[:10]))  # wierd

print(X)

gi = from_nx(g, 'weight')
root = int(X[0])
seed = 1
tree_edges = get_random_steiner_tree(gi, X, root, seed)

print(tree_edges)
