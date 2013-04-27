#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

import unittest

from ..cluster_networks import construct
from ..cluster_networks import calc_soft_cluster

@unittest.skip("not ready")
class TestClusterFromRandom(unittest.TestCase):

    maxDiff = None

    def test_random_0(self):
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
        result = calc_soft_cluster(construct(clusters))
        self.assertItemsEqual(result, gold)

    def test_random_1(self):
        clusters = [(2, 3), (5, 6), (3, 6), (4, 8),
                    (1, 2, 4, 6), (1, 3, 5, 7),
                    (1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,)]

        gold = {(1, 2, 4, 6), (4, 8), (5, 6), (2, 6), (1, 6), (3, 7),
        (4,), (1, 2), (1,), (3,), (5,), (3, 6), (7,), (8,), (2, 4, 6),
        (1, 3, 5, 7), (1, 4), (2, 3), (1, 2, 4), (1, 3, 7), (1, 2, 6),
        (4, 6), (1, 5, 7), (2,), (5, 7), (3, 5, 7), (1, 2, 3, 4, 5, 6, 7, 8),
        (6,), (1, 7), (1, 4, 6), (2, 4)}

        result = calc_soft_cluster(construct(clusters))
        self.assertItemsEqual(result, gold)

    def test_random_2(self):
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

        result = calc_soft_cluster(construct(clusters))
        self.assertItemsEqual(result, gold)


if __name__ == '__main__':
    unittest.main()
