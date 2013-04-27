#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

"""
Construct the hasse diagram of a given set of clusters.
"""

# [ [1, 2, 3], [4] ]
def Hasse(clusters):
    # corner case for the empty input
    if not clusters:
        return []
    if len(clusters) == 1 and not clusters[0]:
        return []

    cluster_dict, level_max = _construct_hasse(clusters)
    results = []

    for levels in range(1, level_max):
        for clr in cluster_dict[levels]:
            for level in range(levels+1, level_max+1):
                level_clusters = cluster_dict[level]
                [_check_in(clr, x, results) for x in level_clusters]
    return results


def _construct_hasse(clusters):
    max_set = set()
    for s in clusters:
        for elem in s:
            max_set.add(elem)
    level_max = len(max_set)

    # cluster_dict has the tree cluster structure
    cluster_dict = {x: [] for x in range(1, level_max+1)}

    for cluster in clusters:
        cluster_dict[len(cluster)].append(cluster)

    # init for single elements pex: [ [1], [2], [3], ]
    cluster_dict[1] = []
    for item in list(max_set):
        cluster_dict[1].append([item])

    if not list(max_set) in cluster_dict[level_max]:
        cluster_dict[level_max].append(list(max_set))

    return cluster_dict, level_max


def _check_in(a, b, results):
    a, b = set(a), set(b)
    if not a.issubset(b):
        return False
    for orig, dest in results:
        orig, dest = set(orig), set(dest)
        if orig.issubset(b) and a == dest:
            return False
    results.append((tuple(b), tuple(a)))
    return True
