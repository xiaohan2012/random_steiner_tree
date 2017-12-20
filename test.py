import pytest
import random
import numpy as np
import networkx as nx
from random_steiner_tree import random_steiner_tree
from random_steiner_tree.util import from_nx


def check_feasiblility(tree, root, X):
    X = set(X) | {int(root)}
    # number of components
    ncc = nx.number_connected_components(tree)
    assert ncc == 1, 'number_connected_components: {} != 1'.format(ncc)

    nodes = set(tree.nodes())
    assert X.issubset(nodes), 'tree does not contain all X'
    
    # leaves are terminals
    # no extra edges
    for n in tree.nodes_iter():
        if tree.degree(n) == 1:
            assert n in X, 'one leaf does not belong to terminal'


@pytest.fixture
def input_data():
    g = nx.karate_club_graph()
    for u, v in g.edges_iter():
        g[u][v]['weight'] = 1

    return g, from_nx(g, 'weight')


def test_loop_erased_feasiblility(input_data):
    g, gi = input_data
    for i in range(10):
        # try different number of terminals
        for k in range(2, g.number_of_nodes()+1):
            X = np.random.permutation(g.number_of_nodes())[:10]
            root = random.choice(g.nodes())
            tree_edges = random_steiner_tree(gi, X, root, method='loop_erased')
            t = nx.Graph()
            t.add_edges_from(tree_edges)
            check_feasiblility(t, root, X)
