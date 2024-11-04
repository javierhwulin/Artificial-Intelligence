"""
N-Queens Solver as a Constraint Satisfaction Problem (CSP)
--------------------------------------------------------
Variables:
    Each row in the n x n grid is a variable.

Domains:
    Each variable (row) has a domain of values {1, 2, ..., n}

Constraints:
    No two queens can attack each other,
        i.e., no two queens can be in the same row, column, or diagonal.
"""
from typing import List, Set, Dict


class NQueensSolver:
    def __init__(self, n: int) -> None:
        self.n = n
        self.domains: Dict[int, Set[int]] = {
            col: set(range(n)) for col in range(n)
        }

    def ac3(self) -> bool:
        """Enforce arc consistency using AC3 algorithm."""
        queue = [
            (xi, xj)
            for xi in range(self.n)
            for xj in range(self.n)
            if xi != xj
        ]

        while queue:
            (xi, xj) = queue.pop(0)
            if self.revise(xi, xj):
                if not self.domains[xi]:
                    return False
                for xk in range(self.n):
                    if xk != xj and xk != xi:
                        queue.append((xk, xi))
        return True

    def revise(self, xi: int, xj: int) -> bool:
        """ "Revise the domain of xi to enforce arc consistency with xj."""
        revised = False
        for row in self.domains[xi].copy():
            if not any(
                self.is_valid_assignment(row, other_row, xi, xj)
                for other_row in self.domains[xj]
            ):
                self.domains[xi].remove(row)
                revised = True
        return revised

    def is_valid_assignment(
        self, row1: int, row2: int, col1: int, col2: int
    ) -> bool:
        """Check if two assignments are consistent (no treath)."""
        return row1 != row2 and abs(row1 - row2) != abs(col1 - col2)

    def select_unassigned_variable(self) -> int:
        """
        Select the column with the fewest remaining values (MRV heuristic).
        """
        return min(
            (col for col in self.domains if len(self.domains[col]) > 1),
            key=lambda col: len(self.domains[col]),
        )

    def order_domain_values(self, col: int) -> List[int]:
        """
        Order the domain values of a variable (column)
        by least constraining value.
        """
        return sorted(self.domains[col])

    def backtrack(self) -> Dict[int, int]:
        """Backtracking search with AC3 and MRV heuristic."""
        if all(len(self.domains[col]) == 1 for col in range(self.n)):
            return {
                col: next(iter(self.domains[col])) for col in range(self.n)
            }

        column = self.select_unassigned_variable()
        original_domain = self.domains[column].copy()

        for row in self.order_domain_values(column):
            if self.is_consistent(column, row):
                self.assign(column, row)
                result = self.backtrack()
                if result:
                    return result
                self.unassign(column, original_domain)

        return {}

    def assign(self, column: int, row: int) -> None:
        """Assign a value to a variable (column)."""
        self.domains[column] = {row}

    def unassign(self, column: int, domain: Set[int]) -> None:
        """Unassign a value from a variable (column)."""
        self.domains[column] = domain

    def is_consistent(self, column: int, row: int) -> bool:
        """Check if a value assignment is consistent with the constraints."""
        for col, domain in self.domains.items():
            if col != column and len(domain) == 1:
                if not self.is_valid_assignment(
                    row, next(iter(domain)), column, col
                ):
                    return False
        return True

    def print_solution(self, solution: Dict[int, int]):
        """Print the solution as an n x n grid."""
        for i in range(self.n):
            print(
                ' '.join(
                    'Q' if solution[i] == j else '.' for j in range(self.n)
                )
            )


if __name__ == '__main__':
    n = 4
    solver = NQueensSolver(n)
    if solver.ac3():
        solution = solver.backtrack()
        if solution:
            solver.print_solution(solution)
        else:
            print('No solution exists')
    else:
        print('Initial constraint makes the problem unsolvable')
