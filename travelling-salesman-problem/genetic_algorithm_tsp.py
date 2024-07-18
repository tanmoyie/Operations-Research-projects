import random
import numpy as np


class GeneticAlgorithmTSP:
    def __init__(self, distance_matrix, pop_size=100, num_generations=500, mutation_rate=0.01):
        self.distance_matrix = distance_matrix
        self.num_cities = len(distance_matrix)
        self.pop_size = pop_size
        self.num_generations = num_generations
        self.mutation_rate = mutation_rate
        self.population = self.create_initial_population()

    def create_initial_population(self):
        population = []
        for _ in range(self.pop_size):
            individual = list(np.random.permutation(self.num_cities))
            population.append(individual)
            # print('Initial Population: ', population)
        return population

    def calculate_fitness(self, individual):
        total_distance = 0
        for i in range(self.num_cities - 1):
            total_distance += self.distance_matrix[individual[i], individual[i + 1]]
        total_distance += self.distance_matrix[individual[-1], individual[0]]  # Return to the start
        return total_distance

    def selection(self):
        fitness_scores = [self.calculate_fitness(ind) for ind in self.population]
        probabilities = [1 / score for score in fitness_scores]
        total_prob = sum(probabilities)
        probabilities = [prob / total_prob for prob in probabilities]
        # print(len(range(self.pop_size)), len(probabilities))
        selected_indices = np.random.choice(range(self.pop_size), size=self.pop_size, p=probabilities)
        return [self.population[i] for i in selected_indices]

    def crossover(self, parent1, parent2):
        size = len(parent1)
        start, end = sorted(random.sample(range(size), 2))
        child = [None] * size
        child[start:end] = parent1[start:end]

        pointer = end
        for gene in parent2:
            if gene not in child:
                if pointer >= size:
                    pointer = 0
                # print('-----')
                # print('child, pointer', child, pointer)

                while child[pointer-1] is not None:
                    pointer += 1
                child[pointer-1] = gene

        return child

    def mutate(self, individual):
        for i in range(len(individual)):
            if random.random() < self.mutation_rate:
                j = random.randint(0, len(individual) - 1)
                individual[i], individual[j] = individual[j], individual[i]
        return individual

    def evolve_population(self):
        for generation in range(self.num_generations):
            parents = self.selection()
            next_population = []
            for i in range(0, len(parents), 2):

                parent1, parent2 = parents[i], parents[i + 1]
                child1, child2 = self.crossover(parent1, parent2), self.crossover(parent2, parent1)
                next_population.extend([self.mutate(child1), self.mutate(child2)])
            self.population = next_population

            print('Initial population: ', self.population)

            best_fitness = min(self.calculate_fitness(ind) for ind in self.population)
            # fitness function of distance, so we minimize this distance
            # print(f"Generation {generation}: Best Fitness = {best_fitness}")

        best_individual = min(self.population, key=self.calculate_fitness)
        return best_individual, self.calculate_fitness(best_individual)
