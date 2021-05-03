import unittest
import numpy as np
import hungarian_algorithm


class TestHungarianAlgorithm(unittest.TestCase):
    def test_reduction(self):
        test_matrix = np.array(
            [[20, 40, 10, 50], [100, 80, 30, 40], [10, 5, 60, 20], [70, 30, 10, 25]]
        )
        expected_reduced_matrix = np.array(
            [[5, 30, 0, 30], [65, 50, 0, 0], [0, 0, 55, 5], [55, 20, 0, 5]]
        )
        expected_lower_bound = 70

        (result_matrix, result_lower_bound) = hungarian_algorithm.reduction(test_matrix)
        self.assertTrue(np.all(expected_reduced_matrix == result_matrix))
        self.assertEqual(expected_lower_bound, result_lower_bound)

    def test_search_zeros(self):
        test_matrix = np.array(
            [[5, 30, 0, 30], [65, 50, 0, 0], [0, 0, 55, 5], [55, 20, 0, 5]]
        )
        # (row_number, col_number)
        zeros_set_permutations = [{(2, 0), (1, 3), (3, 2)},
                                  {(1, 3), (2, 1), (3, 2)},
                                  {(0, 2), (1, 3), (2, 1)},
                                  {(0, 2), (1, 3), (2, 0)}]
        result = hungarian_algorithm.search_zeros(test_matrix)
        self.assertIn(set(result), zeros_set_permutations)

    def test_get_solution(self):
        test_matrix = np.array(
            [[20, 40, 10, 50], [100, 80, 30, 40], [10, 5, 60, 20], [70, 30, 10, 25]]
        )
        expected_cost = 75

        _, result_cost = hungarian_algorithm.get_solution(test_matrix)
        self.assertEqual(result_cost, expected_cost)


if __name__ == "__main__":
    unittest.main()
