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
from itertools import permutations


def is_valid_solution(assignment):
    """Check if the current assignment satisfies the cryptarithmetic puzzle."""
    send = (
        assignment['S'] * 1000
        + assignment['E'] * 100
        + assignment['N'] * 10
        + assignment['D']
    )
    more = (
        assignment['M'] * 1000
        + assignment['O'] * 100
        + assignment['R'] * 10
        + assignment['E']
    )
    money = (
        assignment['M'] * 10000
        + assignment['O'] * 1000
        + assignment['N'] * 100
        + assignment['E'] * 10
        + assignment['Y']
    )
    return send + more == money


def solve_cryptoarithmetic():
    letters = 'SENDMORY'
    for perm in permutations(range(10), len(letters)):
        assignment = {letter: digit for letter, digit in zip(letters, perm)}
        if assignment['S'] == 0 or assignment['M'] == 0:
            continue
        if is_valid_solution(assignment):
            return assignment
    return None


if __name__ == '__main__':
    solution = solve_cryptoarithmetic()
    if solution:
        print('SEND + MORE = MONEY')
        for letter, digit in solution.items():
            print(f'{letter}: {digit}')
    else:
        print('No solution found.')
