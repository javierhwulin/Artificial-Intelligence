import numpy as np


class GridProblem:
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.memo = {}

    def Goal_Test(self, state):
        return state == self.goal

    def Actions(self, state):
        x, y = state
        actions = []
        if x > 0 and self.grid[x - 1][y] == 0:
            actions.append('UP')
        if x < len(self.grid) - 1 and self.grid[x + 1][y] == 0:
            actions.append('DOWN')
        if y > 0 and self.grid[x][y - 1] == 0:
            actions.append('LEFT')
        if y < len(self.grid[0]) - 1 and self.grid[x][y + 1] == 0:
            actions.append('RIGHT')
        return actions

    def Result(self, state, action):
        x, y = state
        if action == 'UP':
            return [(x - 1, y)]
        elif action == 'DOWN':
            return [(x + 1, y)]
        elif action == 'LEFT':
            return [(x, y - 1)]
        elif action == 'RIGHT':
            return [(x, y + 1)]

    def is_valid_state(self, state):
        x, y = state
        return (
            0 <= x < len(self.grid)
            and 0 <= y < len(self.grid[0])
            and self.grid[x][y] == 0
        )


def AND_OR_Search(grid: GridProblem):
    return OR_Search(grid.start, grid, [], set())


def OR_Search(state, grid: GridProblem, path, visited):
    if grid.Goal_Test(state):
        return []
    if state in visited:
        return None  # Avoid loops
    visited.add(state)

    if state in problem.memo:
        return problem.memo[state]

    for action in grid.Actions(state):
        subplan = AND_Search(
            grid.Result(state, action), grid, path + [state], visited.copy()
        )
        if subplan is not None:
            plan = [(action, subplan)]
            problem.memo[state] = plan
            return plan
    return None


def AND_Search(states, grid, path, depth):
    if not states:
        return []
    plan = []
    for state in states:
        subplan = OR_Search(state, grid, path, depth)
        if subplan is None:
            return None
        plan.extend(subplan)
    return plan


def generate_navigable_grid(rows, cols, start=(0, 0), end=None):
    if end is None:
        end = (rows - 1, cols - 1)

    # Initialize grid with all 1s (walls)
    grid = [[1 for _ in range(cols)] for _ in range(rows)]

    # Set start and end points to 0 (path)
    grid[start[0]][start[1]] = 0
    grid[end[0]][end[1]] = 0

    # Helper function to get valid neighbors
    def get_neighbors(x, y):
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                neighbors.append((nx, ny))
        return neighbors

    # Create a path from start to end
    current = start
    path = [current]
    while current != end:
        neighbors = get_neighbors(*current)
        next_step = min(
            neighbors, key=lambda n: abs(n[0] - end[0]) + abs(n[1] - end[1])
        )
        grid[next_step[0]][next_step[1]] = 0
        path.append(next_step)
        current = next_step

    # Randomly open some walls
    num_open = rows * cols // 4  # Open about 25% of the cells
    for _ in range(num_open):
        x, y = np.random.randint(0, rows - 1), np.random.randint(0, cols - 1)
        grid[x][y] = 0

    return grid


def parse_coordinates(coord_input):
    try:
        return tuple(map(int, coord_input.split(',')))
    except ValueError:
        print("Invalid input. Please enter coordinates as 'x,y'.")
        return None


if __name__ == '__main__':
    # Define a grid to run the AND-OR search
    grid = [
        [0, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 0],
    ]

    rows, cols = 10, 10
    start = (0, 0)
    goal = (9, 5)
    random_grid = generate_navigable_grid(rows, cols, start, goal)

    for row in random_grid:
        print('_'.join(map(str, row)))

    problem = GridProblem(random_grid, start, goal)
    plan = AND_OR_Search(problem)
    print(f'Contingency plan: {plan}')
