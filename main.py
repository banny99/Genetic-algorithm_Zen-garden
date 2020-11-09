from utils import *
from class_Garden import Garden

''' 
-zmenit genom [x,y,l,p,p,l,p,p,l,...]
-strhavat fitness(ked skonci uprostred)
-"nova krv" (ak sa stuck-nu) 
-upravit:
    krizenie [-nahodne cislo randrange(1, len(genom))->podla toho cast z 1. a 2. rodica ]
    mutaciu [-nahodne cislo randrange(1, len(genom))->ten gen zmen na iny ]
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

# initialization #
original_garden = Garden(size_x, size_y, rocks)
size_of_population = random.randint(20, 50)
genome_size = size_x-2 + size_y-2 + rock_num
monk_population = []
whole_garden_raked = False
impossible_to_rake_garden = False


# 1st(-random) generation - garden raking:
num_of_generation = 0

# monk_population, whole_garden_raked = simulate_generation(monk_population, size_of_population, original_garden, num_of_generation)

# best_try = get_best_try(monk_population, num_of_generation, (monk_population[0], num_of_generation))

# # ak sa neda pohrabat ani jedno miesto:
# if best_try[0].num_of_raked_places == 0:
#     impossible_to_rake_garden = True

# Other generations - garden raking (till garden raked or 100th.gen):
while not whole_garden_raked and not impossible_to_rake_garden and num_of_generation < 100:
    num_of_generation += 1
    monk_population, whole_garden_raked = simulate_generation(monk_population, size_of_population, genome_size, original_garden, num_of_generation)

    # best_try = get_best_try(monk_population, num_of_generation, best_try)


# --- END--- #
# ak sa mu podarilo vsetko pohrabat:
if impossible_to_rake_garden:
    print("\nImpossible to rake garden")

elif whole_garden_raked:
    print("\n-num of generations passed: ", num_of_generation)
    print("FINITO - pohrabal som celu zahradu !!!")
    monk_population[-1].send_work_report()
    monk_population[-1].myGarden.print_garden()

else:
    print("\nUnable to rake whole garden")
    print("-num of generations passed (limit): ", num_of_generation)
    # print("Best try ->monk from generation n. -", best_try[1])
    # best_try[0].send_work_report()

    # best_monk = get_best_monk(monk_population)
    # best_monk.send_work_report()
    # best_monk.myGarden.print_garden()