import sys
import numpy as np
import time

from utils.data import load_tsp_file, normalize_coordinates
from utils.ops import find_nearest_neighbor, calculate_euclidean_distances, compute_route_length, create_network, calculate_neighborhood, determine_route
from utils.plot import visualize_network, visualize_route

def main():
    if len(sys.argv) != 2:
        print("Usage: python src/main.py <filename>.tsp")
        return -1

    tsp_problem = load_tsp_file(sys.argv[1])

    optimal_route = self_organizing_map(tsp_problem, 100000)

    tsp_problem = tsp_problem.reindex(optimal_route)

    total_distance = compute_route_length(tsp_problem)

    print(f'Route found with total distance: {total_distance}')

def self_organizing_map(problem, num_iterations, initial_learning_rate=0.8):
    """Solve the Traveling Salesman Problem using a Self-Organizing Map (SOM)."""

    # Normalize the cities' coordinates to fit within [0,1]
    cities = problem.copy()
    cities[['x', 'y']] = normalize_coordinates(cities[['x', 'y']])

    # Set the size of the neuron network as 8 times the number of cities
    network_size = cities.shape[0] * 8

    # Generate a neural network with the specified size
    neuron_network = create_network(network_size)
    print(f'Created a network of {network_size} neurons. Starting iterations...')

    for iteration in range(num_iterations):
        if iteration % 100 == 0:
            print(f'\t> Iteration {iteration}/{num_iterations}', end="\r")

        # Select a random city
        selected_city = cities.sample(1)[['x', 'y']].values
        nearest_index = find_nearest_neighbor(neuron_network, selected_city)

        # Generate a Gaussian filter centered on the winning neuron
        gaussian_filter = calculate_neighborhood(nearest_index, network_size // 10, neuron_network.shape[0])

        # Update the neuron weights to move closer to the selected city
        neuron_network += gaussian_filter[:, np.newaxis] * initial_learning_rate * (selected_city - neuron_network)

        # Gradually decay the learning rate and neighborhood size
        initial_learning_rate *= 0.99997
        network_size *= 0.9997

        # Plot the network at specified intervals
        if iteration % 1000 == 0:
            visualize_network(cities, neuron_network, output_file=f'results/{iteration:05d}.png')

        # Check for complete decay of parameters
        if network_size < 1:
            print(f'Radius has completely decayed, stopping at {iteration} iterations.')
            break
        if initial_learning_rate < 0.001:
            print(f'Learning rate has completely decayed, stopping at {iteration} iterations.')
            break
    else:
        print(f'Completed all {num_iterations} iterations.')

    # Final network and route visualization
    visualize_network(cities, neuron_network, output_file='results/final.png')
    final_route = determine_route(cities, neuron_network)
    visualize_route(cities, final_route, 'results/route.png')

    return final_route

if __name__ == '__main__':
    start_time = time.time()
    main()
    print(f"Execution Time (ms): {time.time() - start_time}")
