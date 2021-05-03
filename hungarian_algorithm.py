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
                    break

            del rows_zeros[minimum[1]]
            for x in cols_zeros.copy().keys():
                if temp_G[minimum[1]][x] == 0:
                    if cols_zeros[x] == 1:
                        del cols_zeros[x]
                    else:
                        cols_zeros[x] -= 1
        else:
            for n, elem in enumerate(temp_G[:, minimum[1]]):
                if elem == 0 and minimum[1] not in taken_c and n not in taken_r:
                    ind_zeros.append((n, minimum[1]))
                    break
            del cols_zeros[minimum[1]]
            for x in rows_zeros.keys():
                if temp_G[x][minimum[1]] == 0:
                    if rows_zeros[x] == 1:
                        del rows_zeros[x]
                    else:
                        rows_zeros[x] -= 1
        if rows_zeros:
            min_row = min(rows_zeros, key=rows_zeros.get)
        else:
            ozn_r = np.inf
        if cols_zeros:
            min_col = min(cols_zeros, key=cols_zeros.get)
        else:
            ozn_c = np.inf
    return ind_zeros


def find_more_ind_zeros(G, ind_zeros):
    num_of_lines = len(ind_zeros)
    rows_zeros = {}
    cols_zeros = {}
    lines = []
    for n, elem in enumerate(G):
        rows_zeros[n] = np.count_nonzero(elem == 0)
    for n, elem in enumerate(G):
        cols_zeros[n] = np.count_nonzero(G[:, n] == 0)
    while num_of_lines:
        max_row = max(rows_zeros, key=rows_zeros.get)
        max_col = max(cols_zeros, key=cols_zeros.get)
        maximum = ('r', max_row) if rows_zeros[max_row] >= cols_zeros[max_col] else ('c', max_col)
        if maximum[0] == 'r':
            lines.append((maximum[0], max_row))
            del rows_zeros[max_row]
            for x in cols_zeros.copy().keys():
                if G[max_row][x] == 0:
                    if cols_zeros[x] == 1:
                        del cols_zeros[x]
                    else:
                        cols_zeros[x] -= 1
        else:
            lines.append((maximum[0], max_col))
            del cols_zeros[max_col]
            for x in rows_zeros.copy().keys():
                if G[x][max_col] == 0:
                    if rows_zeros[x] == 1:
                        del rows_zeros[x]
                    else:
                        rows_zeros[x] -= 1
        num_of_lines -= 1
    erased_rows = [i[1] for i in lines if i[0] == 'r']
    erased_cols = [i[1] for i in lines if i[0] == 'c']
    min_element = np.inf
    for i, row in enumerate(G):
        for j, element in enumerate(row):
            if i not in erased_rows and j not in erased_cols:
                if element < min_element:
                    min_element = element
    for i, row in enumerate(G):
        for j, element in enumerate(row):
            if i not in erased_rows and j not in erased_cols:
                G[i][j] -= min_element
            elif i in erased_rows and j in erased_cols:
                G[i][j] += min_element
    return G


if __name__ == '__main__':
    m = np.array([[20, 40, 10, 50],
                  [100, 80, 30, 40],
                  [10, 5, 60, 20],
                  [70, 30, 10, 25]])

    print(search_zeros(reduction(m)[0]))
    s = find_more_ind_zeros(reduction(m)[0], search_zeros(reduction(m)[0]))
    print(s)
    print(search_zeros(s))
