from utils import *
from class_Garden import Garden
import matplotlib.pyplot as plt


# --- * MAIN * --- #

garden_choice = input(" ->Choose garden's plan folder - ")
garden_file = open(garden_choice, "r")
# garden_file = open("gardens/1.txt", "r")
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


# - initialization - #
original_garden = Garden(size_x, size_y, rocks)

# size_of_population = random.randint(20, 100)
# size_of_population = 100
size_of_population = int(input("set number of members in one population:\n "))

# DNA_size = size_x-2 + size_y-2 + rock_num
# DNA_size = 10
DNA_size = int(input("set DNA size:\n "))
while DNA_size > size_x-2 + size_y-2 + rock_num:
    print("-DNA size must not be bigger than ", size_x-2 + size_y-2 + rock_num, "(size_x + size_y + num. of rocks)")
    DNA_size = int(input("set DNA size:\n "))

# parent selection type:
parent_selection = input("choose type of parent selection;\n \"r\" -for Roulette selection\n \"t\" -for Tournament selection\n")

# mutation_probability = 0.5
mutation_probability = float(input("set mutation probability:\n "))

gen_num_limit = 200
monk_population = []
whole_garden_raked = False
impossible_to_rake_garden = False
new_blood_executed = True
new_blood_counter = 0
best_try = (None, 0)
average_fitnesses_arr = []
all_fitnesses_arr = []
best_monks_fitnesses = []


num_of_generation = 0
while not whole_garden_raked and not impossible_to_rake_garden and num_of_generation < gen_num_limit:
    num_of_generation += 1

    # whole generation raking simulation:
    monk_population, whole_garden_raked = simulate_generation(monk_population, size_of_population, DNA_size, mutation_probability, original_garden, num_of_generation, parent_selection)

    # New blood:
    new_blood_counter += 1
    if new_blood_counter >= 100:
        print("\n ->NEW BLOOD")
        monk_population = new_blood(monk_population, original_garden, DNA_size)
        new_blood_counter = 0

    average_fitness = get_average_fitness(monk_population)
    average_fitnesses_arr.append(average_fitness)
    all_fitnesses_arr = append_fitnesses(all_fitnesses_arr, monk_population)
    curr_best_monk = get_best_monk(monk_population)
    best_monks_fitnesses.append(curr_best_monk.num_of_raked_places)
    # print("\nGeneration n.", num_of_generation, ":\n - best fitness =", curr_best_monk.num_of_raked_places, "\n - average fitness =", average_fitness)

    best_try = get_best_try(monk_population, num_of_generation, best_try)



#       ---  END  ---      #

if impossible_to_rake_garden:
    print("\nImpossible to rake garden")

# ak sa mu podarilo vsetko pohrabat:
elif whole_garden_raked:
    print("\n----------\nFINITO -pohrabal som celu zahradu !!!")
    print(" num of generations passed: ", num_of_generation, '\n')
    monk_population[-1].send_work_report()
    monk_population[-1].myGarden.print_garden()

else:
    print("\n----------\nGarden raking -UNsuccessful")
    print(" num of generations passed (limit): ", num_of_generation, '\n')
    print("Best try ->monk from generation n. -", best_try[1], ':')
    best_try[0].send_work_report()
    best_try[0].myGarden.print_garden()


# Graph:

x = list(range(1, num_of_generation+1))
y = average_fitnesses_arr

# plt.plot(x, y)
plt.plot(x, y, color='green', linestyle='dashed', linewidth=1,
         marker='o', markerfacecolor='blue', markersize=5)

plt.xlim(1, gen_num_limit)
plt.ylim(1, original_garden.num_of_sand_places)

plt.xlabel('Generation num.')
plt.ylabel('Average fitness')
plt.title('Average fitnesses cross generations')

plt.show()

# -------------------

# x = list(range(1, len(best_monks_fitnesses)+1))
# y = best_monks_fitnesses
#
# plt.plot(x, y, color='green', linestyle='dashed', linewidth=1,
#          marker='o', markerfacecolor='blue', markersize=5)
#
# plt.xlim(1, len(best_monks_fitnesses))
# plt.ylim(1, original_garden.num_of_sand_places)
#
# plt.xlabel('Monk num.')
# plt.ylabel('Best monk')
# plt.title('Best fitnesses cross generations')
#
# plt.show()