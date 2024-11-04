"""
Sudoku Solver as a Constraint Satisfaction Problem (CSP)
--------------------------------------------------------

Variables:
    Each cell (row, col) in the 9x9 grid is a variable.

Domains:
    Each variable (cell) has a domain of values {1, 2, ..., 9}

Constraints:
    1. Each row must contain each number from 1 to 9 exactly once.
    2. Each column must contain each number from 1 to 9 exactly once.
    3. Each 3x3 subgrid must contain each number from 1 to 9 exactly once.
"""

from typing import List, Set, Dict, Tuple
import timeit
import numpy as np


class SudokuSolver:
    def __init__(self, board: List[List[int]]) -> None:
        self.board = board
        # Map each cell to its domain of possible values
        self.domains: Dict[Tuple[int, int], Set[int]] = {}
        self.initialize_domains()

    def initialize_domains(self):
        """
        Apply node consistency by initializing
        domains based on initial board values.
        """
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    # If cell is empty, set to all possible values {1, ..., 9}
                    self.domains[(row, col)] = set(range(1, 10))
                else:
                    # If cell is filled, set to the value itself
                    self.domains[(row, col)] = {self.board[row][col]}

    def ac3(self) -> bool:
        """Enforce arc consistency using AC3 algorithm."""
        queue = [(i, j) for i in self.domains for j in self.get_neighbors(i)]

        while queue:
            (i, j) = queue.pop(0)
            if self.revise(i, j):
                # If domain of i is empty, then no solution exists
                if not self.domains[i]:
                    return False
                # Add neighbors of i to queue (excluding j)
                for k in self.get_neighbors(i):
                    if k != j:
                        queue.append((k, i))
        return True

    def revise(self, i: Tuple[int, int], j: Tuple[int, int]) -> bool:
        """Revise the domain of i to enforce arc consistency with j."""
        revised = False
        for x in self.domains[i].copy():
            # If there is no value in domain that satisfies the constraint
            # with j's domain, remove x from i's domain
            if not any(
                self.is_valid_assignment(x, y) for y in self.domains[j]
            ):
                self.domains[i].remove(x)
                revised = True
        return revised

    def is_valid_assignment(self, x: int, y: int) -> bool:
        """
        Check if assignment of x to i is valid
        with respect to y's domain.
        """
        return x != y

    def get_neighbors(self, pos: Tuple[int, int]) -> Set[Tuple[int, int]]:
        """Return the set of neighbors for a given cell (row, col)"""
        row, col = pos
        neighbors = set()

        # Row and column neighbors
        for i in range(9):
            if i != col:
                neighbors.add((row, i))
            if i != row:
                neighbors.add((i, col))

        # Subgrid neighbors
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if (i, j) != pos:
                    neighbors.add((i, j))

        return neighbors

    def select_unassigned_variable(self) -> Tuple[int, int]:
        """
        Select the next unassigned variable (cell)
        based on minimum remaining values heuristic.
        """
        return min(
            (
                cell
                for cell in self.domains
                if self.board[cell[0]][cell[1]] == 0
            ),
            key=lambda cell: len(self.domains[cell]),
        )

    def backtracking(self) -> bool:
        """
        Solve the Sudoku board using backtracking algorithm
        with arc consistency and MRV heuristic.
        """
        if all(
            self.board[row][col] != 0 for row in range(9) for col in range(9)
        ):
            return True

        # Select the variable with minimum remaining values (MRV heuristic)
        row, col = self.select_unassigned_variable()

        # Try each value in the domain of the selected variable
        for value in sorted(self.domains[(row, col)]):
            if self.is_valid(value, (row, col)):
                # Assign the value to the cell
                self.board[row][col] = value
                # Backup the domains before making the assignment
                backup = self.domains.copy()
                # Recursively solve the board
                if self.ac3() and self.backtracking():
                    return True
                # Unassign the value if it leads to failure
                self.board[row][col] = 0
                self.domains = backup
        return False

    def is_valid(self, num: int, pos: Tuple[int, int]) -> bool:
        """
        Check if assigning `num` to `pos` is valid
        based on row, column, and subgrid constraints.
        """
        row, col = pos
        return all(
            num != self.board[row][i]
            and num != self.board[i][col]
            and num
            != self.board[3 * (row // 3) + i // 3][3 * (col // 3) + i % 3]
            for i in range(9)
        )

    def print_board(self) -> None:
        for row in range(9):
            if row % 3 == 0 and row != 0:
                print('---------------------')
            for col in range(9):
                if col % 3 == 0 and col != 0:
                    print('|', end=' ')
                print(self.board[row][col], end=' ')
            print()


if __name__ == '__main__':
    board = [
        [0, 0, 5, 0, 0, 4, 0, 7, 0],
        [0, 0, 0, 7, 0, 0, 2, 4, 0],
        [4, 0, 7, 0, 0, 6, 9, 3, 1],
        [0, 0, 8, 0, 7, 0, 1, 0, 0],
        [0, 0, 0, 9, 2, 0, 0, 0, 3],
        [0, 0, 0, 0, 6, 8, 0, 0, 0],
        [0, 7, 0, 0, 0, 0, 3, 0, 0],
        [3, 0, 9, 1, 0, 5, 0, 6, 0],
        [2, 5, 0, 0, 4, 0, 0, 0, 0],
    ]

    solver = SudokuSolver(board)
    if solver.backtracking():
        print('Solved Sudoku Board:')
        solver.print_board()
    else:
        print('No solution exists.')

    time = timeit.repeat(lambda: solver.backtracking(), number=1, repeat=1000)
    print(f'Time: {np.mean(time):.2e} ± {np.std(time):.2e} seconds')

""" Output
Solved Sudoku Board:
9 1 5 | 2 3 4 | 6 7 8
6 8 3 | 7 1 9 | 2 4 5
4 2 7 | 8 5 6 | 9 3 1
---------------------
5 9 8 | 4 7 3 | 1 2 6
7 6 4 | 9 2 1 | 5 8 3
1 3 2 | 5 6 8 | 4 9 7
---------------------
8 7 1 | 6 9 2 | 3 5 4
3 4 9 | 1 8 5 | 7 6 2
2 5 6 | 3 4 7 | 8 1 9

time = 1.309998333454132e-05
"""
