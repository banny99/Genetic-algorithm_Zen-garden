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
    monk = Monk(garden, i+1)

    monk.rake_garden()
    monk.send_work_report()

    monk_population.append(monk)

best1, best2 = tournament_selection(monk_population, random.randint(5, 10))
best1.send_work_report()
best2.send_work_report()