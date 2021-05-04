#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
from typing import List, Tuple

assignation = str
cost = int


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


def find_more_ind_zeros(G, ind_zeros, col_priority=False):
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
        if col_priority:
            maximum = ('c', max_col) if rows_zeros[max_row] == cols_zeros[max_col] else ('r', max_row)
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


def check_zeros(G: np.ndarray, iter=1) -> List[Tuple[int, int]]:
    ind_zeros = search_zeros(G)

    # prints every next state of the G matrix
    print("=" * 20)
    print(G)
    print("=" * 20)

    print(f'liczba zer niezależnych = {len(ind_zeros)}')
    if len(ind_zeros) == G.shape[0]:
        return ind_zeros
    else:
        col_priority = bool(iter % 2)  # stochastic programming
        return check_zeros(find_more_ind_zeros(G, ind_zeros, col_priority), iter + 1)


def get_solution(G: np.ndarray) -> Tuple[assignation, cost]:
    G_reduced, reduction_cost = reduction(G)
    ind_zeros = check_zeros(G_reduced)

    solution = "\n".join([f'Zadanie {t + 1} -> Maszyna {m + 1}' for t, m in sorted(ind_zeros, key=lambda x: x[0])])
    optimal_cost = sum([G[i, j] for i, j in ind_zeros])
    return solution, optimal_cost


if __name__ == '__main__':
    # m = np.array([[20, 40, 10, 50],
    #               [100, 80, 30, 40],
    #               [10, 5, 60, 20],
    #               [70, 30, 10, 25]])
    # s, o = get_solution(m)
    # print(s)
    # print(o)

    m = np.array([[10, 5, 13, 15, 16, 8],
                  [3, 9, 18, 13, 6, 5],
                  [10, 7, 2, 2, 2, 3],
                  [7, 11, 9, 7, 12, 10],
                  [7, 9, 10, 4, 12, 4],
                  [4, 6, 7, 1, 8, 9]])
    s, o = get_solution(m)
    print(s)
    print(o)
