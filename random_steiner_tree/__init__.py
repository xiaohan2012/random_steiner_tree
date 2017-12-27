import random
from .interface import loop_erased, cut_based


def random_steiner_tree(gi, X, root, method="loop_erased", seed=None):
    assert method in {"loop_erased", "closure", "cut"}
    # C++ is strict with type...
    X = list(map(int, X))

    root = int(root)
    if seed is None:
        seed = random.randint(0, 2147483647)  # int32
    if method == "loop_erased":
        return loop_erased(gi, X, root, seed)
    elif method == "cut":
        return cut_based(gi, X, root, seed)
    else:
        raise NotImplemented('yet')
