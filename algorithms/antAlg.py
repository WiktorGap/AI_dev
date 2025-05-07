import random
import math

class Ant:
    def __init__(self, num_of_attractions):
        self.num_of_attractions = num_of_attractions
        self.visited = [random.randint(0, num_of_attractions - 1)]
    
    def visit_attraction_parabolistic(self, pheromone_map, alpha, beta, distance_matrix):
        current_attraction = self.visited[-1]
        all_attractions = list(range(self.num_of_attractions))
        available_attractions = [atr for atr in all_attractions if atr not in self.visited]
        
        probabilities = []
        for attraction in available_attractions:
            pheromone = math.pow(pheromone_map[current_attraction][attraction], alpha)
            heuristic = math.pow(1 / distance_matrix[current_attraction][attraction], beta)
            probability = pheromone * heuristic
            probabilities.append(probability)
        
        total = sum(probabilities)
        if total == 0:
            normalized = [1/len(probabilities) for _ in probabilities]  
        else:
            normalized = [p / total for p in probabilities]

        return available_attractions, normalized
    
    def roulette_select(self, available_attractions, probabilities):
        ranges = []
        total = 0
        for idx, prob in zip(available_attractions, probabilities):
            ranges.append((idx, total, total + prob))
            total += prob
        
        draw = random.random()
        for idx, start, end in ranges:
            if start < draw <= end:
                return idx
        
        return available_attractions[-1]

    def get_distance(self, distance_matrix):
        total_distance = 0
        for i in range(1, len(self.visited)):
            from_attraction = self.visited[i - 1]
            to_attraction = self.visited[i]
            total_distance += distance_matrix[from_attraction][to_attraction]
        return total_distance

    def configure_pheromones(self, initial_value, distance_matrix, pheromone_map):
        for x in range(len(distance_matrix)):
            for y in range(len(distance_matrix)):
                pheromone_map[x][y] = initial_value

    def update_pheromones(self, pheromone_map, distance_matrix, evaporation_rate, colony):
        num_of_attractions = len(distance_matrix)
        for x in range(num_of_attractions):
            for y in range(num_of_attractions):
                pheromone_map[x][y] *= evaporation_rate
                for ant in colony:
                    pheromone_map[x][y] += 1 / ant.get_distance(distance_matrix)

    def get_best_ant(self, colony, previous_best, distance_matrix):
        best_ant = previous_best
        best_distance = previous_best.get_distance(distance_matrix) if previous_best else float('inf')

        for ant in colony:
            distance = ant.get_distance(distance_matrix)
            if distance < best_distance:
                best_ant = ant
                best_distance = distance
        
        return best_ant

    def solve(self, num_of_iterations, evaporation_rate, colony_multiplier, num_of_attractions,
              initial_pheromone_value, distance_matrix, pheromone_map, alpha=1, beta=2):
        self.configure_pheromones(initial_pheromone_value, distance_matrix, pheromone_map)
        best_ant = None
        
        for _ in range(num_of_iterations):
            colony = ant_configuration(colony_multiplier, num_of_attractions)
            for _ in range(num_of_attractions - 1):
                move_ants(colony, pheromone_map, alpha, beta, distance_matrix)
            self.update_pheromones(pheromone_map, distance_matrix, evaporation_rate, colony)
            best_ant = self.get_best_ant(colony, best_ant if best_ant else colony[0], distance_matrix)
        
        return best_ant


def ant_configuration(num_of_ants, num_of_attractions):
    return [Ant(num_of_attractions) for _ in range(num_of_ants)]

def move_ants(colony, pheromone_map, alpha, beta, distance_matrix):
    for ant in colony:
        available_attractions, probabilities = ant.visit_attraction_parabolistic(pheromone_map, alpha, beta, distance_matrix)
        if available_attractions:
            selected = ant.roulette_select(available_attractions, probabilities)
            ant.visited.append(selected)


def test_full_ant_colony():
    distance_matrix = [
        [0, 2, 9, 10, 7],
        [1, 0, 6, 4, 3],
        [15, 7, 0, 8, 12],
        [6, 3, 12, 0, 5],
        [10, 4, 8, 5, 0]
    ]

    pheromone_map = [[1 for _ in range(5)] for _ in range(5)]

    starting_ant = Ant(5)

    best_ant = starting_ant.solve(
        num_of_iterations=20,
        evaporation_rate=0.5,
        colony_multiplier=10,
        num_of_attractions=5,
        initial_pheromone_value=1,
        distance_matrix=distance_matrix,
        pheromone_map=pheromone_map,
        alpha=1,
        beta=2
    )

    print("Best route:", best_ant.visited)
    print("Best distance:", best_ant.get_distance(distance_matrix))

if __name__ == "__main__":
    test_full_ant_colony()
