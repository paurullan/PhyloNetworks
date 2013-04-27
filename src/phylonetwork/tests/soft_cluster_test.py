#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from ..cluster_networks import calc_soft_cluster

from soft_cluster_base import SoftBase

class TestSoft(SoftBase, unittest.TestCase):

    @classmethod
    def soft(cls, g):
        return calc_soft_cluster(g)

if __name__ == '__main__':
    unittest.main()
