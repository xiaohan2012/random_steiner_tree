import pytest
import numpy as np
from graph_tool import Graph
from random_steiner_tree import random_steiner_tree
from random_steiner_tree.util import from_gt
from collections import Counter

EPSILON = 1e-10


def graph():
    """    
       0 (root)
      / \
     1   2
      \ /
       3 (X)
    """
    g = Graph()
    g.add_vertex(4)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 3)
    return g


case1 = {
    (0, 1): 1,
    (0, 2): EPSILON,
    (1, 3): 1,
    (2, 3): EPSILON
}

case2 = {
    (0, 1): 1,
    (0, 2): 2,
    (1, 3): 1,
    (2, 3): 1
}


def build_gi_by_weights(edge2weight):
    g = graph()
    weights = g.new_edge_property('float')
    for (u, v), w in edge2weight.items():
        weights[g.edge(u, v)] = w
    
    return from_gt(g, weights=weights)
    

@pytest.mark.parametrize("edge2weight,expected_fraction", [(case1, 0), (case2, 4/3)])
@pytest.mark.parametrize("sampling_method", ["loop_erased"])
def test_distribution(edge2weight, expected_fraction, sampling_method):
    gi = build_gi_by_weights(edge2weight)
    root = 0
    X = [3]
    n = 100000
    steiner_node_freq = Counter()
    for i in range(n):
        edges = random_steiner_tree(gi, X, root, method=sampling_method, seed=None)
        steiner_nodes = {u for e in edges for u in e} - {root} - set(X)
        for u in steiner_nodes:
            steiner_node_freq[u] += 1

    np.testing.assert_almost_equal(steiner_node_freq[2] / steiner_node_freq[1],
                                   expected_fraction, decimal=2)

    # if the following assertion fails, you can buy a lottery
    # assert steiner_node_freq[2] == 0
    # assert steiner_node_freq[1] == n

    # np.testing.assert_almost_equal(steiner_node_freq[2] / steiner_node_freq[1], 0)
