"""
Cryptarithmetic Problem as a Constraint Satisfaction Problem (CSP)
--------------------------------------------------------
Variables:
    Each letter is a variable. The goal is to assign a digit to each letter.
        - The first letter of each word cannot be 0.
Domains:
    Each variable (letter) has a domain of digits {0, ..., 9}

Constraints:
    1. Each letter must be assigned a digit.
    2. No two letters can have the same digit.
"""
from typing import Dict, List, Optional, Tuple


class CryptarithmeticSolver:
    def __init__(self, variables: List[str]):
        self.variables = variables
        self.domains = {var: set(range(10)) for var in variables}
        self.constraints = self.create_constraints()

    def create_constraints(self) -> List[Tuple[str, str]]:
        """Generate binary constraints for variables to ensure unique values"""
        constraints = []
        for i in range(len(self.variables)):
            for j in range(i + 1, len(self.variables)):
                constraints.append((self.variables[i], self.variables[j]))
        return constraints

    def ac3(self) -> bool:
        """AC-3 Algorithm to enforce arc consistency"""
        queue = self.constraints.copy()
        while queue:
            (xi, xj) = queue.pop(0)
            if self.revise(xi, xj):
                if not self.domains[xi]:
                    return False
                for xk in self.variables:
                    if xk != xi:
                        queue.append((xk, xi))
        return True

    def revise(self, xi: str, xj: str) -> bool:
        revised = False
        for x in self.domains[xi].copy():
            if not any([x != y for y in self.domains[xj]]):
                self.domains[xi].remove(x)
                revised = True
        return revised

    def select_unassigned_variable(
        self, assignment: Dict[str, int]
    ) -> Optional[str]:
        """Select an unassigned variable"""
        unassigned = [var for var in self.variables if var not in assignment]
        if not unassigned:
            return None
        return min(unassigned, key=lambda var: len(self.domains[var]))

    def order_domain_values(
        self, var: str, assignment: Dict[str, int]
    ) -> List[int]:
        """Order domain values for a variable"""
        return sorted(
            self.domains[var],
            key=lambda value: self.count_constraints(var, value, assignment),
        )

    def count_constraints(
        self, var: str, value: int, assignment: Dict[str, int]
    ) -> int:
        """Count constraints for a variable-value pair"""
        count = 0
        for neighbor in (
            v for v in self.variables if v != var and v not in assignment
        ):
            if value == self.domains[neighbor]:
                count += 1
        return count

    def is_valid_solution(self, assignment: Dict[str, int]) -> bool:
        """Check if the current assignment satisfies the cryptarithmetic."""
        if len(set(assignment.values())) < len(
            assignment
        ):  # Check for duplicate values
            return False

        if assignment['S'] == 0 or assignment['M'] == 0:
            return False

        send = (
            1000 * assignment['S']
            + 100 * assignment['E']
            + 10 * assignment['N']
            + assignment['D']
        )
        more = (
            1000 * assignment['M']
            + 100 * assignment['O']
            + 10 * assignment['R']
            + assignment['E']
        )
        money = (
            10000 * assignment['M']
            + 1000 * assignment['O']
            + 100 * assignment['N']
            + 10 * assignment['E']
            + assignment['Y']
        )
        return send + more == money

    def backtrack(
        self, assignment: Dict[str, int]
    ) -> Optional[Dict[str, int]]:
        """Backtrack search to solve the cryptarithmetic puzzle"""
        if len(assignment) == len(self.variables):
            if self.is_valid_solution(assignment):
                return assignment
            return None

        var = self.select_unassigned_variable(assignment)
        if var is None:
            return None

        ordered_values = self.order_domain_values(var, assignment)
        if ordered_values is None:
            return None

        for value in ordered_values:
            if all(value != assignment.get(neigh) for neigh in assignment):
                assignment[var] = value
                original_domains = {
                    v: self.domains[v].copy() for v in self.variables
                }
                if self.ac3():
                    result = self.backtrack(assignment)
                    if result is not None:
                        return result
                self.domains = original_domains
                del assignment[var]
        return None

    def solve(self) -> Optional[Dict[str, int]]:
        """Solve the cryptarithmetic puzzle"""
        if not self.ac3():
            return None
        return self.backtrack({})


if __name__ == '__main__':
    variables = ['S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y']
    solver = CryptarithmeticSolver(variables)
    solution = solver.solve()
    if solution:
        print('SEND + MORE = MONEY')
        for letter, digit in solution.items():
            print(f'{letter}: {digit}')
    else:
        print('No solution found.')
