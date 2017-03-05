#! /usr/bin/python
# -*- coding: utf-8 -*-
import networkx as nx
import numpy as np
from math import ceil


def simple_merge(R, S, default=0, return_cycles=False):
    """Simple Merge Algorithm

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

    all_cycles = []

    for cid, cycle in enumerate(cycles):

        w = 0
        inputs = set()
        each_cycle = []

        print ("Cycle %i: (%s)" % (cid + 1, "-".join([str(n) for n in cycle])))

        for i, j in zip(cycle, cycle[1:] + [cycle[0]]):
            inputs.add(min(i, j))
            weight = G[i][j]["weight"]
            color = G[i][j]["color"]
            each_cycle.append({
                (i, j): {"weight": weight, "color": color}
            })
            if color == "red":
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
        all_cycles.append(each_cycle)

    if return_cycles:
        return merged_matching, weights, all_cycles
    return merged_matching, weights


def format_cycle(cycle, N, node_size=1.8):
    """Format cycle"""
    nodes = []
    edges = []

    visited = {}

    n = len(cycle)
    GAP = 4
    vi = 0
    radius = int(ceil(10 * (node_size * (GAP + 1) * n) / (2 * np.pi))) / 10.0
    d_gap = 360.0 / n
    margin = int(ceil(np.arcsin(node_size/2/radius) * 180 / np.pi)) #+ {1:1,0:0}[n <= 4]

    for edge in cycle:
        i, j = edge.keys()[0]
        for k in [i, j]:
            if not (k in visited):
                nodes.append(
                    {
                     'position': int(d_gap * vi),
                     'identity': k,
                     'label': "{}_{}".format({1: 'I', 0: 'O'}[(k < N)],
                                             k - {1: 0, 0: N}[(k < N)] + 1)
                     }
                )
                visited[k] = vi
                vi += 1

        start = nodes[visited[i]]['position'] + margin
        end = nodes[visited[j]]['position'] - margin
        edges.append(
            {
                'start': start,
                'end': end if end > 0 else end + 360,
                'weight': edge[(i, j)]['weight'],
                'color': edge[(i,j)]['color']
            }
        )
    return {
            'cycle':{
                'nodes': nodes,
                'edges': edges
            },
            'node_size': node_size,
            'radius': radius
            }



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














