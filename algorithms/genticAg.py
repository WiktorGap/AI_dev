import random


def generate_beginning_population(depth, length):
    population = []
    for _ in range(depth):
        member = []
        for _ in range(length):
            element = random.randint(0, 1)
            member.append(element)
        population.append(member)
    return population

def calculate_member_fitness(member, objects_in_backpack, backpack_capacity):
    total_weight = 0
    total_value = 0
    for i in range(len(member)):
        actual_bit = member[i]
        if actual_bit == 1:
            total_weight += objects_in_backpack[i][0]  # weight
            total_value += objects_in_backpack[i][1]   # value
            if total_weight > backpack_capacity:
                return 0
    return total_value


def total_fitness(population, objects_in_backpack, backpack_capacity):
    total = 0
    for member in population:
        total += calculate_member_fitness(member, objects_in_backpack, backpack_capacity)
    return total

def set_probability_in_population(population, objects_in_backpack, backpack_capacity):
    probability_table = []
    total_fitness_ = total_fitness(population, objects_in_backpack, backpack_capacity)
    for member in population:
        fitness = calculate_member_fitness(member, objects_in_backpack, backpack_capacity)
        if total_fitness_ == 0:
            probability = 0
        else:
            probability = fitness / total_fitness_
        probability_table.append(probability)
    return probability_table


def roulette_selection(population, objects_in_backpack, backpack_capacity, num_of_selected):
    probabilities = set_probability_in_population(population, objects_in_backpack, backpack_capacity)
    cumulative_probabilities = []
    cumulative = 0
    for prob in probabilities:
        cumulative += prob
        cumulative_probabilities.append(cumulative)
    
    selected_members = []
    for _ in range(num_of_selected):
        r = random.random()  
        for idx, cum_prob in enumerate(cumulative_probabilities):
            if r <= cum_prob:
                selected_members.append(population[idx])
                break
    return selected_members


def onePointCrosing(parent_a, parent_b, crossingPoint):
    child_1 = parent_a[:crossingPoint] + parent_b[crossingPoint:]
    child_2 = parent_b[:crossingPoint] + parent_a[crossingPoint:]
    return [child_1, child_2]


def mutate_member(member):
    random_idx = random.randrange(len(member)) 
    if member[random_idx] == 0:
        member[random_idx] = 1
    else:
        member[random_idx] = 0
    return member

def executeAlg(sizeOfPopulation, numOfPopulations, backpack_capacity, objects_in_backpack, num_of_selected, crossingPoint):
    bestGlobalFitness = 0
    globalPopulation = generate_beginning_population(sizeOfPopulation, len(objects_in_backpack))
    
    for _ in range(numOfPopulations):
        for member in globalPopulation:
            actualBestFitness = calculate_member_fitness(member, objects_in_backpack, backpack_capacity)
            if actualBestFitness > bestGlobalFitness:
                bestGlobalFitness = actualBestFitness
        

        selected = roulette_selection(globalPopulation, objects_in_backpack, backpack_capacity, num_of_selected)

        parents = []
        for i in range(0, len(selected)-1, 2):
            parents.append((selected[i], selected[i+1]))

        childs = []
        for parent in parents:
            parentA = parent[0]
            parentB = parent[1]
            new_children = onePointCrosing(parentA, parentB, crossingPoint)
            childs.extend(new_children)
        

        for child in childs:
            mutate_member(child)
        

        globalPopulation = globalPopulation + childs
    
    return bestGlobalFitness, globalPopulation


objects = [
    (2, 3),
    (1, 2),
    (3, 6),
    (2, 1),
    (1, 3),
    (5, 10),
    (2, 4),
    (4, 7)
]

backpack_capacity = 10
population = generate_beginning_population(4, len(objects))

print("Generated Population:")
for member in population:
    print(member)


print("\nFitness for each member:")
for member in population:
    fitness = calculate_member_fitness(member, objects, backpack_capacity)
    print(f"Member: {member} -> Fitness (Total Value): {fitness}")

print("------")
print("Total fitness for members:")
total_fitness_population = total_fitness(population, objects, backpack_capacity)
print(total_fitness_population)


print("\nProbability for each member:")
probabilities = set_probability_in_population(population, objects, backpack_capacity)
for idx, prob in enumerate(probabilities):
    print(f"Member {idx}: Probability = {prob:.4f}")

print("\n--- Roulette Selection Test ---")
selected = roulette_selection(population, objects, backpack_capacity, num_of_selected=2)
print("Selected members:")
for member in selected:
    print(member)


bestFitness, finalPopulation = executeAlg(sizeOfPopulation=10, numOfPopulations=10, backpack_capacity=backpack_capacity, objects_in_backpack=objects, num_of_selected=4, crossingPoint=3)
print(f"\nBest fitness: {bestFitness}")
print("\nFinal Population:")
for member in finalPopulation:
    print(member)
