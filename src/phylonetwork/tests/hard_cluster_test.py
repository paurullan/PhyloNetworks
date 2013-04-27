#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

import unittest

from ..utils import construct

from ..classes import PhyloNetwork

class TestHardCluster(unittest.TestCase):

    def test_empty(self):
        G = construct(set())
        gold = set()
        self.assertItemsEqual(G.hard_cluster(), gold)

    def test_one(self):
        clusters = [(1, 2)]
        G = construct(clusters)
        gold = {(1,), (2,), (1, 2)}
        self.assertItemsEqual(G.hard_cluster(), gold)

    def test_three(self):
        clusters = [(1, 2), (3, 4)]
        G = construct(clusters)
        gold = {(1,), (2,), (3,), (4,), (1, 2, 3, 4),
                (1, 2), (3, 4) }
        self.assertItemsEqual(G.hard_cluster(), gold)

    def test_four(self):
        clusters = [(1, 2, 3)]
        G = construct(clusters)
        gold = {(1,), (2,), (3,), (1, 2, 3), }
        self.assertItemsEqual(G.hard_cluster(), gold)

    def test_five(self):
        """
        In this test we have a node ('n') that is not a leaf.
        """
        edges = [
            ((1, 2, 3, 'n'), ('n', )),
            (('n', ), (3, )),
            ((1, 2,), (1, )),
            ((1, 2,), (2, )),
            ((1, 2, 3, 'n'), (1, 2, )),
            ]
        G = PhyloNetwork()
        G.add_edges_from(edges)
        gold = {(1,), (2,), (3,), (1, 2), (1, 2, 3), }
        self.assertItemsEqual(G.hard_cluster(), gold)

    def test_six(self):
        edges = [
            ((1, 2, 3, 4), (1, 2)),
            ((1, 2, 3, 4), (3, 4)),
            ((3, 4, ), (3, )),
            ((3, 4, ), (4, )),
            ((1, 2,), (1, )),
            ((1, 2,), (2, )),
        ]
        G = PhyloNetwork()
        G.add_edges_from(edges)
        gold = {(1,), (2,), (3,), (4,), (1, 2), (3, 4), (1, 2, 3, 4), }
        self.assertItemsEqual(G.hard_cluster(), gold)


if __name__ == '__main__':
    unittest.main()
