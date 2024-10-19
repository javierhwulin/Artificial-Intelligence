"""
Consider the task of traveling from one city to another
(e.g., finding a route from City A to City B).

Initial State: City A
Actions: Go to another city (node)
Goal Test: Reaching City B
Path Cost: The Euclidean Distance between cities

Cities as Nodes:
A connects to:
    B with a distance of 2
    C with a distance of 4
    D with a distance of 1

B connects to:
    A with a distance of 2
    C with a distance of 1
    E with a distance of 5

C connects to:
    A with a distance of 4
    B with a distance of 1
    D with a distance of 2
    F with a distance of 7

D connects to:
    A with a distance of 1
    C with a distance of 2
    E with a distance of 3

E connects to:
    B with a distance of 5
    D with a distance of 3
    F with a distance of 2

F (destination node)
"""

from collections import deque
import heapq
from math import sqrt


def bfs(start, goal):
    queue = deque([start])
    visited_nodes = set()
    visited_nodes.add(start)
    path = {start: None}

    while queue:
        node = queue.popleft()

        # If we reach the goal, reconstruct the path
        if node == goal:
            return reconstruct_path(path, start, goal)

        # Explore neighbors
        for neighbour in adj[node]:
            if neighbour not in visited_nodes:
                queue.append(neighbour)
                visited_nodes.add(neighbour)
                path[neighbour] = node

    return None   # Return None if the goal is not found


def Astar(start, goal):
    priority_queue = [
        (h(start, goal), start)
    ]   # Priority queue (f_cost, node)
    visited_nodes = set()
    g_cost = {start: 0}  # Stores the current shortest path to each node.
    path = {start: None}   # To reconstruct path

    while priority_queue:
        # Pop the node with the smallest f_cost
        current_f, node = heapq.heappop(priority_queue)

        # If we reach teh goal, reconstruct
        if node == goal:
            return reconstruct_path(path, start, goal)

        # Explore neighbours
        for neighbour in adj[node]:
            tentative_g_cost = (
                g_cost[node] + adj[node][neighbour]
            )   # g(current) + cost(current, neighbor)
            if neighbour not in g_cost or tentative_g_cost < g_cost[neighbour]:
                # Update the g_cost for the neighbor
                if neighbour not in visited_nodes:
                    g_cost[neighbour] = tentative_g_cost
                    f_cost = tentative_g_cost + h(
                        neighbour, goal
                    )   # f(n) = g(n) + h(n)
                    # Push neighbor onto the priority queue
                    heapq.heappush(priority_queue, (f_cost, neighbour))
                    # Update the path
                    path[neighbour] = node
        visited_nodes.add(node)
    return None


def h(node, goal):
    """Heuristic function: Euclidean distance between nodes."""
    x = coord[goal][0] - coord[node][0]
    y = coord[goal][1] - coord[node][1]
    return sqrt(pow(x, 2) + pow(y, 2))


def reconstruct_path(path, start, goal):
    """Reconstruct the path from start to goal."""
    curr = goal
    reverse_path = []

    while curr is not None:
        reverse_path.append(curr)
        curr = path[curr]

    reverse_path.reverse()
    return reverse_path


if __name__ == '__main__':
    adj = {
        'A': {'B': 2, 'C': 4, 'D': 1},
        'B': {'A': 2, 'C': 1, 'E': 5},
        'C': {'A': 4, 'B': 1, 'D': 2, 'F': 7},
        'D': {'A': 1, 'C': 2, 'E': 3},
        'E': {'B': 5, 'D': 3, 'F': 2},
        'F': {},
    }

    coord = {
        'A': (0, 0),
        'B': (2, 1),
        'C': (4, 4),
        'D': (1, 3),
        'E': (5, 1),
        'F': (6, 6),
    }

    option = int(input('Enter operation BFS(0) or A*(1): '))

    if option == 0:
        path = bfs('A', 'F')
        print(path)
    elif option == 1:
        path = Astar('A', 'F')
        print(path)
    else:
        print('Enter valid operation')
