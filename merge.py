#! /usr/bin/python
# -*- coding: utf-8 -*-
import networkx as nx


def simple_merge(R, S, default=0):
    """Simple Merge ALgorithm

    Parameters
    ----------
    R : tuple
       The random matching (with weight), the matching
       is simply described by a permutation with weights,
       which has two elements, the first one is the
       permutation described by a list, the second one is
       a dict for weight
    S : tuple
       similar as R
    default : int
      Under the circumference of ties, which one should be
      choose

    Note that, in the dict for weight, the key is the identity of
    the input port of the corresponding edge in the matching.
    The idea of MERGE was first proposed in [1]

    For example,
    simple_merge(([0, 1, 2], {0: 10, 1: 20, 2: 15}),
    ([2, 0, 1], {0: 30, 1: 6, 2: 13}))

    Returns
    -------
    merged_matching : list
        The resulted matching described in a permutation
    weights: dict
        weight associated with each edge

    .. [1] P. Giaccone, B. Prabhakar, and D. Shah, “Randomized scheduling
       algorithms for high-aggregate bandwidth switches,” IEEE Journal on
       Selected Areas in Communications, vol. 21, no. 4, pp. 546–559, 2003.
    """

    N = len(R[0])
    red = R[1]
    green = S[1]

    G = nx.DiGraph()
    for i in xrange(2*N):
        G.add_node(i)
    for i, o in enumerate(R[0]):
        G.add_edge(i, o + N, weight=R[1][i], color="red")
    for i, o in enumerate(S[0]):
        G.add_edge(o + N, i, weight=S[1][i], color="green")

    cycles = nx.simple_cycles(G)
    merged_matching = [-1] * N
    weights = {}

    for cid, cycle in enumerate(cycles):

        w = 0
        inputs = []

        print ("Cycle %i: (%s)" % (cid + 1, "-".join([str(n) for n in cycle])))

        for i, j in zip(cycle, cycle[1:] + [cycle[0]]):
            inputs.append(min(i, j))
            weight = G[i][j]["weight"]
            if G[i][j]["color"] == "red":
                w += weight
            else:
                w -= weight
        if w > 0:
            choice = R
        elif w < 0:
            choice = S
        else:
            choice = R if default == 0 else S
    
        for i in inputs:
            merged_matching[i] = choice[0][i]
            weights[i] = choice[1][i]
    return merged_matching, weights


# if __name__ == "__main__":
#     import numpy as np
#     N = 8
#     R = (np.random.permutation(N).tolist(), dict(zip(range(N),
#         np.random.randint(1, high=10,size=N))))
#     S = (np.random.permutation(N).tolist(), dict(zip(range(N),
#         np.random.randint(1, high=10,size=N))))
#     print ("Random matching: %s" % str(R))
#     print ("Previous matching: %s" % str(S))
#     print ("Merged matching: %s" % str(simple_merge(R, S)))














