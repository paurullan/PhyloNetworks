#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

import unittest

import networkx as nx

from ..utils import construct, network
from ..utils import check_cluster

from ..classes import PhyloNetwork
from ..hasse import Hasse

class TestCleanTree(unittest.TestCase):

    def assertGraphEqual(self, G1, G2):
        GM = nx.algorithms.isomorphism.GraphMatcher(G1,G2)
        self.assertTrue(GM.is_isomorphic())

    def test_empty(self):
        G = PhyloNetwork()
        gold = PhyloNetwork()
        self.assertGraphEqual(G.clean_graph(), gold)
        self.assertEqual(G.edges(), gold.edges())

    def test_one(self):
        G = PhyloNetwork()
        G.add_node(1)
        clean = G.clean_graph()
        gold = {1}
        self.assertItemsEqual(clean.nodes(), gold)

    def test_complex(self):
        G = PhyloNetwork()
        G.add_edges_from([(1, 2), (2, 3)])
        gold = PhyloNetwork()
        gold.add_edges_from([(1, 3)])
        clean = G.clean_graph()
        self.assertEqual(clean.edges(), gold.edges())

class TestGraphCreation(unittest.TestCase):

    def test_type(self):
        edges = [(1, 2), (2, 3)]
        G = network(edges)
        self.assertEqual(G.edges(), edges)

    def test_edges(self):
        edges = [((1, 2), (1,)),
                 ((1, 2), (2,)),
                 ((1, 3), (1,)),
                 ((1, 3), (3,)),
                 ((1, 2, 3), (1, 2,)),
                 ((1, 2, 3), (2, 3)),
                 ]
        G = network(edges)
        self.assertItemsEqual(G.edges(), edges)

    def test_degree(self):
        edges = [(1, 2), (2, 3)]
        G = network(edges)
        self.assertEqual(G.edges(), edges)
        self.assertEqual(G.in_degree(1), 0)
        self.assertEqual(G.in_degree(2), 1)
        self.assertEqual(G.in_degree(3), 1)

    def test_degree_hasse(self):
        edges = [(1, 2), (1, 3)]
        h = Hasse(edges)
        G = network(h)
        # remember that the nodes are tuples (x, )
        self.assertEqual(G.in_degree((1,)), 2)
        self.assertEqual(G.in_degree((2,)), 1)
        self.assertEqual(G.in_degree((3,)), 1)


class TestHybridNodes(unittest.TestCase):

    def test_empty(self):
        clusters = [[]]
        G = construct(clusters)
        self.assertItemsEqual(G.hybrid_nodes(), [])

    def test_none(self):
        clusters = [(1, 2), (3, 4)]
        G = construct(clusters)
        self.assertItemsEqual(G.hybrid_nodes(), [])

    def test_one(self):
        clusters = [(1, 2), (1, 3)]
        G = construct(clusters)
        self.assertItemsEqual(G.hybrid_nodes(), [('1h', ),])

    def test_two(self):
        clusters = [(1, 2), (1, 3), (2, 3)]
        G = construct(clusters)
        self.assertItemsEqual(G.hybrid_nodes(), [('1h',), ('2h',), ('3h',)])

    def test_three(self):
        clusters = [(1, 2), (2, 3), (3, 4)]
        G = construct(clusters)
        self.assertItemsEqual(G.hybrid_nodes(), [('2h',), ('3h',)])


class TestTreeChild(unittest.TestCase):
    """The graf is tree-child"""

    def true_hybrid(self):
        "The fact to have hybrids does not mean you can't be tree-child"
        clusters = [(1, 2), (1, 3)]
        G = construct(clusters)
        self.assertTrue(G.is_treechild())

    def test_complex_false(self):
        clusters = [(1, 2), (1, 3), (2, 3)]
        G = construct(clusters)
        self.assertFalse(G.is_treechild())

    def test_true(self):
        clusters = [(1, 2), (3, 4)]
        G = construct(clusters)
        self.assertTrue(G.is_treechild())


class TestCheckCluster(unittest.TestCase):

    def test_empty(self):
        clusters = [[]]
        self.assertTrue(check_cluster(clusters))

    def test_one(self):
        clusters = [(1, 2)]
        self.assertTrue(check_cluster(clusters))


class TestCalcHybrid(unittest.TestCase):

    def test_empty(self):
        clusters = []
        result = construct(clusters).hybrid_nodes()
        gold = []
        self.assertItemsEqual(result, gold)

    def test_one(self):
        clusters = [(1, 2), (3, 5), (3, 4, 5) ]
        result = construct(clusters).hybrid_nodes()
        gold = []
        self.assertItemsEqual(result, gold)

    def test_two(self):
        clusters = [(1, 2), (2, 3), (3, 5), (3, 4, 5) ]
        result = construct(clusters).hybrid_nodes()
        gold = [('2h',), ('3h', )]
        self.assertItemsEqual(result, gold)

    def test_three(self):
        clusters = [(6, 8), (4, 7), (2, 6), (7, 10), (6, 10), (2, 3, 7,
        9, 10), (1, 4, 7, 9, 10), (1,), (2,), (3,), (4,), (5,), (6,),
        (7,), (8,), (9,), (10,)]
        result = construct(clusters).hybrid_nodes()
        gold = [('2h',), ('10h',), ('7h',), ('9h',), ('6h',),
                ('(7, 10)h',)]
        self.assertItemsEqual(result, gold)



class TestConstructNetwork(unittest.TestCase):

    def test_empty(self):
        clusters = []
        result = construct(clusters)
        gold = []
        self.assertItemsEqual(result, gold)

    def test_one(self):
        clusters = [(1, 2), (3, 5), (3, 4, 5) ]
        result = construct(clusters)
        gold = [(1,), (2,), (3,), (4,), (5,),
                (1, 2), (3, 5), (3, 4, 5),
                (1, 2, 3, 4, 5)]
        self.assertItemsEqual(result, gold)

    def test_two(self):
        clusters = [(1, 2), (2, 3), (3, 5), (3, 4, 5) ]
        result = construct(clusters)
        gold = [(1,), (2,), (3,), (4,), (5,),
                (1, 2), (2, 3), (3, 5),
                (3, 4, 5),
                (1, 2, 3, 4, 5),
                ('2h',), ('3h', )]
        self.assertItemsEqual(result, gold)


class TestCleanGraph(unittest.TestCase):

    def test_empty(self):
        edges = []
        G = PhyloNetwork()
        G.add_edges_from(edges)
        result = G.clean_graph()
        gold = []
        self.assertItemsEqual(result, gold)

    def test_direct(self):
        edges = [(1, 2),]
        G = PhyloNetwork()
        G.add_edges_from(edges)
        result = G.clean_graph()
        gold = [1, 2]
        self.assertItemsEqual(result, gold)

    def test_one_goes(self):
        edges = [(1, 2), (2, 3)]
        G = PhyloNetwork()
        G.add_edges_from(edges)
        result = G.clean_graph()
        gold = [1, 3]
        self.assertItemsEqual(result, gold)

    def test_two_go(self):
        edges = [(1, 2), (2, 3), (3, 4)]
        G = PhyloNetwork()
        G.add_edges_from(edges)
        result = G.clean_graph()
        gold = [1, 4]
        self.assertItemsEqual(result, gold)


if __name__ == '__main__':
    unittest.main()
