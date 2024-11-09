from itertools import product


class LogicalStateEstimator:
    def __init__(self):
        self.facts = set()
        self.rules = []
        self.possible_states = []

    def add_fact(self, fact):
        self.facts.add(fact)

    def add_rule(self, premise, conclusion):
        negated_premise = {self.negate(premise) for premise in premise}
        rule = negated_premise | conclusion
        self.rules.append(rule)

    def negate(self, literal):
        if literal[0] == '~':
            return literal[1:]
        else:
            return '~' + literal

    def is_consistent(self, state):
        for fact in self.facts:
            if self.negate(fact) in state:
                return False

        for rule in self.rules:
            if all(self.negate(literal) in state for literal in rule):
                return False
        return True

    def estimate_state(self):
        literals = {literals for rule in self.rules for literals in rule}
        literals.update(self.facts)
        literals = {lit.lstrip('~') for lit in literals}

        all_states = [
            set(state)
            for state in product(
                *[(lit, self.negate(lit)) for lit in literals]
            )
        ]
        self.possible_states = [
            state for state in all_states if self.is_consistent(state)
        ]
        return self.possible_states

    def query(self, query):
        query_results = [query in state for state in self.possible_states]

        if all(query_results):
            return True
        elif not any(query_results):
            return False
        else:
            return 'Unknown'


def main():
    agent = LogicalStateEstimator()
    agent.add_fact('Dark')

    agent.add_rule({'Dark'}, {'~LightOn'})
    agent.add_rule({'LightOn'}, {'Bright'})

    possible_states = agent.estimate_state()
    print(f'Possible states: {possible_states}')

    query_light_off = agent.query('~LightOn')
    query_bright = agent.query('Bright')

    print(f'Query ~LightOn: {query_light_off}')
    print(f'Query Bright: {query_bright}')


if __name__ == '__main__':
    main()
