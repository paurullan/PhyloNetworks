#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint

from hasse import Hasse


def total_cmp(x,y):
    """
    Return -1 if x<y, 0 if x=y, 1 if x>y, with respect to the product partial
    order.
    """
    nx=x.size
    ny=y.size
    if nx < ny: return -1
    if nx > ny: return 1
    for i in range(nx):
        if x[i]<y[i]: return -1
        if x[i]>y[i]: return 1
    return 0


def random_weighted(d):
    """Given ``d`` a dictionary, returns a key in it with probability equals to its value
    (normalized over the sum of all values)
    """
    sum_of_values = sum(d.values())
    r = randint(0,sum_of_values-1)
    for item in d:
        if r < d[item]:
            return item
        r = r-d[item]



def construct(clusters):
    from classes import PhyloNetwork
    if len(clusters) == 1 and not clusters[0]:
        return PhyloNetwork()
    # the first net is the created from the Hasse, the second the real hybrid
    net = network(Hasse(clusters))
    hybrid = net.calc_hybrid()
    return hybrid


def network(edge_list):
    """
    Alias for creating a graph from a list of edges
    """
    from classes import PhyloNetwork
    G = PhyloNetwork()
    G.add_edges_from(edge_list) #, name="", group=1)
    return G


def make_d3_ready(G):
    """
    https://github.com/mbostock/d3/wiki/Ordinal-Scales#categorical-colors
    blue, orange, green, red, purple, brown, pink, grey, lime, cyan
    """
    for node in G.nodes_iter():
        G.node[node]['name'] = str(node)
    for node in G.get_non_leaf_nodes():
        G.node[node]['group'] = 1
    for node in G.get_leaf_nodes():
        G.node[node]['group'] = 2
    for node in G.hybrid_nodes():
        G.node[node]['group'] = 3
    for node in G.get_root_nodes():
        G.node[node]['group'] = 4
    return G


def check_cluster(clusters):
    """
    Checks if the C_soft(N) == C_hard(N) of a network.
    """
    G = construct(clusters)
    return G.hard_cluster() == G.soft_cluster()
