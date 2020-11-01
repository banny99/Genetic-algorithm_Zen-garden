import random

class Monk:

    def __init__(self, garden, index):
        self.DNA = []
        self.num_of_raked_places = 0
        self.myPoz_x = None
        self.myPoz_y = None
        self.move_direction = None
        self.myGarden = garden
        self.starting_positions = []
        self.chosen_directions = []
        self.index = index


    def rake_garden(self):

        turn_index = 1
        while self.num_of_raked_places < self.myGarden.num_of_sand_places:

            # nahodny vyber startovacej pozicie hrabania
            max_num_of_starting_positions = self.myGarden.size_x-2 + self.myGarden.size_y-2 + len(self.myGarden.rocks)
            if len(self.starting_positions) <= max_num_of_starting_positions and len(self.myGarden.free_start_positions) > 0:
                start_poz = self.choose_beginning_poz()
            else:
                break

            # priradenie vybranych pozicii mnichovi +nasledne urcenie smeru pohybu
            self.myPoz_x = start_poz[0]
            self.myPoz_y = start_poz[1]
            self.set_initial_move_direction()

            # ak je vobec mozne z danej start. pozicie zacat hrabanie
            if self.is_possible_to_begin_raking():

                still_inside_the_garden = True
                # posuvanie hrabajuceho mnicha pokym sa mu nepodari dostat na okraj zahrady alebo sa v nej nezasekne
                while still_inside_the_garden and self.move_direction != 'x':
                    still_inside_the_garden = self.move(turn_index)

                # ak sa zasekol v zahradke a nevie sa pohnut
                if self.move_direction == 'x':
                    break
                # ak sa dostal na okraj
                else:
                    # odstran vychodnu poz z listu moznych zaciatkov
                    end_poz = (self.myPoz_x, self.myPoz_y)
                    self.myGarden.free_start_positions.remove(end_poz)
                    # navys index tahov
                    turn_index += 1


    def choose_beginning_poz(self):
        start_position = random.choice(self.myGarden.free_start_positions)
        self.myGarden.free_start_positions.remove(start_position)
        return start_position


    def set_initial_move_direction(self):
        if self.myPoz_x == 0:
            self.move_direction = 'r'
        elif self.myPoz_x == self.myGarden.size_x-1:
            self.move_direction = 'l'

        elif self.myPoz_y == 0:
            self.move_direction = 'd'
        elif self.myPoz_y == self.myGarden.size_y-1:
            self.move_direction = 'u'


    def is_possible_to_begin_raking(self):
        if self.move_direction == 'u':
            if self.myGarden.garden_grid[self.myPoz_y-1][self.myPoz_x] == 0:
                self.starting_positions.append((self.myPoz_x, self.myPoz_y))
                return True
            elif self.myGarden.garden_grid[self.myPoz_y-1][self.myPoz_x] == 'K':
                self.starting_positions.append((self.myPoz_x, self.myPoz_y))
                return False
            else:
                return False

        elif self.move_direction == 'd':
            if self.myGarden.garden_grid[self.myPoz_y+1][self.myPoz_x] == 0:
                self.starting_positions.append((self.myPoz_x, self.myPoz_y))
                return True
            elif self.myGarden.garden_grid[self.myPoz_y+1][self.myPoz_x] == 'K':
                self.starting_positions.append((self.myPoz_x, self.myPoz_y))
                return False
            else:
                return False

        elif self.move_direction == 'r':
            if self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x+1] == 0:
                self.starting_positions.append((self.myPoz_x, self.myPoz_y))
                return True
            elif self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x+1] == 'K':
                self.starting_positions.append((self.myPoz_x, self.myPoz_y))
                return False
            else:
                return False

        elif self.move_direction == 'l':
            if self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x-1] == 0:
                self.starting_positions.append((self.myPoz_x, self.myPoz_y))
                return True
            elif self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x-1] == 'K':
                self.starting_positions.append((self.myPoz_x, self.myPoz_y))
                return False
            else:
                return False

        else:
            return False


    def move(self, move_index):

        # right:
        if self.move_direction == 'r':
            garden_poz = self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x + 1]
            # ak sa moze posunut v jeho smere ->pohrabe a posuva sa
            if garden_poz == 0 or garden_poz == -1:
                self.rake_curr_place(move_index)
                self.myPoz_x += 1
                # ak je este vo vnutri zahrady
                if garden_poz == 0:
                    self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x] = 'M'
                    return True
                # ak sa uz posunul von
                elif garden_poz == -1:
                    return False
            else:
                self.choose_new_direction()
                return True

        # left:
        elif self.move_direction == 'l':
            garden_poz = self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x - 1]
            if garden_poz == 0 or garden_poz == -1:
                self.rake_curr_place(move_index)
                self.myPoz_x -= 1
                if garden_poz == 0:
                    self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x] = 'M'
                    return True
                elif garden_poz == -1:
                    return False
            else:
                self.choose_new_direction()
                return True

        # down:
        elif self.move_direction == 'd':
            garden_poz = self.myGarden.garden_grid[self.myPoz_y + 1][self.myPoz_x]
            if garden_poz == 0 or garden_poz == -1:
                self.rake_curr_place(move_index)
                self.myPoz_y += 1
                if garden_poz == 0:
                    self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x] = 'M'
                    return True
                elif garden_poz == -1:
                    return False
            else:
                self.choose_new_direction()
                return True

        # up:
        elif self.move_direction == 'u':
            garden_poz = self.myGarden.garden_grid[self.myPoz_y - 1][self.myPoz_x]
            if garden_poz == 0 or garden_poz == -1:
                self.rake_curr_place(move_index)
                self.myPoz_y -= 1
                if garden_poz == 0:
                    self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x] = 'M'
                    return True
                elif garden_poz == -1:
                    return False
            else:
                self.choose_new_direction()
                return True


    def rake_curr_place(self, move_index):
        if self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x] != -1:
            self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x] = move_index
            self.num_of_raked_places += 1


    def choose_new_direction(self):
        if self.is_NOT_possible_to_move() and self.is_NOT_possible_to_get_out():
            self.move_direction = 'x'

        else:
            if self.move_direction == 'r' or self.move_direction == 'l':
                d = self.myGarden.garden_grid[self.myPoz_y+1][self.myPoz_x]
                u = self.myGarden.garden_grid[self.myPoz_y-1][self.myPoz_x]
                # ak su mozne oba smery ->vyber nahodny z nich
                if (u == 0 or u == -1) and (d == 0 or d == -1):
                    self.move_direction = random.choice(['u', 'd'])
                else:
                    if u == 0 or u == -1:
                        self.move_direction = 'u'
                    elif d == 0 or d == -1:
                        self.move_direction = 'd'

            elif self.move_direction == 'u' or self.move_direction == 'd':
                r = self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x+1]
                l = self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x-1]
                if (r == 0 or r == -1) and (l == 0 or l == -1):
                    self.move_direction = random.choice(['l', 'r'])
                else:
                    if r == 0 or r == -1:
                        self.move_direction = 'r'
                    elif l == 0 or l == -1:
                        self.move_direction = 'l'

            self.chosen_directions.append(self.move_direction)


    def is_NOT_possible_to_get_out(self):
        # ak je niektory z nich v startovacich poziciach znamena to ze sa tade moze dostat von
        if (self.myPoz_x + 1, self.myPoz_y) in self.myGarden.free_start_positions or (self.myPoz_x - 1, self.myPoz_y) in self.myGarden.free_start_positions or (self.myPoz_x, self.myPoz_y + 1) in self.myGarden.free_start_positions or (self.myPoz_x, self.myPoz_y - 1) in self.myGarden.free_start_positions:
            return False
        else:
            return True


    def is_NOT_possible_to_move(self):
        if self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x + 1] == 0 or self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x - 1] == 0 or self.myGarden.garden_grid[self.myPoz_y + 1][self.myPoz_x] == 0 or self.myGarden.garden_grid[self.myPoz_y - 1][self.myPoz_x] == 0:
            return False
        else:
            return True


    def send_work_report(self):
        # self.myGarden.print_garden()
        print("\n-----\nMonk's num.", self.index, "work-report:")
        print(" -I raked ", self.num_of_raked_places, " places out of ", self.myGarden.num_of_sand_places, "places.")
        print(" -My starting positions: ", self.starting_positions)
        print(" -Decisions I made: ", self.chosen_directions)