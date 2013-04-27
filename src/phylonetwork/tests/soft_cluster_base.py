#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

from ..utils import construct
from ..classes import PhyloNetwork

class SoftBase(object):
    """This test needs to be subclassed and add the self.soft function"""

    def test_empty(self):
        G = construct(set())
        gold = set()
        self.assertItemsEqual(self.soft(G), gold)

    def test_one(self):
        clusters = [(1, 2), ]
        G = construct(clusters)
        gold = {(1,), (2,), (1, 2), }
        self.assertItemsEqual(self.soft(G), gold)

    def test_two(self):
        clusters = [(1, 2), (3, 4)]
        G = construct(clusters)
        gold = {(1,), (2,), (3,), (4,),
                (1, 2, 3, 4), (1, 2), (3, 4)}
        self.assertItemsEqual(self.soft(G), gold)

    def test_three(self):
        clusters = [(1, 2), (1, 3)]
        G = construct(clusters)
        gold = {(1, 2), (1, 3), (1,), (2,), (3,), (1, 2, 3), }
        self.assertItemsEqual(self.soft(G), gold)

    def test_three_b(self):
        clusters = [(1, 2), (1, 3), (2, 3)]
        G = construct(clusters)
        gold = {(1, 2), (1, 3), (2, 3), (1,), (2,), (3,), (1, 2, 3), }
        self.assertItemsEqual(self.soft(G), gold)

    def test_four(self):
        clusters = [(1, 2), (2, 3), (3, 4)]
        G = construct(clusters)
        gold = {(1,), (2,), (3,), (4,), (1, 2, 3, 4),
                (1, 2), (2, 3), (3, 4)}
        self.assertItemsEqual(self.soft(G), gold)

    def test_six(self):
        clusters = [(1, 2), (3, 4), (4, 5), (1, 2, 3, 4), (3, 4, 5)]
        G = construct(clusters)
        gold = {(1,), (2,), (3,), (4,), (5,),
                (1, 2), (3, 4), (4, 5),
                (1, 2, 3), (3, 4, 5), (1, 2, 3, 4),
                (1, 2, 3, 4, 5),
                }
        self.assertItemsEqual(self.soft(G), gold)

    def test_adria_1(self):
        edges = [
            ((1, 2, 3, 4, 5), (1, 2, 3, 4)),  # a
            ((1, 2, 3, 4, 5), (3, 4, 5)),  # b
            ((1, 2, 3, 4), (1, )),  # c
            ((1, 2, 3, 4), ('2h', )),  # d
            (('2h', ), (2, 3, 4,)),  # e
            ((2, 3, 4,), (2, )),  # f
            ((2, 3, 4,), ('3h', )),  # g
            ((3, 4, 5), ('3, 4, 5h')),  # h
            ((3, 4, 5), ('3h',)),  # i
            (('3, 4, 5h'), (2, 3, 4, 5)),  # j
            ((2, 3, 4, 5), ('2h', )),  # k
            (('3, 4, 5h'), ('4h',)),  # l
            ((2, 3, 4, 5), (5, )),  # m
            (('3h', ), (3, 4)),  # n
            ((3, 4, ), ('4h', )),  # o
            ((3, 4, ), (3, )),  # p
            (('4h', ), (4, )),  # q
        ]
        G = PhyloNetwork()
        G.add_edges_from(edges)
        gold = [(1,), (2,), (3,), (4,), (5,),
                (4, 5), (2, 3), (2, 5), (1, 2), (3, 4),
                (2, 3, 5), (1, 2, 3), (2, 4, 5),
                (3, 4, 5), (2, 3, 4), (2, 3, 4, 5),
                (1, 2, 3, 4), (1, 2, 3, 4, 5)]
        self.assertItemsEqual(self.soft(G), gold)

    def test_adria_2(self):
        clusters = [
            (1, 2), (3, 4), (4, 5), (3, 4, 5), (1, 2, 3, 4)
        ]
        G = construct(clusters)
        gold = {(1,), (2,), (3,), (4,), (5,),
                (1, 2), (4, 5), (3, 4),
                (3, 4, 5), (1, 2, 3),
                (1, 2, 3, 4), (1, 2, 3, 4, 5)}
        self.assertItemsEqual(self.soft(G), gold)

    def test_adria_3(self):
        clusters = [(1, 3), (2, 3), (3, 4), ]
        G = construct(clusters)
        gold = [(1,), (2,), (3,), (4,),
                (1, 3), (2, 3), (3, 4),
                (1, 2, 3, 4)]
        self.assertItemsEqual(self.soft(G), gold)

    def test_adria_4(self):
        clusters = [(2, 3), (1, 3), (3, 4), (1, 2, 3), (1, 3, 4), ]
        G = construct(clusters)
        gold = [(1,), (2,), (3,), (4,),
                (1, 2), (1, 3), (1, 4), (2, 3), (3, 4),
                (1, 3, 4), (1, 2, 3), (1, 2, 3, 4)]
        self.assertItemsEqual(self.soft(G), gold)

    def test_adria_5(self):
        clusters = [(1, 2), (3, 4), (4, 5), (1, 2, 3, 4), (3, 4, 5), ]
        G = construct(clusters)
        gold = [(1,), (2,), (3,), (4,), (5, ),
                (1, 2), (3, 4), (4, 5),
                (1, 2, 3), (3, 4, 5),
                (1, 2, 3, 4),
                (1, 2, 3, 4, 5)]
        self.assertItemsEqual(self.soft(G), gold)

    def test_adria_6(self):
        """ 8 nodes emparellats, 8 híbrids, 196 crides, .25 segons"""
        clusters = [
            (1, 2), (2, 3), (3, 4), (4, 5),
            (5, 6), (6, 7), (7, 8), (8, 1), ]
        G = construct(clusters)
        gold = {(7, 8), (5, 6), (8,), (2, 3),
                (1, 2, 3, 4, 5, 6, 7, 8),
                (1, 2), (6, 7),
                (1,), (2,), (3,), (1, 8), (4,), (4, 5),
                (5,), (6,), (7,), (3, 4)}
        self.assertItemsEqual(self.soft(G), gold)

    def test_complex_0(self):
        clusters = [(3, 8), (2, 6), (3, 4), (1, 7),
                    (2, 3, 5, 7), (1, 4, 7, 8),
                    (1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,)]
        gold = {
            (1, 2, 3, 4, 5, 6, 7, 8),
            (1, 4, 7, 8), (2, 3, 5, 7),
            (2, 6), (3, 8), (1, 7), (3, 4),
            (1, 4), (1, 8), (2, 5), (3, 5), (5, 7),
            (1, 4, 7), (1, 4, 8), (1, 7, 8), (2, 3, 5), (2, 5, 7), (3, 5, 7),
            (1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,),
            }
        result = self.soft(construct(clusters))
        self.assertItemsEqual(result, gold)

    def test_complex_1(self):
        clusters = [(2, 3), (5, 6), (3, 6), (4, 8),
                    (1, 2, 4, 6), (1, 3, 5, 7),
                    (1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,)]

        gold = {(1, 2, 4, 6), (4, 8), (5, 6), (2, 6), (1, 6), (3, 7),
        (4,), (1, 2), (1,), (3,), (5,), (3, 6), (7,), (8,), (2, 4, 6),
        (1, 3, 5, 7), (1, 4), (2, 3), (1, 2, 4), (1, 3, 7), (1, 2, 6),
        (4, 6), (1, 5, 7), (2,), (5, 7), (3, 5, 7), (1, 2, 3, 4, 5, 6, 7, 8),
        (6,), (1, 7), (1, 4, 6), (2, 4)}
        result = self.soft(construct(clusters))
        self.assertItemsEqual(result, gold)

    def test_complex_2(self):
        clusters = [
            (3, 5), (2, 5), (5, 9), (4, 10), (1, 2),
            (3, 4, 6, 7, 8), (2, 5, 8, 9, 10),
            (1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (10,)]

        gold = { (5, 9), (2, 5, 8, 9, 10), (2, 5, 8, 9), (9,), (8, 9),
            (2, 5, 9), (2, 5), (2, 8, 9, 10), (1, 2), (6, 7), (1,),
            (5, 8, 9, 10), (4, 6, 7, 8), (3,), (5,), (2, 8, 9), (7,),
            (3, 6, 7), (4, 10), (5, 9, 10), (8,), (6, 7, 8), (9, 10),
            (10,), (5, 8, 9), (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), (2, 9,
            10), (2, 5, 9, 10), (3, 5), (8, 9, 10), (3, 6, 7, 8), (2,
            9), (2,), (4,), (6,), (3, 4, 6, 7), (4, 6, 7), (3, 4, 6, 7, 8)
            }
        result = self.soft(construct(clusters))
        self.assertItemsEqual(result, gold)
