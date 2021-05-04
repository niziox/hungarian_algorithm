#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
from typing import List, Tuple

assignation = str
cost = str


def reduction(G):
    # odejęcie minimalnej wartości w każdym wierszu
    row = G.min(axis=1)
    G = G - np.array([row]).T

    # odejęcie minimalnej wartości w każdej kolumnie
    col = G.min(axis=0)
    G = G - col

    return G, sum(row) + sum(col)


def search_zeros(G):
    rows_zeros = {}
    cols_zeros = {}
    ind_zeros = []
    temp_G = G.copy()

    # liczba zer w każdym wierszu i kolumnie
    for n, elem in enumerate(temp_G):
        rows_zeros[n] = np.count_nonzero(elem == 0)
    for n, elem in enumerate(temp_G):
        cols_zeros[n] = np.count_nonzero(temp_G[:, n] == 0)

    # wiersz i kolumna z minimalną wartością zer
    min_row = min(rows_zeros, key=rows_zeros.get)
    min_col = min(cols_zeros, key=cols_zeros.get)
    ozn_c = 0
    ozn_r = 0

    # wykreślanie zer niezależnych
    while rows_zeros or cols_zeros:
        if ozn_c != 0:
            minimum = ('r', min_row)
        elif ozn_r != 0:
            minimum = ('c', min_col)
        else:
            # poszukiwanie wiersza lub kolumny z minimalną liczbą zer
            minimum = ('r', min_row) if rows_zeros[min_row] <= cols_zeros[min_col] else ('c', min_col)
        taken_r = [i[0] for i in ind_zeros]
        taken_c = [i[1] for i in ind_zeros]
        if minimum[0] == 'r':
            for n, elem in enumerate(temp_G[minimum[1]]):
                if elem == 0 and n not in taken_c and minimum[1] not in taken_r:
                    ind_zeros.append((minimum[1], n))
                    break

            # wykreślanie rzędu z zerem niezależnym
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

            # wykreślanie kolumny z zerem niezależnym
            del cols_zeros[minimum[1]]

            for x in rows_zeros.keys():
                if temp_G[x][minimum[1]] == 0:
                    if rows_zeros[x] == 1:
                        del rows_zeros[x]
                    else:
                        rows_zeros[x] -= 1

        # sprawdzenie czy zostały jeszcze jakieś niewykreślone zera
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

    # liczba zer w każdym wierszu i kolumnie
    for n, elem in enumerate(G):
        rows_zeros[n] = np.count_nonzero(elem == 0)
    for n, elem in enumerate(G):
        cols_zeros[n] = np.count_nonzero(G[:, n] == 0)

    # liczba linii musi być równa liczbie zer niezależnych
    while num_of_lines:
        max_row = max(rows_zeros, key=rows_zeros.get)
        max_col = max(cols_zeros, key=cols_zeros.get)
        maximum = ('r', max_row) if rows_zeros[max_row] >= cols_zeros[max_col] else ('c', max_col)

        # wykreślanie wiersza lub kolumny z największą ilością zer
        if col_priority:
            maximum = ('c', max_col) if rows_zeros[max_row] <= cols_zeros[max_col] else ('r', max_row)
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

        # zmniejszenie liczby dostępnych linii do skreślenia
        num_of_lines -= 1
    erased_rows = [i[1] for i in lines if i[0] == 'r']
    erased_cols = [i[1] for i in lines if i[0] == 'c']
    min_element = np.inf

    # wyszukwianie najmniejszego elementu spośród niezakreślonych elementów macierzy
    for i, row in enumerate(G):
        for j, element in enumerate(row):
            if i not in erased_rows and j not in erased_cols:
                if element < min_element:
                    min_element = element

    # odejmowanie wartości minimalnej od niezakreślonych elementów macierzy
    for i, row in enumerate(G):
        for j, element in enumerate(row):
            if i not in erased_rows and j not in erased_cols:
                G[i][j] -= min_element

            # dodawanie wartości minimalnej do podwójnie zakreślonych elementów macierzy
            elif i in erased_rows and j in erased_cols:
                G[i][j] += min_element
    return G


def check_zeros(G: np.ndarray) -> List[Tuple[int, int]]:
    ind_zeros = search_zeros(G)

    # wypisanie każdego stanu macierzy G
    print("=" * 20)
    print(G)
    print("=" * 20)

    print(f'liczba zer niezależnych = {len(ind_zeros)}')
    if len(ind_zeros) == G.shape[0]:
        return ind_zeros
    else:
        # rekurencyjne wywoływanie funkcji do momentu znalezienia liczby zer niezależnych równej liczbie wierszy macierzy
        if len(search_zeros(find_more_ind_zeros(G, ind_zeros))) == len(ind_zeros):
            return check_zeros(find_more_ind_zeros(G, ind_zeros, True))
        else:
            return check_zeros(find_more_ind_zeros(G, ind_zeros))


def get_solution(G: np.ndarray) -> Tuple[assignation, cost]:
    G_reduced, reduction_cost = reduction(G)
    ind_zeros = check_zeros(G_reduced)

    solution = "\n".join([f'Zadanie {t + 1} -> Maszyna {m + 1}' for t, m in sorted(ind_zeros, key=lambda x: x[0])])
    optimal_cost = sum([G[i, j] for i, j in ind_zeros])
    optimal_cost = 'Wartość funkcji celu:' + str(optimal_cost)
    return solution, optimal_cost


if __name__ == '__main__':
    # m = np.array([[10, 5, 13, 15, 16, 8],
    #               [3, 9, 18, 13, 6, 5],
    #               [10, 7, 2, 2, 2, 3],
    #               [7, 11, 9, 7, 12, 10],
    #               [7, 9, 10, 4, 12, 4],
    #               [4, 6, 7, 1, 8, 9]])
    m = np.array([[44, 26, 25, 78, 56, 97, 85, 27, 29, 22],
                  [80, 76, 29, 10, 70, 91, 55, 53, 89, 19],
                  [15, 36, 96, 71, 29, 54, 99, 85, 27, 49],
                  [77, 73, 63, 5, 82, 7, 44, 40, 64, 88],
                  [99, 34, 55, 9, 12, 4, 85, 40, 31, 21],
                  [1, 48, 18, 66, 96, 89, 89, 14, 34, 98],
                  [12, 57, 2, 31, 7, 98, 21, 51, 22, 95],
                  [36, 81, 69, 24, 15, 6, 9, 80, 37, 45],
                  [10, 65, 79, 43, 70, 64, 15, 56, 16, 88],
                  [89, 22, 85, 63, 78, 45, 43, 28, 9, 64]])
    s, o = get_solution(m)
    print(s)
    print(o)
