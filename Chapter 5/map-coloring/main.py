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
