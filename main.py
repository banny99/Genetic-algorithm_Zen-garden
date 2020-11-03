from utils import *
from copy import deepcopy
from class_Garden import Garden
from class_Monk import Monk


# --- * MAIN * --- #

# garden_choice = input(" ->Choose garden's plan folder - ")
# garden_file = open(garden_choice, "r")
garden_file = open("gardens/1.txt", "r")
garden_plan = garden_file.readlines()
garden_file.close()

# 1-st file_line - garden size:
size_line = garden_plan[0].split()
size_x = int(size_line[0]) + 2
size_y = int(size_line[1]) + 2

# 2-nd file_line - number of rocks:
rock_num = int(garden_plan[1])
rocks = []
if rock_num > 0:
    rocks = load_rocks(garden_plan)

original_garden = Garden(size_x, size_y, rocks)
all_start_poz = original_garden.free_start_positions

# 1st(-random) population - garden raking:
monk_population = []
size_of_population = random.randint(20, 50)
for i in range(size_of_population):
    garden_copy = deepcopy(original_garden)
    monk = Monk(garden_copy, [], i)

    monk.rake_garden()
    # monk.send_work_report()
    if monk.num_of_raked_places == original_garden.num_of_sand_places:
        print("FINITO - pohrabal som celu zahradu !!!")
        monk.send_work_report()
        break

    monk_population.append(monk)

whole_garden_raked = False
num_of_generation = 1
while not whole_garden_raked and num_of_generation < 100:

    # REPRODUCTION ->next generation:
    new_generation = []
    # vybrat n-novych rodicov ->pre n-novych potomkov = nova generacia:
    for i in range(size_of_population):
        # vyber 2 rodicov turnajom:
        # best1, best2 = tournament_selection(monk_population, random.randint(5, 10))

        # vyber 2 rodicov ruletov:
        best1, best2 = roulette_selection(monk_population)

        # print("\n---\n ->Chosen parents:")
        # best1.send_work_report()
        # best2.send_work_report()

        # vytvor potomka a pridaj do listu potomkov = novej generacie:
        child = create_descendant(best1, best2, all_start_poz, deepcopy(original_garden), i)
        new_generation.append(child)


    # raking the garden:
    monk_population = []
    for monk in new_generation:
        monk.rake_garden()
        # monk.send_work_report()
        # ak sa mu podarilo vsetko pohrabat:
        if monk.num_of_raked_places == original_garden.num_of_sand_places:
            monk_population.append(monk)
            whole_garden_raked = True
            break

        monk_population.append(monk)

    num_of_generation += 1

# ak sa mu podarilo vsetko pohrabat:
if whole_garden_raked:
    print("num of generation: ", num_of_generation)
    print("FINITO - pohrabal som celu zahradu !!!")
    monk_population[-1].send_work_report()
    monk_population[-1].myGarden.print_garden()

else:
    print("Unable to rake whole garden")
    print("num of generations: ", num_of_generation)
    print("Best try: ")
    best_monk = get_best_try(monk_population)
    best_monk.send_work_report()
    best_monk.myGarden.print_garden()