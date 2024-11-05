"""
This module contains the main function that checks
if a given propositional logic formula entails another.
"""
from itertools import product


# Function to evaluate an expression given a model
def evaluate_expression(expression, model):
    for symbol, value in model.items():
        expression = expression.replace(symbol, str(value))
    return eval(expression)


# Function to generate all possible models given a list of symbols
def generate_models(symbols):
    combinations = list(product([True, False], repeat=len(symbols)))
    return [dict(zip(symbols, combination)) for combination in combinations]


# Function to check if a formula entails another (KB entails query)
def is_entailed(KB, query):
    symbols = set(
        [
            symbol
            for formula in KB + [query]
            for symbol in formula
            if symbol.isupper()
        ]
    )
    models = generate_models(symbols)
    for model in models:
        if all(evaluate_expression(formula, model) for formula in KB):
            if not evaluate_expression(query, model):
                return (
                    False  # Found a model where KB is true but query is false
                )
    return True  # No counterexample found


# Main function
def main():
    """
    KB is a list of propositional logic formulas, represented as strings,
    where each formula is separated by a comma,
    and each symbol is separated by a space.
    Upper case letters represent propositional symbols.
    Lower case letters represent logical operators.
    """

    # Example 1
    KB = [
        'A or B',
        'not A or C',
        'not B or C',
    ]   # not A or C is equivalent to A -> C
    query = 'C'
    print(f'Example 1: KB = {KB}, query = {query}')
    if is_entailed(KB, query):
        print('KB entails query')
    else:
        print('KB does not entail query')

    # Example 2
    KB = [
        'A and B',
        'not A or C',
        'not B or C',
    ]
    query = 'C'
    print(f'Example 2: KB = {KB}, query = {query}')
    if is_entailed(KB, query):
        print('KB entails query')
    else:
        print('KB does not entail query')

    # Example 3: Modus Ponens
    KB = [
        'not A or B',
        'A',
    ]
    query = 'B'
    print(f'Example 3: KB = {KB}, query = {query}')
    if is_entailed(KB, query):
        print('KB entails query')
    else:
        print('KB does not entail query')

    # Example 4: Modus Tollens
    KB = [
        'not A or B',
        'not B',
    ]
    query = 'not A'
    print(f'Example 4: KB = {KB}, query = {query}')
    if is_entailed(KB, query):
        print('KB entails query')
    else:
        print('KB does not entail query')

    # Example 5: Hypothetical Syllogism
    KB = [
        'not A or B',
        'not B or C',
    ]
    query = 'not A or C'
    print(f'Example 5: KB = {KB}, query = {query}')
    if is_entailed(KB, query):
        print('KB entails query')
    else:
        print('KB does not entail query')

    # Example 6: Disjunctive Syllogism
    KB = [
        'A or B',
        'not A',
    ]
    query = 'B'
    print(f'Example 6: KB = {KB}, query = {query}')
    if is_entailed(KB, query):
        print('KB entails query')
    else:
        print('KB does not entail query')

    # Example 7: Constructive Dilemma
    KB = [
        'not A or B',
        'not C or D',
        'A or C',
    ]
    query = 'B or D'
    print(f'Example 7: KB = {KB}, query = {query}')
    if is_entailed(KB, query):
        print('KB entails query')
    else:
        print('KB does not entail query')

    # Example 8: Simplification
    KB = [
        'A and B',
    ]
    query = 'A'
    print(f'Example 8: KB = {KB}, query = {query}')
    if is_entailed(KB, query):
        print('KB entails query')
    else:
        print('KB does not entail query')

    # Example 9: Conjunction
    KB = [
        'A',
        'B',
    ]
    query = 'A and B'
    print(f'Example 9: KB = {KB}, query = {query}')
    if is_entailed(KB, query):
        print('KB entails query')
    else:
        print('KB does not entail query')

    # Example 10: Resolution
    KB = [
        'A or B',
        'not A or C',
        'not B or D',
    ]
    query = 'C or D'
    print(f'Example 10: KB = {KB}, query = {query}')
    if is_entailed(KB, query):
        print('KB entails query')
    else:
        print('KB does not entail query')

    # Example 11: Absorption
    KB = [
        'not A or B',
    ]
    query = 'not A or (A and B)'
    print(f'Example 11: KB = {KB}, query = {query}')
    if is_entailed(KB, query):
        print('KB entails query')
    else:
        print('KB does not entail query')

    # Example 12: De Morgan's Law
    KB = [
        'not (A and B)',
    ]
    query = 'not A or not B'
    print(f'Example 12: KB = {KB}, query = {query}')
    if is_entailed(KB, query):
        print('KB entails query')
    else:
        print('KB does not entail query')

    # Example 13: Double Negation
    KB = [
        'A',
    ]
    query = 'not not A'
    print(f'Example 13: KB = {KB}, query = {query}')
    if is_entailed(KB, query):
        print('KB entails query')
    else:
        print('KB does not entail query')

    # Example 14: Exportation
    KB = [
        'not (A and B) or C',
    ]
    query = 'not A or (not B or C)'
    print(f'Example 14: KB = {KB}, query = {query}')
    if is_entailed(KB, query):
        print('KB entails query')
    else:
        print('KB does not entail query')

    # Example 15: Tautology
    KB = [
        'A or not A',
    ]
    query = 'A or B'
    print(f'Example 15: KB = {KB}, query = {query}')
    if is_entailed(KB, query):
        print('KB entails query')
    else:
        print('KB does not entail query')

    # Example 16: Contradiction
    KB = [
        'A and not A',
    ]
    query = 'A or B'
    print(f'Example 16: KB = {KB}, query = {query}')
    if is_entailed(KB, query):
        print('KB entails query')
    else:
        print('KB does not entail query')

    # Example 17: Contingency
    KB = [
        'A or B',
    ]
    query = 'A or B'
    print(f'Example 17: KB = {KB}, query = {query}')
    if is_entailed(KB, query):
        print('KB entails query')
    else:
        print('KB does not entail query')

    # Example 18: Equivalence
    KB = [
        'not A or B',
        'not B or A',
    ]
    query = '(not A or B) and (not B or A)'
    print(f'Example 18: KB = {KB}, query = {query}')
    if is_entailed(KB, query):
        print('KB entails query')
    else:
        print('KB does not entail query')

    # Example 20: Distribution
    KB = [
        'A and (B or C)',
    ]
    query = '(A and B) or (A and C)'
    print(f'Example 19: KB = {KB}, query = {query}')
    if is_entailed(KB, query):
        print('KB entails query')
    else:
        print('KB does not entail query')


if __name__ == '__main__':
    main()
