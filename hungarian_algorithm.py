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
    rows_zeros = {}
    cols_zeros = {}
    ind_zeros = []
    temp_G = G.copy()
    for n, elem in enumerate(temp_G):
        rows_zeros[n] = np.count_nonzero(elem == 0)
    for n, elem in enumerate(temp_G):
        cols_zeros[n] = np.count_nonzero(temp_G[:, n] == 0)
    min_row = min(rows_zeros, key=rows_zeros.get)
    min_col = min(cols_zeros, key=cols_zeros.get)
    ozn_c = 0
    ozn_r = 0
    while rows_zeros or cols_zeros:
        if ozn_c != 0:
            minimum = ('r', min_row)
        elif ozn_r != 0:
            minimum = ('c', min_col)
        else:
            minimum = ('r', min_row) if rows_zeros[min_row] <= cols_zeros[min_col] else ('c', min_col)
        taken_r = [i[0] for i in ind_zeros]
        taken_c = [i[1] for i in ind_zeros]
        if minimum[0] == 'r':
            for n, elem in enumerate(temp_G[minimum[1]]):
                if elem == 0 and n not in taken_c and minimum[1] not in taken_r:
                    ind_zeros.append((minimum[1], n))
            del rows_zeros[minimum[1]]
        else:
            for n, elem in enumerate(temp_G[:, minimum[1]]):
                if elem == 0 and minimum[1] not in taken_c and n not in taken_r:
                    ind_zeros.append((n, minimum[1]))
            del cols_zeros[minimum[1]]
        if rows_zeros:
            min_row = min(rows_zeros, key=rows_zeros.get)
        else:
            ozn_r = np.inf
        if cols_zeros:
            min_col = min(cols_zeros, key=cols_zeros.get)
        else:
            ozn_c = np.inf
    return ind_zeros


if __name__ == '__main__':
    m = np.array([[20, 40, 10, 50],
                  [100, 80, 30, 40],
                  [10, 5, 60, 20],
                  [70, 30, 10, 25]])

    print(search_zeros(reduction(m)[0]))
