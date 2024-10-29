def belief_state_search(
    initial_state, goal_state, belief_state, threshold=0.5
):
    # Start with a set of initial states
    initial_belief_state = {initial_state}
    # Each frontier holds a belief state and a path
    frontier = [(initial_belief_state, [])]
    explored = set()

    while frontier:
        belief_state, path = frontier.pop(0)

        # Goal test: Check if any state in the belief state is a goal state
        goal_count = sum(1 for state in belief_state if state in goal_state)
        if goal_count / len(belief_state) >= threshold:
            return path

        # Skip already explored belief states
        if frozenset(belief_state) in explored:
            continue
        explored.add(frozenset(belief_state))

        # Iterate over all actions
        for action in actions:
            new_belief_state = set()

            # Update the belief state based on the action
            for state in belief_state:
                if action in adj[state]:  # Ensure the action is valid
                    new_belief_state.update(adj[state][action])

            # Only add the new belief state if it is not in the explored set
            if frozenset(new_belief_state) not in explored:
                frontier.append((new_belief_state, path + [action]))
    return None


if __name__ == '__main__':
    actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    adj = {
        (0, 0): {
            'UP': [(0, 0)],  # Can't move up
            'DOWN': [(1, 0), (0, 1)],  # Move down or slip right
            'LEFT': [(0, 0)],  # Can't move left
            'RIGHT': [(0, 1), (1, 0)],  # Move right or slip down
        },
        (0, 1): {
            'UP': [(0, 1)],  # Can't move up
            'DOWN': [(1, 1), (1, 0)],  # Move down or slip left
            'LEFT': [(0, 0)],  # Move left
            'RIGHT': [(0, 1)],  # Can't move right
        },
        (1, 0): {
            'UP': [(0, 0), (0, 1)],  # Move up or slip right
            'DOWN': [(1, 0)],  # Can't move down
            'LEFT': [(1, 0)],  # Can't move left
            'RIGHT': [(1, 1), (0, 0)],  # Move right or slip up
        },
        (1, 1): {
            'UP': [(0, 1), (1, 0)],  # Move up or slip left
            'DOWN': [(1, 1)],  # Can't move down
            'LEFT': [(1, 0)],  # Move left
            'RIGHT': [(1, 1)],  # Can't move right
        },
    }

    path = belief_state_search((0, 0), {(1, 1)}, {(0, 0)})
    print(f'Path: {path}')
