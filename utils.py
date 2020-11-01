import random

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