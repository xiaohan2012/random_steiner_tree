from .interface import build_graph


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
