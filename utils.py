import random
from class_Monk import Monk
from copy import deepcopy


def load_rocks(garden_plan):
    rocks = []
    for line in garden_plan[2:]:
        rock_info = line.split()
        rock = (int(rock_info[0])+1, int(rock_info[1])+1)
        rocks.append(rock)
    return rocks


# generate first-random population genomes:
def create_genome(genome_size, start_positions):

    random_genome = [random.choice(start_positions)]
    for j in range(genome_size):
        random_genome.append(random.choice(['l', 'r']))

    return random_genome


# ->Generation raking simulation:
def simulate_generation(old_monk_population, size_of_population, genome_size, mutation_probability, original_garden, num_of_generation):

    new_monk_population = []
    whole_garden_raked = False
    all_start_poz = original_garden.free_start_positions

    for i in range(size_of_population):

        # ak je to prva generacia
        if num_of_generation == 1:
            garden_copy = deepcopy(original_garden)
            random_genome = create_genome(genome_size, garden_copy.free_start_positions)
            monk = Monk(garden_copy, random_genome, i)

        else:
            # vyber 2 rodicov turnajom:
            # best1, best2 = tournament_selection(old_monk_population, random.randint(5, 10))
            # vyber 2 rodicov ruletov:
            best1, best2 = roulette_selection(old_monk_population)

            # print("\n---\n ->Chosen parents:")
            # best1.send_work_report()
            # best2.send_work_report()

            # vytvor potomka a pridaj do listu potomkov = novej generacie:
            monk = create_descendant(best1, best2, deepcopy(original_garden), i, mutation_probability)

        monk.rake_garden()
        # monk.send_work_report()
        new_monk_population.append(monk)

        # ak sa podarilo pohrabat celu zahradu
        if monk.num_of_raked_places == original_garden.num_of_sand_places:
            whole_garden_raked = True
            break

    return new_monk_population, whole_garden_raked



# --- REPRODUCTION --- #

# ->Selections:
def tournament_selection(monk_population, n):

    tournament_member_indexes = []
    # vyber nahodnych mnichov do turnaja (bez opakovani?)
    for i in range(n):
        # vyber nahodneho mnicha
        random_monk_poz_index = random.randrange(len(monk_population))
        # ak uz mnich already je v turnaji ->vyberaj dalsieho, pokym nevyberies takeho aky tam este nie je (-aby sa neopakovali mnisi v turnaji)
        while random_monk_poz_index in tournament_member_indexes:
            random_monk_poz_index = random.randrange(len(monk_population))

        tournament_member_indexes.append(random_monk_poz_index)


    best_monk1 = None
    best_monk2 = None
    # vyber najlepsich 2 mnichov z turnaja
    for monk_index in tournament_member_indexes:
        monk_competitor = monk_population[monk_index]
        if (best_monk1 == None) or (monk_competitor.num_of_raked_places > best_monk1.num_of_raked_places):
            best_monk2 = best_monk1
            best_monk1 = monk_competitor
        elif (best_monk2 == None) or (monk_competitor.num_of_raked_places > best_monk2.num_of_raked_places):
            best_monk2 = monk_competitor

    return best_monk1, best_monk2


def roulette_selection(monk_population):

    total_fintess = 0
    # celkova fitness celej populacie mnichov
    for monk in monk_population:
        total_fintess += monk.num_of_raked_places

    cummulative_probabilities = []
    # vypocet pravdepodobnosti vyberu jednotlivych mnichov
    for monk in monk_population:
        monk_probability = monk.num_of_raked_places / total_fintess

        if len(cummulative_probabilities) == 0:
            cummulative_probabilities.append(monk_probability)
        else:
            cummulative_probabilities.append(cummulative_probabilities[-1] + monk_probability)

    # vyber n(2?)-mnichov ruletov
    chosen_monks = []
    for n in range(2):
        r = random.uniform(0, 1)
        for i in range(len(cummulative_probabilities)):
            if r <= cummulative_probabilities[i]:
                chosen_monks.append(monk_population[i])
                break

    return chosen_monks[0], chosen_monks[1]


# ->Child creation:
def create_descendant(parent1, parent2, childs_garden, index, mutation_probability):
    # krizenie:
    child_genes = crossover(parent1.DNA, parent2.DNA)
    # mutacia:
    child_genes = mutation(child_genes, mutation_probability)

    child = Monk(childs_garden, child_genes, index)

    return child

# ->Krizenie:
def crossover(genes1, genes2):
    # # cia polovica bude prva:
    # whose = random.choice([1, 2])

    # # 50/50:
    # cut_point = len(genes1)//2
    # child_genes = genes1[:cut_point] + genes2[cut_point:]

    # random cut-point:
    cut_point = random.randrange(1, len(genes1))
    child_genes = genes1[:cut_point] + genes2[cut_point:]

    return child_genes

# ->Mutacia:
def mutation(child_genes, mutation_probability):

    # mutation_probability = 0.25
    if random.random() <= mutation_probability:
        random_gene_to_change = random.randrange(1, len(child_genes))

        # child_genes[random_gene_to_change] = random.choice(['l', 'r'])

        if child_genes[random_gene_to_change] == 'l':
            child_genes[random_gene_to_change] = 'r'
        elif child_genes[random_gene_to_change] == 'r':
            child_genes[random_gene_to_change] = 'l'

    return child_genes



# -Najlepsi pokus- #
def get_best_try(monk_population, num_of_generation, best_try):
    curr_best_fitness = None
    curr_best_monk = None

    # najde nejlepsieho mnicha tejto generacie:
    for monk in monk_population:
        fitness = monk.num_of_raked_places
        if curr_best_fitness == None or fitness > curr_best_fitness:
            curr_best_fitness = fitness
            curr_best_monk = monk

    best_monk = best_try[0]
    # ak je najlepsi z tejto lepsi jak celkovy:
    if curr_best_fitness >= best_monk.num_of_raked_places:
        best_try = (curr_best_monk, num_of_generation)

    return best_try


def get_best_monk(monk_population):
    best_fitness = None
    best_monk = None

    for monk in monk_population:
        fitness = monk.num_of_raked_places
        if best_fitness == None or fitness > best_fitness:
            best_fitness = fitness
            best_monk = monk

    return best_monk

