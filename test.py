import pytest
import random
import numpy as np
import networkx as nx
from graph_tool import Graph
from random_steiner_tree import random_steiner_tree
from random_steiner_tree.util import (from_nx, from_gt,
                                      num_vertices,
                                      isolate_vertex,
                                      vertices,
                                      reachable_vertices)


def check_feasiblity(tree, root, X):
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
            check_feasiblity(t, root, X)


def test_isolate_vertex_num_verticesx():
    _, gi, _ = input_data_gt()
    prev_N = num_vertices(gi)
    isolate_vertex(gi, 0)
    assert prev_N == num_vertices(gi)
    isolate_vertex(gi, 1)
    assert prev_N == num_vertices(gi)


@pytest.fixture
def disconnected_line_graph():
    g = nx.Graph()
    g.add_nodes_from([0, 1, 2, 3, 4])
    g.add_edges_from([(0, 1), (1, 2), (3, 4)])
    return from_nx(g)


def test_remove_vertex_node_index(disconnected_line_graph):
    gi = disconnected_line_graph
    isolate_vertex(gi, 0)
    assert set(vertices(gi)) == {0, 1, 2, 3, 4}

    assert reachable_vertices(gi, 0) == [0]
    assert reachable_vertices(gi, 1) == [1, 2]
    assert reachable_vertices(gi, 3) == [3, 4]

    
@pytest.mark.parametrize("expected, pivot", [({0, 1, 2}, 1), ({3, 4}, 3)])
def test_reachable_vertices(disconnected_line_graph, expected, pivot):
    gi = disconnected_line_graph
    nodes = reachable_vertices(gi, pivot)
    print('num_vertices', num_vertices(gi))
    # 0, 1, 2 remains
    assert set(nodes) == expected


@pytest.mark.parametrize("method", ['cut', 'loop_erased'])
def test_steiner_tree_with_disconnected_component(disconnected_line_graph, method):
    gi = disconnected_line_graph
    edges = random_steiner_tree(gi, X=[0, 2], root=1, method=method)
    assert set(edges) == {(1, 0), (1, 2)}
