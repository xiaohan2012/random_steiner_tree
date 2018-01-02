import pytest
import random
import numpy as np
import networkx as nx
from graph_tool import Graph
from random_steiner_tree import random_steiner_tree
from random_steiner_tree.util import from_nx, from_gt


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


def input_data_nx():
    g = nx.karate_club_graph()
    for u, v in g.edges_iter():
        g[u][v]['weight'] = 1

    return g, from_nx(g, 'weight'), g.number_of_nodes()


def input_data_gt():
    g_nx = nx.karate_club_graph()
    g = Graph(directed=False)
    g.add_vertex(g_nx.number_of_nodes())
    for u, v in g_nx.edges():
        g.add_edge(u, v)

    return g, from_gt(g, None), g.num_vertices()


@pytest.mark.parametrize("data_type", ["nx", "gt"])
@pytest.mark.parametrize("method", ["loop_erased", "cut"])
def test_feasiblility(data_type, method):
    if data_type == 'nx':
        data = input_data_nx()
    elif data_type == 'gt':
        data = input_data_gt()
    g, gi, N = data
    for i in range(10):
        # try different number of terminals1
        for k in range(2, N+1):
            X = np.random.permutation(N)[:10]

            if data_type == 'nx':
                nodes = g.nodes()
            elif data_type == 'gt':
                nodes = list(map(int, g.vertices()))

            root = random.choice(nodes)
            tree_edges = random_steiner_tree(gi, X, root, method=method)
            t = nx.Graph()
            t.add_edges_from(tree_edges)
            check_feasiblility(t, root, X)
            
