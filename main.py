from utils import *
from class_Garden import Garden

''' 
-zmenit genom [x,y,l,p,p,l,p,p,l,...] -done
-strhavat fitness(ked skonci uprostred) -???
-"nova krv" (ak sa stuck-nu) -> do 50. gen ak nenajdu =>nova krv -done
-upravit:
    krizenie [-nahodne cislo randrange(1, len(genom))->podla toho cast z 1. a 2. rodica ] -done
    mutaciu [-nahodne cislo randrange(1, len(genom))->ten gen zmen na iny ] -done
'''

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


# - initialization - #
original_garden = Garden(size_x, size_y, rocks)

# size_of_population = random.randint(20, 100)
# size_of_population = 100
size_of_population = int(input("set number of members in one population:\n "))

# genome_size = size_x-2 + size_y-2 + rock_num
# genome_size = 10
genome_size = int(input("set genome size:\n "))
while genome_size >= size_x-2 + size_y-2 + rock_num:
    print("genome size must not be bigger than ", size_x-2 + size_y-2 + rock_num)
    genome_size = int(input("set genome size:\n "))

# mutation_probability = 0.5
mutation_probability = float(input("set mutation probability:\n "))

gen_num_limit = 100
monk_population = []
whole_garden_raked = False
impossible_to_rake_garden = False
new_blood_executed = True
best_try = (None, 0)


num_of_generation = 0
while not whole_garden_raked and not impossible_to_rake_garden and num_of_generation < gen_num_limit:
    num_of_generation += 1

    # New blood:
    if num_of_generation > gen_num_limit//2 and new_blood_executed:
        print("\n ->NEW BLOOD")
        monk_population = new_blood(monk_population, original_garden, genome_size)
        new_blood_executed = False

    # whole generation raking simulation:
    monk_population, whole_garden_raked = simulate_generation(monk_population, size_of_population, genome_size, mutation_probability, original_garden, num_of_generation)

    # curr_best_monk = get_best_monk(monk_population)
    # average_fitness = get_average_fitness(monk_population)
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