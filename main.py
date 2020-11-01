from utils import *
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
rocks = load_rocks(garden_plan)


# 1st(-random) population - garden raking:
monk_population = []
for i in range(random.randint(20, 50)):
    garden = Garden(size_x, size_y, rocks)
    monk = Monk(garden, i)

    monk.rake_garden()
    # monk.send_work_report()
    if monk.num_of_raked_places == garden.num_of_sand_places:
        print("FINITO - pohrabal som celu zahradu !!!")
        monk.send_work_report()
        break

    monk_population.append(monk)

tournament1, tournament2 = tournament_selection(monk_population, random.randint(5, 10))
roulette1, roulette2 = roulette_selection(monk_population)

print("\n---\n ->Tournament_WINNERS:")
tournament1.send_work_report()
tournament2.send_work_report()

print("\n---\n ->Roulette-WINNERS:")
roulette1.send_work_report()
roulette2.send_work_report()