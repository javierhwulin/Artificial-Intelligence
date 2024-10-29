class OnlineSearchAgent:
    def __init__(self, grid, start, goal, actions):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.actions = actions
        self.explored_map = {}
        self.visited = set()

    def explore(self):
        frontier = [(self.start, [])]

        while frontier:
            current_state, path = frontier.pop(0)
            if current_state == self.goal:
                return path
            self.visited.add(current_state)
            self.explored_map[current_state] = self.sense_surroundings(
                current_state
            )

            for direction in self.actions:
                if (
                    direction not in self.explored_map[current_state]
                    and self.explored_map[current_state][direction]
                    == 'blocked'
                ):
                    continue

                new_state = self.get_new_state(current_state, direction)

                if new_state not in self.visited and self.is_free(new_state):
                    frontier.append((new_state, path + [direction]))

        return None

    def sense_surroundings(self, state):
        x, y = state
        surroundings = {
            'UP': (x - 1, y) if x > 0 else None,
            'DOWN': (x + 1, y) if x < len(self.grid) - 1 else None,
            'LEFT': (x, y - 1) if y > 0 else None,
            'RIGHT': (x, y + 1) if y < len(self.grid[0]) - 1 else None,
        }
        sensed = {}
        for direction, new_pos in surroundings.items():
            if new_pos and self.grid[new_pos[0]][new_pos[1]] == 0:
                sensed[direction] = 'free'
            else:
                sensed[direction] = 'blocked'
        return sensed

    def get_new_state(self, state, direction):
        x, y = state
        if direction == 'UP':
            return (x - 1, y)
        elif direction == 'DOWN':
            return (x + 1, y)
        elif direction == 'LEFT':
            return (x, y - 1)
        elif direction == 'RIGHT':
            return (x, y + 1)
        return state

    def is_free(self, state):
        x, y = state
        return (
            0 <= x < len(self.grid)
            and 0 <= y < len(self.grid[0])
            and self.grid[x][y] == 0
        )


if __name__ == '__main__':
    grid = [
        [0, 0, 1, 0],
        [1, 0, 1, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0],
    ]

    start = (0, 0)
    goal = (3, 3)
    actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']

    agent = OnlineSearchAgent(grid, start, goal, actions)
    path = agent.explore()
    print(f'Path: {path}')
