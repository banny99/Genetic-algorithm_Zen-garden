import random

class Monk:

    def __init__(self, garden, genes, index):
        self.myGarden = garden
        # geny (pri prvej populacii ->genes = []):
        self.DNA = genes
        self.DNA_index = 1
        self.index = index
        # fitness:
        self.num_of_raked_places = 0
        self.starting_positions = []
        self.myPoz_x = None
        self.myPoz_y = None
        self.move_direction = None
        self.chosen_directions = []


    def rake_garden(self):

        # max_num_of_starting_positions = self.myGarden.size_x - 2 + self.myGarden.size_y - 2 + len(self.myGarden.rocks)
        turn_index = 1

        while self.num_of_raked_places < self.myGarden.num_of_sand_places:

            # if len(self.myGarden.free_start_positions) > 0 and len(self.starting_positions) <= max_num_of_starting_positions:
            if len(self.myGarden.free_start_positions) > 0:
                start_poz = self.set_beginning_poz()
            else:
                break

            # priradenie vybranych pozicii mnichovi +nasledne urcenie smeru pohybu
            self.myPoz_x = start_poz[0]
            self.myPoz_y = start_poz[1]
            self.set_initial_move_direction()

            # ak je vobec mozne z danej start. pozicie zacat hrabanie
            if self.is_possible_to_rake():

                # number of raked places witihin one SUCCESFUL!!! raking line [norpwol = Number Of Raked Places Within One Line]
                norpwol = -1

                # posuvanie hrabajuceho mnicha pokym sa mu nepodari dostat na okraj zahrady alebo sa v nej nezasekne
                still_inside_the_garden = True
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

        start_position = self.DNA[0]

        if start_position not in self.myGarden.free_start_positions:
            start_position = random.choice(self.myGarden.free_start_positions)

        self.starting_positions.append(start_position)
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
            garden_poz = self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x + 1]
            # ak sa moze posunut v jeho smere ->pohrabe a posuva sa
            if garden_poz == 0 or garden_poz == -1:
                self.rake_curr_place(turn_index)
                norpwol += 1
                self.myPoz_x += 1
                # ak je este vo vnutri zahrady
                if garden_poz == 0:
                    self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x] = 'M'
                    return True, norpwol
                # ak sa uz posunul von
                elif garden_poz == -1:
                    return False, norpwol
            else:
                self.choose_new_direction2()
                return True, norpwol

        # left:
        elif self.move_direction == 'l':
            garden_poz = self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x - 1]
            if garden_poz == 0 or garden_poz == -1:
                self.rake_curr_place(turn_index)
                norpwol += 1
                self.myPoz_x -= 1
                if garden_poz == 0:
                    self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x] = 'M'
                    return True, norpwol
                elif garden_poz == -1:
                    return False, norpwol
            else:
                self.choose_new_direction2()
                return True, norpwol

        # down:
        elif self.move_direction == 'd':
            garden_poz = self.myGarden.garden_grid[self.myPoz_y + 1][self.myPoz_x]
            if garden_poz == 0 or garden_poz == -1:
                self.rake_curr_place(turn_index)
                norpwol += 1
                self.myPoz_y += 1
                if garden_poz == 0:
                    self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x] = 'M'
                    return True, norpwol
                elif garden_poz == -1:
                    return False, norpwol
            else:
                self.choose_new_direction2()
                return True, norpwol

        # up:
        elif self.move_direction == 'u':
            garden_poz = self.myGarden.garden_grid[self.myPoz_y - 1][self.myPoz_x]
            if garden_poz == 0 or garden_poz == -1:
                self.rake_curr_place(turn_index)
                norpwol += 1
                self.myPoz_y -= 1
                if garden_poz == 0:
                    self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x] = 'M'
                    return True, norpwol
                elif garden_poz == -1:
                    return False, norpwol
            else:
                self.choose_new_direction2()
                return True, norpwol


    def rake_curr_place(self, turn_index):
        if self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x] != -1:
            self.myGarden.garden_grid[self.myPoz_y][self.myPoz_x] = turn_index


    def choose_new_direction(self):
        # ak sa nemoze nikam pohnut:
        if self.is_NOT_possible_to_move():
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

    def choose_new_direction2(self):
        # ak sa nemoze nikam pohnut:
        if self.is_NOT_possible_to_move():
            self.move_direction = 'x'

        else:
            # vyber rozhodnutie z genomu mnicha
            turn_to = self.DNA[self.DNA_index]
            self.DNA_index += 1
            # ak je uz na konci ->bez od zaciatku
            if self.DNA_index == len(self.DNA):
                self.DNA_index = 1

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
                self.choose_new_direction2()


    # def is_NOT_possible_to_get_out(self):
    #     # ak je niektory z nich v startovacich poziciach znamena to ze sa tade moze dostat von
    #     if (self.myPoz_x + 1, self.myPoz_y) in self.myGarden.free_start_positions or (self.myPoz_x - 1, self.myPoz_y) in self.myGarden.free_start_positions or (self.myPoz_x, self.myPoz_y + 1) in self.myGarden.free_start_positions or (self.myPoz_x, self.myPoz_y - 1) in self.myGarden.free_start_positions:
    #         return False
    #     else:
    #         return True


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
        print("\n   Monk's num.", self.index, "work-report:")
        print(" -I raked ", self.num_of_raked_places, " places out of ", self.myGarden.num_of_sand_places, "places.")
        print(" -My starting positions: ", self.starting_positions)
        print(" -Decisions I made: ", self.chosen_directions)