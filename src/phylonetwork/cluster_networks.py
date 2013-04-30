#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division

import operator


class ClusterNetworkMixin(object):

    def get_root_nodes(self):
        return [n for n in self.nodes() if len(self.predecessors(n)) == 0]

    def get_leaf_nodes(self):
        return [n for n in self.nodes() if len(self.successors(n)) == 0]

    def get_non_leaf_nodes(self):
        return [n for n in self.nodes() if len(self.successors(n)) > 0]


    def hybrid_nodes(self):
        return [n for n in self.nodes() if self.node_hybrid(n)]


    def has_tree_child(self, n):
        return any([self.node_tree(child) for child in self.successors(n)])


    def node_hybrid(self, n):
        return self.in_degree(n) > 1


    def node_tree(self, n):
        return self.in_degree(n) <= 1

    def is_treechild(self):
        """ We take all the nodes but the root. """
        non_leaf_nodes = self.get_non_leaf_nodes()
        return all([self.has_tree_child(n) for n in non_leaf_nodes])

    def _leafes_from(self, node):
        succs = self.successors(node)
        if not succs:
            return node
        else:
            leafes = [self._leafes_from(n) for n in succs]
            T = []
            for leafe in leafes:
                if type(leafe) == list and len(leafe) == 1:
                    T.append(leafe[0])
                elif  len(leafe) == 1:
                    T.append(leafe)
                else:
                    T += leafe[:]
        return T

    def calc_hybrid(self):
        """
        Gets a network, looks for all nodes that have multiple parents and makes
        the hybrid network.
        """

        def _translate(G, node):
            assert(G.in_degree(node) > 1)
            if len(node) == 1:
                return (str(node[0]) + 'h', )
            else:
                val = tuple(sorted(node))
                return (str(val) + 'h', )

        hybrids = self.hybrid_nodes()
        translation = {n: _translate(self, n) for n in hybrids}
        new = []
        for x, y in self.edges():
            new_y = translation.get(y, y)
            new.append((x, new_y))
            for node, hybrid in translation.items():
                new.append((hybrid, node))
        G = self.__class__()
        G.add_edges_from(new)
        return G

    def potential_number_of_calls(self):
        """
        The potential number of calls for a soft_cluster is the product of the
        many hybrid nodes by their input level.
        """
        H = self.hybrid_nodes()
        return reduce(operator.mul, [len(self.predecessors(h)) for h in H])


    def clean_graph(self):
        """
        Streams and cleans a graph that has become polluted from transformations
        of the tree child process. Not pure, removes in place.
        """

        def _may_go(self, n):
            return self.in_degree(n) == 1 and self.out_degree(n) == 1

        candidates = [n for n in self.nodes() if _may_go(self, n)]
        if not candidates:
            return self
        else:
            node = candidates[0]
            # let's remove the node and change the in-out
            assert(len(self.predecessors(node)) == 1)
            assert(len(self.successors(node)) == 1)
            in_node = self.predecessors(node)[0]
            out_node = self.successors(node)[0]
            self.add_edge(in_node, out_node,  name="", group=1)
            self.remove_node(node)
            return self.clean_graph()

    def hard_cluster(self):
        # TODO revisar implementació
        def _make_set(leaf_list):
            return set(zip(*sorted(leaf_list)))
        leafs = set(self.get_leaf_nodes())
        root = _make_set([n for n in self.get_leaf_nodes()])
        hard = leafs.copy()
        hard.update(root)
        for node in self.get_non_leaf_nodes():
            leafs = self._leafes_from(node)
            leafs_set = _make_set(leafs)
            hard.update(leafs_set)
        return hard


    def soft_cluster(self, results=None):
        """
        Calculate the softcluster of the graph. It is important to
        take into account that we cannot just remove one of the
        predecessors since it will be an usual case were an hybrid
        node has three predecessors.
        """
        results = set() if not results else results
        if not self.hybrid_nodes():
            results.update(self.hard_cluster())
        else:
            h = self.hybrid_nodes()[0]
            preds = self.predecessors(h)
            successor = self.successors(h)[0]
            assert len(preds) > 1, "Always at least two predecessors"
            assert len(self.successors(h)) == 1, \
                "Only one successor on hybrids"
            for predecessor in preds:
                g = self.copy()
                g.remove_node(h)
                g.add_edge(predecessor, successor,  name="", group=1)
                g = g.clean_graph()
                results.update(g.soft_cluster(results))
        return results

    def make_web_ready(self):
        for node in self.nodes_iter():
            self.node[node]['label'] =  ", ".join(map(str, node))
        for node in self.get_non_leaf_nodes():
            self.node[node]['color'] = "black"
        for node in self.get_leaf_nodes():
            self.node[node]['color'] = "blue"
        for node in self.hybrid_nodes():
            self.node[node]['color'] = "green"
        for node in self.get_root_nodes():
            self.node[node]['color'] = "red"

    def get_removable_edges(self):
        edges = []
        for node in self.hybrid_nodes():
            for edge in self.input(node):  # edges in
                if self.remove_edge(edge):
                    edges.append(edge)
                    break


    def can_remove_edge(self, edge):
        """
        Calculate the possibility of removing this edge while keeping
        the graph with the same soft_cluster output.
        """
        pass
        nodes = un_node_amb_tots_els_fill_hibrids(G)
        node = nodes[0]
        pares = self.predecessors(node)
        pares_arbres = [te_un_full_arbre(pare) for pare in pares]
        pare_minim = min(pares_arbres, key=altura)
        u = node
        v = pare_minim
        # anàlisi de si podem llevar aresta
        ws = self.LCSA(u, v)
        for w in ws:
            intermitjos = w - u - v
            for ui in intermitjos_esquerra:  # camí de w → u
                if not antecessor_estricte(node=ui, origen=v, desti=u):
                    # return False ?
                    break
            for vi in intermitjos_dreta:  # camí de w → v
                if not antecessor_estricte(node=ui, origen=v, desti=u):
                    # return False ?
                    break
        else:
            return False
        return True
