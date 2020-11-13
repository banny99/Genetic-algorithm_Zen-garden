import random

class Monk:

    def __init__(self, garden, genes, index):
        self.myGarden = garden
        self.DNA = genes
        self.index = index
        self.num_of_raked_places = 0
        self.starting_positions = []
        self.myPoz_x = None
        self.myPoz_y = None
        self.move_direction = None
        self.chosen_directions = []


    def rake_garden(self):

        turn_index = 1
        # Turn:
        while self.num_of_raked_places < self.myGarden.num_of_sand_places:

            if len(self.myGarden.free_start_positions) > 0:
                self.set_beginning_poz()
            else:
                break

            # ak je vobec mozne z danej start. pozicie zacat hrabanie
            if self.is_possible_to_rake():

                # number of raked places witihin one SUCCESFUL!!! raking line [norpwol = Number Of Raked Places Within One Line]
                norpwol = -1
                # posuvanie hrabajuceho mnicha pokym sa mu nepodari dostat na okraj zahrady alebo sa v nej nezasekne
                still_inside_the_garden = True

                # Move:
                while still_inside_the_garden and self.move_direction != 'x':
                    still_inside_the_garden, norpwol = self.move(turn_index, norpwol)

                # ak sa zasekol v zahradke a nevie sa pohnut (=neuspesny tah ->koniec)
                if self.move_direction == 'x':
                    break
                # ak sa dostal na okraj (=uspesny tah)
                else:
                    # odstran vychodnu poz z listu moznych zaciatkov
                    end_poz = (self.myPoz_x, self.myPoz_y)
                    self.myGarden.free_start_positions.remove(end_poz)
                    # pripocitaj pocet pohrabanych policok v tomto (uspesnom) tahu k celkovemu poctu pohrabanych policok
                    self.num_of_raked_places += norpwol
                    # navys index tahov
                    turn_index += 1



    def set_beginning_poz(self):

        if self.DNA[0][0] >= len(self.DNA[0]):
            start_position = random.choice(self.myGarden.free_start_positions)

        else:
            start_poz_index = self.DNA[0][0]
            start_position = self.DNA[0][start_poz_index]
            self.DNA[0][0] += 1

            while start_position not in self.myGarden.free_start_positions:
                if self.DNA[0][0] >= len(self.DNA[0]):
                    start_position = random.choice(self.myGarden.free_start_positions)
                    break
                start_poz_index = self.DNA[0][0]
                start_position = self.DNA[0][start_poz_index]
                self.DNA[0][0] += 1

        self.myPoz_x = start_position[0]
        self.myPoz_y = start_position[1]
        self.set_initial_move_direction()

        self.starting_positions.append(start_position)
        self.myGarden.free_start_positions.remove(start_position)


    def set_initial_move_direction(self):
        if self.myPoz_x == 0:
            self.move_direction = 'r'
        elif self.myPoz_x == self.myGarden.size_x-1:
            self.move_direction = 'l'

        elif self.myPoz_y == 0:
            self.move_direction = 'd'
        elif self.myPoz_y == self.myGarden.size_y-1:
            self.move_direction = 'u'


    def is_possible_to_rake(self):
        if self.move_direction == 'u':
            poz_to_check = self.myGarden.garden_grid[self.myPoz_y-1][self.myPoz_x]

        elif self.move_direction == 'd':
            poz_to_check = self.myGarden.garden_grid[self.myPoz_y+1][self.myPoz_x]

        elif self.move_direction == 'r':
            poz_to_check = self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x+1]

        elif self.move_direction == 'l':
            poz_to_check = self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x-1]


        if poz_to_check == 0 or poz_to_check == -1:
            return True
        else:
            return False


    def move(self, turn_index, norpwol):
        # right:
        if self.move_direction == 'r':
            next_poz = self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x + 1]
        # left:
        elif self.move_direction == 'l':
            next_poz = self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x - 1]
        # down:
        elif self.move_direction == 'd':
            next_poz = self.myGarden.garden_grid[self.myPoz_y + 1][self.myPoz_x]
        # up:
        elif self.move_direction == 'u':
            next_poz = self.myGarden.garden_grid[self.myPoz_y - 1][self.myPoz_x]


        still_inside_the_garden, norpwol = self.rake_curr_place(next_poz, turn_index, norpwol)
        return still_inside_the_garden, norpwol



    def rake_curr_place(self, next_poz, turn_index, norpwol):
        curr_poz = self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x]

        # ak sa da v mojom smere pokracovat
        if next_poz == 0:
            # a ak nestojim na okraji ->prepis index tahu
            if curr_poz != -1:
                self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x] = turn_index
            # posun v smere:
            self.shift_me_in_my_direction()
            # a oznac moju akt. poz na mape:
            self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x] = 'M'
            norpwol += 1
            return True, norpwol

        # ak sa uz posunul von
        elif next_poz == -1:
            if curr_poz != -1:
                self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x] = turn_index
            self.shift_me_in_my_direction()
            norpwol += 1
            return False, norpwol

        # ak sa neda v mojom smere pokracovat (-prekazka):
        else:
            recursion_check = 1
            self.choose_new_direction2(recursion_check)
            return True, norpwol


    def shift_me_in_my_direction(self):
        # right:
        if self.move_direction == 'r':
            self.myPoz_x = self.myPoz_x + 1
        # left:
        elif self.move_direction == 'l':
            self.myPoz_x = self.myPoz_x - 1
        # down:
        elif self.move_direction == 'd':
            self.myPoz_y = self.myPoz_y + 1
        # up:
        elif self.move_direction == 'u':
            self.myPoz_y = self.myPoz_y - 1


    def choose_new_direction2(self, recursion_check):
        # ak sa nemoze nikam pohnut:
        if self.is_NOT_possible_to_move() or recursion_check >= len(self.DNA[1]):
            self.move_direction = 'x'

        else:
            # vyber rozhodnutie z genomu mnicha
            turn_index = self.DNA[1][0]
            turn_to = self.DNA[1][turn_index]
            self.DNA[1][0] += 1
            # ak je uz na konci ->bez od zaciatku
            if self.DNA[1][0] >= len(self.DNA[1]):
                self.DNA[1][0] = 1

            old_direction = self.move_direction
            # ak sa otaca do lava:
            if turn_to == 'l':
                if self.move_direction == 'r':
                    self.move_direction = 'u'
                elif self.move_direction == 'l':
                    self.move_direction = 'd'
                elif self.move_direction == 'u':
                    self.move_direction = 'l'
                elif self.move_direction == 'd':
                    self.move_direction = 'r'

            # ak sa otaca do prava:
            elif turn_to == 'r':
                if self.move_direction == 'r':
                    self.move_direction = 'd'
                elif self.move_direction == 'l':
                    self.move_direction = 'u'
                elif self.move_direction == 'u':
                    self.move_direction = 'r'
                elif self.move_direction == 'd':
                    self.move_direction = 'l'

            # ak nie je mozne v tomto smere pokracovat v hrabani nezmen:
            if not self.is_possible_to_rake():
                self.move_direction = old_direction
                recursion_check += 1
                self.choose_new_direction2(recursion_check)

            self.chosen_directions.append(self.move_direction)
            return recursion_check


    def is_NOT_possible_to_move(self):
        poz_r = self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x + 1]
        poz_l = self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x - 1]
        poz_d = self.myGarden.garden_grid[self.myPoz_y + 1][self.myPoz_x]
        poz_u = self.myGarden.garden_grid[self.myPoz_y - 1][self.myPoz_x]

        if (self.move_direction == 'u' or self.move_direction == 'd') and (poz_r == 0 or poz_r == -1 or poz_l == 0 or poz_l == -1):
            return False

        elif (self.move_direction == 'l' or self.move_direction == 'r') and (poz_u == 0 or poz_u == -1 or poz_d == 0 or poz_d == -1):
            return False

        else:
            return True


    def send_work_report(self):
        # self.myGarden.print_garden()
        print("   Monk's num.", self.index, "work-report:")
        print(" -I raked ", self.num_of_raked_places, " places out of ", self.myGarden.num_of_sand_places, "places.")
        print(" -My starting positions: ", self.starting_positions)
        print(" -Decisions I made: ", self.chosen_directions, '\n')