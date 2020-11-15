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


# generate first-random population DNAs:
def create_DNA(DNA_size, all_start_positions):
    random_DNA = []
    starting_poz = [1]
    turn_choices = [1]

    for j in range(DNA_size//2):
        turn_choices.append(random.choice(['l', 'r']))
        random_start_poz = random.choice(all_start_positions)
        while random_start_poz in starting_poz:
            random_start_poz = random.choice(all_start_positions)
        starting_poz.append(random_start_poz)

    random_DNA.append(starting_poz)
    random_DNA.append(turn_choices)
    return random_DNA


# ->Generation raking simulation:
def simulate_generation(old_monk_population, size_of_population, DNA_size, mutation_probability, original_garden, num_of_generation, parent_selection):

    new_monk_population = []
    whole_garden_raked = False

    for i in range(size_of_population):

        # ak je to prva generacia
        if num_of_generation == 1:
            garden_copy = deepcopy(original_garden)
            random_DNA = create_DNA(DNA_size, garden_copy.free_start_positions)
            monk = Monk(garden_copy, random_DNA, i)

        else:
            if parent_selection == 't':
                # vyber 2 rodicov turnajom:
                parent1 = tournament_selection(old_monk_population, random.randint(2, 5))
                parent2 = tournament_selection(old_monk_population, random.randint(2, 5))
            else:
                # vyber 2 rodicov ruletov:
                parent1, parent2 = roulette_selection(old_monk_population)

            # vytvor potomka a pridaj do listu potomkov = novej generacie:
            monk = create_descendant(parent1, parent2, deepcopy(original_garden), i, mutation_probability)

        monk.rake_garden()
        # ak skoncil v strede zahrady:
        # if monk.myGarden.garden_grid[monk.myPoz_y][monk.myPoz_x] != -1:
        #     monk.num_of_raked_places = monk.num_of_raked_places//2
        new_monk_population.append(monk)

        # ak sa podarilo pohrabat celu zahradu
        if monk.num_of_raked_places == original_garden.num_of_sand_places:
            whole_garden_raked = True
            break

    return new_monk_population, whole_garden_raked



# --- REPRODUCTION --- #

# ->Selections:
def tournament_selection(monk_population, n):

    tournament_members = []
    # vyber nahodnych mnichov do turnaja
    for i in range(n):
        # vyber nahodneho mnicha
        tournament_members.append(random.choice(monk_population))

    best_monk = None
    for monk_competitor in tournament_members:
        if (best_monk == None) or (monk_competitor.num_of_raked_places > best_monk.num_of_raked_places):
            best_monk = monk_competitor

    return best_monk


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

    # vyber n(2?) mnichov ruletov
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
    child_DNA = crossover(parent1.DNA, parent2.DNA)
    # mutacia:
    child_DNA = mutation(child_DNA, mutation_probability, childs_garden)

    child = Monk(childs_garden, child_DNA, index)
    return child

# ->Krizenie:
def crossover(DNA1, DNA2):
    child_DNA = []

    # random cut-point:
    cut_point = random.randrange(1, len(DNA1[0])-1)
    child_starting_poz = ([1] + DNA1[0][1:cut_point] + DNA2[0][cut_point:])

    cut_point = random.randrange(1, len(DNA2[1]) - 1)
    child_turn_choices = ([1] + DNA1[1][1:cut_point] + DNA2[1][cut_point:])

    child_DNA.append(child_starting_poz)
    child_DNA.append(child_turn_choices)

    return child_DNA

# ->Mutacia:
def mutation(childs_DNA, mutation_probability, childs_garden):

    if random.random() <= mutation_probability:

        random_gene_to_change = random.randrange(1, len(childs_DNA[0]))
        random_start_poz = random.choice(childs_garden.free_start_positions)
        while random_start_poz in childs_DNA[0]:
            random_start_poz = random.choice(childs_garden.free_start_positions)
        childs_DNA[0][random_gene_to_change] = random_start_poz

        random_gene_to_change = random.randrange(1, len(childs_DNA[1]))
        if childs_DNA[1][random_gene_to_change] == 'l':
            childs_DNA[1][random_gene_to_change] = 'r'
        elif childs_DNA[1][random_gene_to_change] == 'r':
            childs_DNA[1][random_gene_to_change] = 'l'

    return childs_DNA


# New blood:
def new_blood(monk_population, original_garden, DNA_size):
    kill_num = int(input("what percentage of the population should be killed ?\n "))
    kill_num = int((kill_num * len(monk_population)) / 100.0)

    for i in range(kill_num):
        random_index = random.randrange(1, len(monk_population))
        del(monk_population[random_index])

        garden_copy = deepcopy(original_garden)
        random_DNA = create_DNA(DNA_size, garden_copy.free_start_positions)
        monk = Monk(garden_copy, random_DNA, i)
        monk.rake_garden()
        monk_population.append(monk)

    return monk_population


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

    # ak je najlepsi z tejto lepsi jak celkovy:
    if best_try[0] == None or curr_best_fitness >= best_try[0].num_of_raked_places:
        best_try = (curr_best_monk, num_of_generation)
        print("gen. num: " + str(best_try[1]) + "; fitness-" + str(best_try[0].num_of_raked_places))

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


def get_average_fitness(monk_population):

    fitness_sum = 0
    for monk in monk_population:
        fitness_sum += monk.num_of_raked_places

    return fitness_sum//len(monk_population)


def append_fitnesses(all_fitnesses_arr, monk_population):
    for monk in monk_population:
        all_fitnesses_arr.append(monk.num_of_raked_places)

    return all_fitnesses_arr