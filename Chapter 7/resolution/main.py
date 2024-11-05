def negate(literal):
    if literal[0] == '~':
        return literal[1:]
    else:
        return '~' + literal


def resolve(ci, cj):
    resolvents = set()
    for literal in ci:
        if negate(literal) in cj:
            resolvent = (ci - {literal}) | (cj - {negate(literal)})
            resolvents.add(frozenset(resolvent))
    return resolvents


def resolution(KB, query):
    clauses = [frozenset(clause) for clause in KB + [{negate(query)}]]
    new_clauses = set(clauses)

    while True:
        pairs = [
            (ci, cj) for ci in new_clauses for cj in new_clauses if ci != cj
        ]
        generated = set()
        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)
            if frozenset() in resolvents:
                return True
            generated.update(resolvents)

        if generated.issubset(new_clauses):
            return False

        new_clauses.update(generated)


def main():
    # Example 1: Resolution
    KB = [
        {'~R', 'W'},  # -R or W is equivalent to R -> W
        {'~W', 'S'},  # -W or S is equivalent to W -> S
        {'R'},
    ]
    query = 'S'
    print(f'KB = {KB}, query = {query}')
    if resolution(KB, query):
        print('KB entails query')
    else:
        print('KB does not entail query')


if __name__ == '__main__':
    main()
