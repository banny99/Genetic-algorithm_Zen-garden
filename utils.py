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
    for i in range(n):
        random_monk_poz_index = random.randrange(len(monk_population))
        while random_monk_poz_index in tournament_member_indexes:
            random_monk_poz_index = random.randrange(len(monk_population))

        tournament_member_indexes.append(random_monk_poz_index)

    best_monk1 = None
    best_monk2 = None
    for i in range(n):
        random_monk = monk_population[tournament_member_indexes[i]]
        if (best_monk1 == None) or (random_monk.num_of_raked_places > best_monk1.num_of_raked_places):
            best_monk2 = best_monk1
            best_monk1 = random_monk
        elif (best_monk2 == None) or (random_monk.num_of_raked_places > best_monk2.num_of_raked_places):
            best_monk2 = random_monk

    return best_monk1, best_monk2