#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from soft_cluster_base import SoftBase


class TestSoft(SoftBase, unittest.TestCase):

    @classmethod
    def soft(cls, g):
        return g.soft_cluster()

if __name__ == '__main__':
    unittest.main()
