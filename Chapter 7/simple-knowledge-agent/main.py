class KnowledgeBasedAgent:
    def __init__(self):
        self.facts = set()
        self.rules = []

    def add_fact(self, fact):
        self.facts.add(fact)

    def add_rule(self, conditions, conclusion):
        self.rules.append((conditions, conclusion))

    def evaluate_conditions(self, conditions, visited=None):
        if visited is None:
            visited = set()

        if isinstance(conditions, dict) and 'and' in conditions:
            return all(
                self.query_with_backward_chaining(condition, visited)
                for condition in conditions['and']
            )
        elif isinstance(conditions, dict) and 'or' in conditions:
            return any(
                self.query_with_backward_chaining(condition, visited)
                for condition in conditions['or']
            )
        else:
            return self.query_with_backward_chaining(conditions, visited)

    def infer_new_facts(self):
        new_facts_inferred = False
        for conditions, conclusion in self.rules:
            if self.evaluate_conditions(
                conditions
            ) and not conclusion.issubset(self.facts):
                self.facts.update(conclusion)
                new_facts_inferred = True
                print(f'Inferred new fact: {conclusion}')
        return new_facts_inferred

    def query_with_forward_chaining(self, goal):
        while self.infer_new_facts():
            pass
        return goal in self.facts

    def query_with_backward_chaining(self, goal, visited=None):
        if visited is None:
            visited = set()
        if goal in self.facts:
            return True
        if goal in visited:
            return False
        visited.add(goal)

        for conditions, conclusion in self.rules:
            if goal in conclusion:
                if self.evaluate_conditions(conditions, visited):
                    self.facts.add(goal)
                    return True
        return False

    def query_multiple(self, goals, method='backward'):
        results = {}
        for goal in goals:
            if method == 'forward':
                results[goal] = self.query_with_forward_chaining(goal)
            elif method == 'backward':
                results[goal] = self.query_with_backward_chaining(goal)
            else:
                raise ValueError('Invalid method')
            print(f'Query result for {goal}: {results[goal]}')
        return results

    def __str__(self):
        return f'Facts: {self.facts}\nRules: {self.rules}'


def main():
    # Example 1: Simple knowledge-based agent
    agent = KnowledgeBasedAgent()
    agent.add_fact('Raining')
    agent.add_fact('Wet Ground')
    agent.add_rule({'and': ['Raining', 'Wet Ground']}, {'Muddy Ground'})
    agent.add_rule('Muddy Ground', 'Dirty Shoes')
    agent.add_rule('Dirty Shoes', 'Footprints')
    agent.add_rule('Footprints', 'Caught')
    print(agent)
    agent.query_multiple(['Caught'], method='backward')

    # Example 2: More complex knowledge-based agent
    print('\n')
    agent = KnowledgeBasedAgent()
    agent.add_fact('Raining')
    agent.add_fact('Cold')
    agent.add_rule({'and': ['Raining', 'Cold']}, {'Snowy'})
    agent.add_rule({'or': ['Snowy', 'Cold']}, {'Icy'})
    agent.add_rule({'or': ['Raining', 'Snowy']}, {'Wet'})
    agent.add_rule({'and': ['Wet', 'Icy']}, {'Slippery'})
    agent.add_rule('Slippery', 'Accident')
    agent.add_rule('Accident', 'Damage')
    agent.add_rule('Damage', 'Repair')
    agent.add_rule('Repair', 'Expenses')
    agent.add_rule('Expenses', 'Loss')

    print(agent)
    goals = [
        'Loss',
        'Raining',
        'Cold',
        'Snowy',
        'Icy',
        'Wet',
        'Slippery',
        'Accident',
        'Damage',
        'Repair',
        'Expenses',
    ]
    agent.query_multiple(goals, method='backward')


if __name__ == '__main__':
    main()
