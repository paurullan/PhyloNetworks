#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import logging
log = logging.getLogger(__name__)

from ..classes import PhyloNetwork

class TestENewick(unittest.TestCase):
    "((Aurora,(Boylii)#H1)Amerana,(#H1,Temporaria))Laurasiarana;"
    "((Aurora)#H1,((#H1,Boylii)Amerana,Temporaria))Laurasiarana;)"
    pass


class TestPhyloNet(unittest.TestCase):

    def test_enewick(self):
        pass

    def test_csa_1(self):
        network = PhyloNetwork(eNewick='((,(3,4)#1)2,#1)1;')
        result = network.CSA('3', '4')
        gold = ["#1", "_1"]
        self.assertItemsEqual(result, gold)

    def test_lcsa_1(self):
        network = PhyloNetwork(eNewick='((,(3,4)#1)2,#1)1;')
        result = network.LCSA('3', '4')
        gold = "#1"
        log.debug(result)
        self.assertEqual(result, gold)


class TestLCSA(unittest.TestCase):

    def setUp(self):
        self.p = PhyloNetwork()
        nodes = [
            (1,), (2, ), (3, ), (1, 2, 3),
            (1, 2), (2, 3), ('2h',),
            (1, 2, 'x'), (2, 3, 'y'),
        ]
        # from → to
        edges = [
            [(1, 2), (1,)],
            [(1, 2), ('2h',)],
            [(2, 3), (3,)],
            [(2, 3), ('2h',)],
            [('2h', ), (2,)],

            [(1, 2, 3), (1, 2, 'x')],
            [(1, 2, 3), (2, 3, 'y')],
            [(1, 2, 'x'), (1, 2)],
            [(2, 3, 'y'), (2, 3)],
        ]
        self.p.add_nodes_from(nodes)
        self.p.add_edges_from(edges)

    def test_lcsa(self):

        #import ipdb; ipdb.set_trace()
        #       x = self.p.LCSA((1, ), (2, ))
        pass

    def test_strict_predecessor(self):
        pass
