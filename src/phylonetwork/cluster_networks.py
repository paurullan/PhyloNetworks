#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division

import operator

import networkx as nx

from hasse import Hasse


def construct(clusters):
    if len(clusters) == 1 and not clusters[0]:
        return nx.DiGraph()
    # the first net is the created from the Hasse, the second the real hybrid
    net = network(Hasse(clusters))
    hybrid = calc_hybrid(net)
    return hybrid


def network(edge_list):
    """
    Alias for creating a graph from a list of edges
    """
    G = nx.DiGraph()
    G.add_edges_from(edge_list) #, name="", group=1)
    return G

def make_d3_ready(G):
    """
    https://github.com/mbostock/d3/wiki/Ordinal-Scales#categorical-colors
    blue, orange, green, red, purple, brown, pink, grey, lime, cyan
    """
    for node in G.nodes_iter():
        G.node[node]['name'] = str(node)
    for node in get_non_leaf_nodes(G):
        G.node[node]['group'] = 1
    for node in get_leaf_nodes(G):
        G.node[node]['group'] = 2
    for node in hybrid_nodes(G):
        G.node[node]['group'] = 3
    for node in get_root_nodes(G):
        G.node[node]['group'] = 4
    return G


def clean_graph(G):
    """
    Streams and cleans a graph that has become polluted from transformations
    of the tree child process. Not pure, removes in place.
    """

    def _may_go(G, n):
        return G.in_degree(n) == 1 and G.out_degree(n) == 1

    candidates = [n for n in G.nodes() if _may_go(G, n)]
    if not candidates:
        return G
    else:
        node = candidates[0]
        # let's remove the node and change the in-out
        assert(len(G.predecessors(node)) == 1)
        assert(len(G.successors(node)) == 1)
        in_node = G.predecessors(node)[0]
        out_node = G.successors(node)[0]
        G.add_edge(in_node, out_node,  name="", group=1)
        G.remove_node(node)
        return clean_graph(G)


def _translate(G, node):
    assert(G.in_degree(node) > 1)
    if len(node) == 1:
        return (str(node[0]) + 'h', )
    else:
        val = tuple(sorted(node))
        return (str(val) + 'h', )


def calc_hybrid(G):
    """
    Gets a network, looks for all nodes that have multiple parents and makes
    the hybrid network.
    """
    hybrids = hybrid_nodes(G)
    translation = {n: _translate(G, n) for n in hybrids}
    new = []
    for x, y in G.edges():
        new_y = translation.get(y, y)
        new.append((x, new_y))
    for node, hybrid in translation.items():
        new.append((hybrid, node))
    return network(new)


def is_treechild(G):
    """ We take all the nodes but the root. """
    non_leaf_nodes = get_non_leaf_nodes(G)
    return all([has_tree_child(G, n) for n in non_leaf_nodes])

def get_root_nodes(G):
    return [n for n in G.nodes() if len(G.predecessors(n)) == 0]

def get_leaf_nodes(G):
    return [n for n in G.nodes() if len(G.successors(n)) == 0]

def get_non_leaf_nodes(G):
    return [n for n in G.nodes() if len(G.successors(n)) > 0]


def has_tree_child(G, n):
    return any([node_tree(G, child) for child in G.successors(n)])


def hybrid_nodes(G):
    return [n for n in G.nodes() if node_hybrid(G, n)]


def node_hybrid(G, n):
    return G.in_degree(n) > 1


def node_tree(G, n):
    return G.in_degree(n) <= 1


def _leafes_from(G, node):
    if not G.successors(node):
        return node
    else:
        leafes = [_leafes_from(G, n) for n in G.successors(node)]
        T = []
        for leafe in leafes:
            if len(leafe) == 1:
                T.append(leafe)
            else:
                T += leafe[:]
        return T


def _make_set(leaf_list):
    return set(zip(*sorted(leaf_list)))


def calc_hard_cluster(G_orig):
    G = clean_graph(G_orig.copy())
    leafs = set(get_leaf_nodes(G))
    root = _make_set([n for n in get_leaf_nodes(G)])
    hard = leafs.copy()
    hard.update(root)
    for node in get_non_leaf_nodes(G):
        leafs = _leafes_from(G, node)
        leafs_set = _make_set(leafs)
        hard.update(leafs_set)
    return hard


def potential_number_of_calls(G):
    """
    The potential number of calls for a soft_cluster is the product of the
    many hybrid nodes by their input level.
    """
    H = hybrid_nodes(G)
    return reduce(operator.mul, [len(G.predecessors(h)) for h in H])


def calc_soft_cluster(G):
    return soft_cluster(G, set())


def check_cluster(clusters):
    """
    Checks if the C_soft(N) == C_hard(N) of a network.
    """
    G = construct(clusters)
    return calc_hard_cluster(G) == calc_soft_cluster(G)


def soft_cluster(G, results):
    """
    Calculate the softcluster of the graph. It is important to take into
    account that we cannot just remove one of the predecessors since it will
    be an usual case were an hybrid node has three predecessors.
    """
    if not hybrid_nodes(G):
        results.update(calc_hard_cluster(G))
    else:
        h = hybrid_nodes(G)[0]
        preds = G.predecessors(h)
        assert len(preds) > 1, "Always and at least two predecessors"
        assert len(G.successors(h)) == 1, "Only one successor on hybrids"
        successor = G.successors(h)[0]
        for predecessor in preds:
            g = G.copy()
            g.remove_node(h)
            g.add_edge(predecessor, successor,  name="", group=1)
            g = clean_graph(g)
            soft_cluster(g, results)
    return results




def calc_soft_cluster_lift(G):
    g = G.copy()
    for node in g.nodes():
        node.soft = set()
    for leaf in get_leaf_nodes(g):
        leaf.soft.add(str(leaf))
    for hybrid in hybrid_nodes(g):
        hybrid.soft.add(set())
    val = soft_lift(g)
    return val


def soft_lift(G):
    if len(G.nodes()) == 1:
        return G.nodes()[0].soft
    for leaf in get_leaf_nodes(G):
        for pred in G.predecessors(leaf):
            pred.soft.update(leaf.soft)
        G.remove(leaf)
    return soft_lift(G)
