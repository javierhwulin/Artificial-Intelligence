"""
function HILL-CLIMBING(problem) returns a state that is a local maximum
    current ← problem.INITIAL
    while true do
        neighbor ← a highest-valued successor state of current
        if VALUE(neighbor) ≤ VALUE(current) then return current
        current ← neighbor

For finding the highest-valued successor state,
check more neighbors to find a state with higher value
"""
import random
import numpy as np
import matplotlib.pyplot as plt


def hill_climbing(initial_state, step_size, max_iterations):
    current_state = initial_state
    current_value = f(current_state)
    iterations = 0

    # Store states and values for plotting
    states = [current_state]
    values = [current_value]

    while iterations < max_iterations:
        better_found = False

        for _ in range(100):
            neighbor = generate_neighbor(current_state, step_size)
            neighbor_value = f(neighbor)

            if neighbor_value > current_value:
                current_state = neighbor
                current_value = neighbor_value
                better_found = True

                # Store the new state and values
                states.append(current_state)
                values.append(current_value)
                break
        if not better_found:
            break

        iterations += 1

    return current_state, current_value, states, values


def generate_neighbor(state, step_size):
    return state + random.uniform(
        -step_size, step_size
    )   # Small perturbation around current state


def f(x):
    return -x**2+4*x  # Define function to find maximum


if __name__ == '__main__':
    # Initial state, step size, and max iterations
    initial_state = random.uniform(0, 100)
    step_size = 0.01
    max_iterations = 1e6

    #  Run hill-climbing and get states and values at each step
    state, value, states, values = hill_climbing(
        initial_state, step_size, max_iterations
    )

    # Plot the function and the result state
    xs = np.linspace(-100, 100, 1000)
    ys = [f(x) for x in xs]

    # Plot the function
    plt.plot(xs, ys, label='f(x) = -x^2 + 4x')

    # Plot the iterations
    plt.plot(states, values, '-', label='Iterations')

    # Mark the final state
    plt.axvline(state, color='r', linestyle='--', label=f'State: {state}')
    plt.scatter([state], [value], color='r')  # Mark the found state

    # Plot settings
    plt.title('Hill Climbing Optimization')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()
    plt.show()
