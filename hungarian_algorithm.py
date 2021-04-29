#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np

def reduction(G):
    row = G.min(axis=1)
    G = G - np.array([row]).T

    col = G.min(axis=0)
    G = G - col

    return G, sum(row) + sum(col)

def search_zeros(G):
    row = [1, 2, 2, 1]
    col = [1, 1, 3, 1]

    for i in G:
        for j in G[i]:
            pass




if __name__ == '__main__':
    m = np.array([[20, 40, 10, 50],
                  [100, 80, 30, 40],
                  [10, 5, 60, 20],
                  [70, 30, 10, 25]])

    print(reduction(m))

