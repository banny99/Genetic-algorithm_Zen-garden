import random
from class_Monk import Monk

def load_rocks(garden_plan):
    rocks = []
    for line in garden_plan[2:]:
        rock_info = line.split()
        rock = (int(rock_info[0])+1, int(rock_info[1])+1)
        rocks.append(rock)
    return rocks


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

    monk_probabilities = []
    cummulative_probabilities = []
    # vypocet pravdepodobnosti vyberu jednotlivych mnichov
    for monk in monk_population:
        monk_probability = monk.num_of_raked_places / total_fintess
        monk_probabilities.append(monk_probability)

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


def create_descendant(parent1, parent2, all_start_poz, childs_garden, index):
    # krizenie:
    child_genes = crossover(parent1.starting_positions, parent2.starting_positions)

    # mutacia:
    child_genes = mutation(child_genes, all_start_poz)

    child = Monk(childs_garden, child_genes, index)

    return child

def crossover(genes1, genes2):
    # 50/50:
    child_genes = genes1[:len(genes1)//2] + genes2[len(genes2)//2:]

    # removeDuplicate touples (-> tato metode meni poradie-vadi to ?):
    child_genes = list(set([i for i in child_genes]))

    return child_genes


def mutation(child_genes, all_start_poz):
    mutation_probability = 0.25

    if random.random() < mutation_probability:
        random_gene = all_start_poz[random.randrange(0, len(all_start_poz))]
        # nahodny gen zmen za iny nahodny ak sa tam este nenachadza:
        if random_gene not in child_genes:
            child_genes[random.randrange(0, len(child_genes))] = random_gene

    return child_genes



def get_best_try(last_population):

    best_fitness = None
    best_monk = None
    for monk in last_population:
        fitness = monk.num_of_raked_places
        if best_fitness == None or fitness > best_fitness:
            best_fitness = fitness
            best_monk = monk


    return best_monk