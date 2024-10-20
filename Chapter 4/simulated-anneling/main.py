"""
function SIMULATED-ANNEALING(problem, schedule) returns a solution state
    current ← problem.INITIAL
    for t = 1 to ∞ do
        T ← schedule(t)
        if T = 0 then return current
        next ← a randomly selected successor of current
        ∆E ← VALUE(current) – VALUE(next)
        if ∆E > 0 then current ← next
        else current ← next only with probability e∆E/T
"""
import math
import random
import numpy as np
import matplotlib.pyplot as plt


def simulated_annealing(
    initial_state, initial_temperature, cooling_rate, step_size, max_iterations
):
    current_state = initial_state
    current_value = f(current_state)

    temperature = initial_temperature
    iterations = 0

    while iterations < max_iterations and temperature > 1e-6:
        neighbor = generate_neighbor(current_state, step_size)
        neighbor_value = f(neighbor)
        delta = neighbor_value - current_value

        if delta > 0 or random.random() < math.exp(delta / temperature):
            current_state = neighbor
            current_value = neighbor_value
            print('s:', current_state, 't:', temperature, 'it:', iterations)

        temperature *= cooling_rate
        iterations += 1

    return current_state, current_value


def generate_neighbor(state, step_size):
    return state + random.uniform(-step_size, step_size)


def f(x):
    return 1 + 1 / 4000 * x**2 - np.cos(x / np.sqrt(100))


if __name__ == '__main__':
    random.seed(42)
    initial_state = random.uniform(0, 100)
    initial_temperature = 100
    cooling_rate = 0.95
    step_size = 10
    max_iterations = 1000
    state, value = simulated_annealing(
        initial_state,
        initial_temperature,
        cooling_rate,
        step_size,
        max_iterations,
    )
    print(f'Optimal state: {state:.6f}, Optimal value: {value:.6f}')

    # Plot the function and the result state
    xs = np.linspace(-1000, 1000, 1000000)
    ys = [f(x) for x in xs]

    plt.figure(figsize=(10, 6))
    # Plot the function
    plt.plot(xs, ys, label='f(x) = -x^2 + 4x')

    # Mark the final state
    plt.axvline(
        state, color='r', linestyle='--', label=f'Optimal state: {state:.6}'
    )
    plt.scatter([state], [value], color='r')

    # Plot settings
    plt.title('Simulated Annealing Optimization')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()
    plt.grid(True)
    plt.show()
