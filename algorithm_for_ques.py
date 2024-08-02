import numpy as np
import random

# Define function to calculate path length
def calculate_length(path, distances):
    total_length = 0
    for i in range(len(path) - 1):
        total_length += distances[path[i]][path[i+1]]
    return total_length

# Define function to update pheromone
def update_pheromone(pheromone_matrix, evaporation_rate, q, path, distances):
    for i in range(len(path) - 1):
        pheromone_matrix[path[i]][path[i+1]] = (1 - evaporation_rate) * pheromone_matrix[path[i]][path[i+1]] + q / calculate_length(path, distances)

# Define function to select next city
def select_next_city(current_city, pheromone_matrix, distances, visibility_factor, visited_cities):
    allowed_cities = [city for city in range(len(pheromone_matrix[current_city])) if city not in visited_cities]
    probabilities = []
    for city in allowed_cities:
        probability = (pheromone_matrix[current_city][city] ** visibility_factor) / distances[current_city][city]
        probabilities.append(probability)
    sum_probabilities = sum(probabilities)
    probabilities = [prob / sum_probabilities for prob in probabilities]
    next_city = random.choices(allowed_cities, probabilities)[0]
    return next_city

# Define ant colony optimization algorithm
def ant_colony_optimization(distances, num_ants, num_iterations, evaporation_rate, q, visibility_factor):
    # Initialize pheromone matrix
    pheromone_matrix = np.ones((len(distances), len(distances)))

    # Main loop of the algorithm
    for iteration in range(num_iterations):
        # Create ants
        ants = []
        for _ in range(num_ants):
            starting_city = 0
            visited_cities = [starting_city]
            path = [starting_city]
            while len(path) < len(distances):
                next_city = select_next_city(path[-1], pheromone_matrix, distances, visibility_factor, visited_cities)
                path.append(next_city)
                visited_cities.append(next_city)
            path.append(starting_city)  # Complete the cycle
            ants.append(path)

        # Calculate path lengths for each ant
        path_lengths = [calculate_length(path, distances) for path in ants]

        # Find the best path
        best_path = ants[np.argmin(path_lengths)]

        # Update pheromone matrix
        for i in range(len(best_path) - 1):
            update_pheromone(pheromone_matrix, evaporation_rate, q, best_path, distances)

    return best_path

# Example usage of the algorithm
if __name__ == "__main__":
    # Define distance matrix
    distances = np.array([
        [0, 10, 15, 20, 25],
        [10, 0, 12, 18, 21],
        [15, 12, 0, 11, 16],
        [20, 18, 11, 0, 14],
        [25, 21, 16, 14, 0]
    ])

    # Set algorithm parameters
    num_ants = 10
    num_iterations = 100
    evaporation_rate = 0.5
    q = 1
    visibility_factor = 2

    # Solve the problem using the algorithm
    best_path = ant_colony_optimization(distances, num_ants, num_iterations, evaporation_rate, q, visibility_factor)

    # Print the best path and its length
    print("Best path:", best_path)
    print("Path length:", calculate_length(best_path, distances))
