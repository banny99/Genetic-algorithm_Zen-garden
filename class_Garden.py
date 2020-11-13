
class Garden:

    def __init__(self, size_x, size_y, rocks):
        self.size_x = size_x
        self.size_y = size_y
        self.rocks = rocks
        self.num_of_sand_places = (size_x-2) * (size_y-2) - len(rocks)
        self.garden_grid = []
        self.free_start_positions = []

        self.build_garden()
        self.set_free_start_positions()

    def build_garden(self):
        self.border_garden()
        if len(self.rocks) > 0:
            self.place_rocks()

    def border_garden(self):
        for y in range(self.size_y):
            self.garden_grid.append([])
            for x in range(self.size_x):
                if x == 0 or x == self.size_x-1 or y == 0 or y == self.size_y-1:
                    self.garden_grid[y].append(-1)
                else:
                    self.garden_grid[y].append(0)

    def place_rocks(self):
        for rock in self.rocks:
            self.garden_grid[rock[1]][rock[0]] = 'K'


    def set_free_start_positions(self):
        for x in range(1, self.size_x-1):
            self.free_start_positions.append((x, 0))
            self.free_start_positions.append((x, self.size_y-1))

        for y in range(1, self.size_y-1):
            self.free_start_positions.append((0, y))
            self.free_start_positions.append((self.size_x-1, y))


    def print_garden(self):
        for line in self.garden_grid:
            str_line = ''
            for place in line:
                str_line = str_line + str(place) + '\t'
            print(str_line)