"""
Map Coloring Problem as a Constraint Satisfaction Problem (CSP)
--------------------------------------------------------

Variables:
    Each country is a variable. The goal is to assign a color to each country.

Domains:
    Each variable (country) has a domain of colors {Red, Green, Blue, Yellow}
    - Based on the four-color theorem:
        we only need four colors to color any map.

Constraints:
    1. Each country must be assigned a color.
    2. No two adjacent countries can have the same color.
    3. The map must be colored using the fewest number of colors.
"""

from typing import List, Dict, Set


class MapColoring:
    def __init__(
        self, map_graph: Dict[str, List[str]], colors: List[str]
    ) -> None:
        self.map_graph = map_graph
        self.colors = colors
        self.domains = {country: set(colors) for country in map_graph}

    def ac3(self) -> bool:
        """Ensure arc consistency across the map."""
        queue = [
            (xi, xj) for xi in self.map_graph for xj in self.map_graph[xi]
        ]
        while queue:
            (xi, xj) = queue.pop(0)
            if self.revise(xi, xj):
                if not self.domains[xi]:
                    return False
                for xk in self.map_graph[xi]:
                    if xk != xj:
                        queue.append((xk, xi))
        return True

    def revise(self, xi: str, xj: str) -> bool:
        revised = False
        for color in self.domains[xi].copy():
            if not any(color != xj_color for xj_color in self.domains[xj]):
                self.domains[xi].remove(color)
                revised = True
        return revised

    def select_unassigned_variable(self) -> str:
        """
        Select the next variable using MRV heuristic
        and tie-breaking with degree heuristic
        """
        return min(
            (
                country
                for country in self.domains
                if len(self.domains[country]) > 1
            ),
            key=lambda country: (
                len(self.domains[country]),
                -len(self.map_graph[country]),
            ),
        )

    def is_consistent(self, country: str, color: str) -> bool:
        """
        Check if assigning color to country
        is consistent with constraints
        """
        for neighbor in self.map_graph[country]:
            if (
                len(self.domains[neighbor]) == 1
                and color in self.domains[neighbor]
            ):
                return False
        return True

    def assign(self, country: str, color: str):
        """Assign a color to a region and propagate constraints"""
        self.domains[country] = {color}

    def unassign(self, country: str, original_domain: Set[str]):
        """Restore the original domain after backtracking"""
        self.domains[country] = original_domain

    def backtrack(self) -> bool:
        if all(len(self.domains[country]) == 1 for country in self.domains):
            return True

        country = self.select_unassigned_variable()
        original_domain = self.domains[country].copy()

        for color in sorted(self.domains[country]):
            if self.is_consistent(country, color):
                self.assign(country, color)
                if self.ac3() and self.backtrack():
                    return True
            self.unassign(country, original_domain)

        return False

    def print_map(self):
        """Print the solution of the map coloring problem"""
        for country in self.domains:
            color = next(iter(self.domains[country]))
            print(f'Country {country}: {color}')


if __name__ == '__main__':
    map_graph = {
        'Galicia': ['Asturias', 'Castilla y Leon'],
        'Asturias': ['Galicia', 'Castilla y Leon', 'Cantabria'],
        'Cantabria': ['Asturias', 'Castilla y Leon', 'Pais Basco'],
        'Pais Basco': ['Cantabria', 'Castilla y Leon', 'La Rioja', 'Navarra'],
        'La Rioja': ['Pais Basco', 'Castilla y Leon', 'Navarra'],
        'Navarra': ['La Rioja', 'Pais Basco', 'Aragon', 'Castilla y Leon'],
        'Aragon': [
            'Navarra',
            'Castilla y Leon',
            'Catalonia',
            'Castilla La Mancha',
            'Valenciana',
        ],
        'Catalonia': ['Aragon', 'Valenciana'],
        'Valenciana': ['Aragon', 'Castilla La Mancha', 'Murcia', 'Catalonia'],
        'Murcia': ['Valenciana', 'Castilla La Mancha', 'Andalusia'],
        'Andalusia': ['Murcia', 'Castilla La Mancha', 'Extremadura'],
        'Extremadura': ['Andalusia', 'Castilla La Mancha', 'Castilla y Leon'],
        'Castilla La Mancha': [
            'Aragon',
            'Valenciana',
            'Murcia',
            'Andalusia',
            'Extremadura',
            'Madrid',
            'Castilla y Leon',
        ],
        'Castilla y Leon': [
            'Galicia',
            'Asturias',
            'Cantabria',
            'Pais Basco',
            'La Rioja',
            'Navarra',
            'Aragon',
            'Castilla La Mancha',
            'Madrid',
            'Extremadura',
        ],
        'Madrid': ['Castilla La Mancha', 'Castilla y Leon'],
        'Islas Baleares': [],
    }

    colors = ['Red', 'Green', 'Blue', 'Violet']

    solver = MapColoring(map_graph, colors)
    if solver.backtrack():
        print('Map coloring solution found')
        solver.print_map()
    else:
        print('No solution exists.')
