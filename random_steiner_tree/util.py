from .interface import (build_graph,
                        isolate_vertex,
                        vertices,
                        edges,
                        num_vertices,
                        reachable_vertices)


def nx2edges_and_weights(g, weight='weight'):
    """
    args:
    
    g: networkx.Graph|DiGraph
    weight: attribute name for edge weight

    return:

    list of (source, target, weight)
    """
    return [(e[0], e[1], g[e[0]][e[1]].get(weight, 1))
            for e in g.edges_iter()]


def from_nx(g, weight='weight'):
    return build_graph(g.number_of_nodes(),
                       nx2edges_and_weights(g, weight))


def gt2edges_and_weights(g, weights):
    """
    args:
    g: graph_tool.Graph
    weights: list of edge weight, edge order should be the same g.get_edges()
    returns:
    
    list of (source, target, weight)
    """
    from graph_tool import PropertyMap
    if isinstance(weights, PropertyMap):  # convert to np.ndarray if necessary
        weights = weights.a
    elif weights is None:
        weights = [1] * g.num_edges()

    assert g.num_edges() == len(weights)

    return [(e[0], e[1], w)
            for e, w in zip(g.get_edges(), weights)]


def from_gt(g, weights=None):
    """weights: edge weights, PropertyMap or np.ndarray
    """
    return build_graph(g.num_vertices(),
                       gt2edges_and_weights(g, weights))
