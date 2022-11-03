
from random import randint as rand
import pygame
import time


row_max =16
column_max =16
mine_count = 50

square_list = []
square_size = 30
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)
pygame.init()
stage = "setup"
check_list = []

screen = pygame.display.set_mode((square_size*column_max, square_size*row_max)) 
pygame.display.set_caption("Minesweeper")

class square:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.mine = False
        self.hidden = True
        self.flag = False
        self.mark_mine = False
        self.mark_safe = False
        

    def adjacents(self, choice):
        adjacent_list = []
        empty_list = []
        for row_difference in range(-1,2):
            new_row = self.row + row_difference
            for column_difference in range(-1,2):
                new_column = self.column + column_difference
                if (0 <= new_column < column_max) and (0 <= new_row < row_max) and not (column_difference == 0 and row_difference == 0):           
                    adjacent_list.append([self.row+row_difference, self.column + column_difference])
        output_list = []
        for item in adjacent_list:
            thing = square_list[item[0]][item[1]]
            output_list.append(thing)
            if thing.hidden and not thing.flag:
                empty_list.append(thing)

        if choice == 0:
            return output_list
        else:
            return empty_list


                

    def adjacent_mines(self, type):
        num_mines = 0
        num_safe = 0
        num_hidden = 0
        num_flag = 0
        num_blank = 0
        for item in self.adjacents(0):
            if item.mine:
                num_mines += 1
            else:
                num_safe +=1
            if item.hidden:
                num_hidden +=1
                if item.flag:
                    num_flag +=1
                else:
                    num_blank += 1

        if type == 'm':
            return num_mines
        elif type == 's':
            return num_safe 
        elif type == "h":
            return num_hidden
        elif type == "f":
            return num_flag
        elif type == "b":
            return num_blank
    
    def draw_me(self):
        if self.hidden:
            colour = WHITE
            text_colour = BLACK
            text = "F"
        else:
            colour = BLACK
            text_colour = WHITE
            text = str(self.adjacent_mines("m"))
        pygame.draw.rect(screen, colour, (self.column*square_size, self.row*square_size, square_size, square_size))
        if ((not self.hidden) or self.flag) and text != "0":
            font = pygame.font.SysFont(None, square_size)
            screen.blit(font.render(text, True, text_colour), (self.column *square_size + square_size/3, self.row*square_size + square_size/3))

    def reveal(self):
        global reveal_count
        global stage
        global win
        global check_list
        if self.hidden:
            reveal_count += 1
            self.flag = False
            if self.mine:
                stage = "end"
                win = False
                print(self.row, self.column)
   
            else:
                self.hidden = False
                check_win()

        if self.adjacent_mines("m") == 0:
            for item in self.adjacents(0):
                if item.hidden:
                    item.reveal()
            
        if self.adjacent_mines("b") > 0:
            check_list.append(self)


    def autocomplete(self):
        worked = False
        if (not self.hidden) and self.adjacent_mines("b") > 0:

            if self.adjacent_mines("b") == self.adjacent_mines("m")-self.adjacent_mines("f"):

                worked = True
                for item in self.adjacents(1):
                    item.flag = True
    

            elif self.adjacent_mines("m") == self.adjacent_mines("f"):
  
                worked = True
                for item in self.adjacents(1):                                   
                    item.reveal()

        return worked

for row in range(row_max):
    square_list.append([])
    for column in range(column_max):
        square_object = square(row, column)
        square_list[row].append(square_object)



def setup(chosen_row, chosen_column):
    global reveal_count
    square_list[chosen_row][chosen_column].hidden = False
    reveal_count = 1
    for item in square_list[chosen_row][chosen_column].adjacents(0):
        item.hidden = False
        reveal_count += 1
    for _ in range(mine_count):
        valid = False
        while not valid:
            valid = True
            random_column = rand(0, column_max-1)
            random_row = rand(0, row_max -1)
            if square_list[random_row][random_column].mine or (not square_list[random_row][random_column].hidden):
                valid = False
            else:
                square_list[random_row][random_column].mine = True
                for item in square_list[random_row][random_column].adjacents(0):
                    if item.adjacent_mines('s') == 0:
                        valid = False
                        square_list[random_row][random_column].mine = False
                        break
    for row in square_list:
        for item in row:
            if not item.hidden:
                item.reveal()
    



def draw_grid():
    for i in range(row_max + 1):
        pygame.draw.line(screen, BLUE, (0, i*square_size), (column_max*square_size, i*square_size))
    for i in range(column_max + 1):
        pygame.draw.line(screen, BLUE, (i*square_size, 0), (i*square_size, row_max*square_size))

def draw_board():
    for row in square_list:
        for item in row:
            item.draw_me()
    draw_grid()


def list_possibilities(num_things, num_spaces):
    if num_things > num_spaces:
        return([])
    elif num_things == 0:
        string = ""
        for _ in range(num_spaces):
            string += "0"
        return([string])
    else:
        output_list = []
        position_list = []
        for _ in range(num_things):
            position_list.append("")

        def recursive(ordinal, smaller):
            nonlocal output_list
            nonlocal position_list
            
            for current in range(smaller+1, num_spaces -ordinal ):
                position_list[ordinal] = current

                if ordinal == 0:
                    placeholder = []
                    for item in position_list:
                        placeholder.append(item)

                    output_list.append(placeholder)
                else:
                    recursive(ordinal - 1, current)
        recursive(num_things-1, -1)
        return output_list


def wait():
    draw_board()
    pygame.display.update()

def brute(working):
    global check_list
    for square in check_list:
        print(square.row, square.column)
    wait()
    if working:
        print("going")
        working = False
        count = 0
        for i in range(len(check_list)):
            if stage == "play":
                item = check_list[count]
                if item.adjacent_mines("b") > 0:
                    attempt = item.autocomplete()
                    pygame.event.get()

                    if attempt:
                        working = True
                        del check_list[count]
                        wait()
                        check_win()
                    else:
                        count += 1
                else:
                    del check_list[count]
    
            else:
                break
 
    
    else:
        print("stuck")
        wait()
        stuck_v2()
        # thread = threading.Thread(stuck())
        # thread.start()
        # thread.join()

        working = True
        check_win()
    return working



def check_board():
    valid = True
    for row in square_list:
        for item in row:
            if (not item.hidden) and item.adjacent_mines("m") > 0:
                suspicious_count = 0
                for adjacent in item.adjacents(0):
                    if adjacent.flag or adjacent.mark_mine:
                        suspicious_count += 1
                if suspicious_count != item.adjacent_mines("m"):
                    valid = False
                    break
    return valid

def check_win():
    global win
    global stage
    if reveal_count == row_max*column_max - mine_count:
        stage = "end"
        win = True

timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, 1)

def game(option):
    global screen
    global stage
    global win
    global check_list
    win = False
    done = False

    screen.fill(WHITE)
    draw_grid()
    autocomplete_working = True
    stage_done = True

    

    while not done:  

        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                done = True  

            if stage == "setup":
                if option == "c":
                    setup(rand(0, row_max-1), rand(0,column_max-1))
                    stage = "play"
                    draw_board()
                    for row in square_list:
                        for square in row:
                            if not square.hidden and square.adjacent_mines("b") > 0:
                                check_list.append(square)
                    wait()
                    time.sleep(1.5)
                if  event.type == pygame.MOUSEBUTTONDOWN and option == "p":
                    mouse_row = pygame.mouse.get_pos()[1]//square_size
                    mouse_column = pygame.mouse.get_pos()[0]//square_size
                    setup(mouse_row, mouse_column)
                    stage = "play"
                    draw_board()
                



            elif stage == "play":          
                if event.type == pygame.MOUSEBUTTONDOWN and option == "p":
                    mouse_row = pygame.mouse.get_pos()[1]//square_size
                    mouse_column = pygame.mouse.get_pos()[0]//square_size
                    button = event.button
                    if button == 1:
                        if square_list[mouse_row][mouse_column].hidden:
                            square_list[mouse_row][mouse_column].reveal()
                        else:
                            _ = square_list[mouse_row][mouse_column].autocomplete()
                        print(square_possibilities(square_list[mouse_row][mouse_column]))


                        check_win()
                        draw_board()
                    #Left click

                    elif button == 3:
                    #Right click
                        square_list[mouse_row][mouse_column].flag = not square_list[mouse_row][mouse_column].flag
                        draw_board()
                        print(square_possibilities(square_list[mouse_row][mouse_column]))
                 
               
                elif option == "c" and event.type == timer_event:
                    autocomplete_working = brute(autocomplete_working)
                 




      
            elif stage == "end":
                
                if stage_done == True:

                    if win == False:
                        print("lose")
                        # for row in square_list:
                        #     for square in row:
                        #         if square.flag:
                        #             print(square.row, square.column, "flag")
                            
                    else:
                        print("win")
                        if option == "c":
                            for row in square_list:
                                for item in row:
                                    if not item.flag and item.hidden:
                                        item.flag = True
                            wait()
                    stage_done = False
                # # if event.type == pygame.MOUSEBUTTONDOWN:
                # #     done = True 
                # # else:
                # if win:
                #     text = "You Win!"
                # else:
                #     text = "You Lose!"
                # screen.fill(BLACK)
                # font = pygame.font.SysFont(None, square_size)
                # screen.blit(font.render(text, True, WHITE), (square_size*column_max/3, square_size*row_max/3))
                
        pygame.display.update()


def square_possibilities(square):
    spaces = square.adjacent_mines("b")

    temp_list = list_possibilities(square.adjacent_mines("m") - square.adjacent_mines("f"), spaces)
    output_list = []
    for item in temp_list:
        binary_string = ''
        for i in range(spaces):
            if i in item:
                binary_string += "1"
            else:
                binary_string += "0"
        
        output_list.append(binary_string)
    return output_list

def convert_overlap(indexes, string):
    new_bin = ""
    for index in indexes:
        new_bin += string[index]  
    return new_bin  
#reduce string to just overlaps

def make_new_bin(overlap_indexes, possibilities):   
    output_list = []
    for bin in possibilities:
        new_bin = convert_overlap(overlap_indexes, bin)
        if new_bin not in output_list:
            output_list.append(new_bin)      
    return output_list
#make new list of just overlap possibilities
def check_in_list(possibility_list, indexes, overlap_possibilities):
    count = 0
    for i in range(len(possibility_list)):
        if convert_overlap(indexes, possibility_list[count]) not in overlap_possibilities:
            possibility_list.pop(count)
        else:
            count += 1
    return possibility_list
#Cull board_possibilities to possible lists

def stuck_v2():  
    global check_list
    num_flags = 0
    for row in square_list:
        for item in row:
            if item.flag:
                num_flags += 1
    
    board_possibilities = square_possibilities(check_list[0])
    # for item in check_list:
    #     print(item.row, item.column, item.hidden)
    keys = check_list[0].adjacents(1)
    for key in keys:
        print(key.row, key.column, "key")
    # for key in keys:
    #     print("keys", key.row, key.column)
    big_success = False
    for k in range(1,len(check_list)):
        for key in keys:
            print(key.row, key.column, "key")
    

        item = check_list[k]
        # print(item, item.row, item.column)
        big_overlap_indexes = []
        small_overlap_indexes = []
        item_adjacents = item.adjacents(1)
        # for adjacent in item_adjacents:
        #     # print("adjacents",adjacent.row, adjacent.column )
        
        item_possibilities = square_possibilities(item)
        print(item_possibilities, item.row, item.column)
        for i in range(len(keys)):
            for k in range(len(item_adjacents)):
                if keys[i] == item_adjacents[k]:
                    big_overlap_indexes.append(i)
                    small_overlap_indexes.append(k)
#Finds which squares overlap
        
        big_overlap_possibilities = make_new_bin(big_overlap_indexes, board_possibilities)
        print(big_overlap_possibilities, "big overlap possibilities")
        small_overlap_possibilities = make_new_bin(small_overlap_indexes, item_possibilities)
        print(small_overlap_possibilities, "small """)

        overlap_possibilities = small_overlap_possibilities
        for bin in overlap_possibilities:
            if bin not in big_overlap_possibilities:
                overlap_possibilities.remove(bin)

        board_possibilities = check_in_list(board_possibilities, big_overlap_indexes, overlap_possibilities)
        item_possibilities = check_in_list(item_possibilities, small_overlap_indexes, overlap_possibilities)
        pygame.event.get()
        stripped_item_possibilities = []

        for bin in item_possibilities:
            new_bin = ""
            for i in range(len(bin)):
                if i not in small_overlap_indexes:
                    new_bin += bin[i]
            if new_bin not in stripped_item_possibilities:
                stripped_item_possibilities.append(new_bin)
        stripped_item_keys = []
        pygame.event.get()
        for i in range(len(item_adjacents)):
            if i not in small_overlap_indexes:
                stripped_item_keys.append(item_adjacents[i])
        new_board_possibilities = []
        for bin in board_possibilities:
            for item_bin in stripped_item_possibilities:
                potential_mines = 0
                new_bin = bin + item_bin
                check_bin = item_bin

                for i in range(len(big_overlap_indexes)):
                    check_bin = check_bin[:small_overlap_indexes[i]] + bin[big_overlap_indexes[i]] + check_bin[small_overlap_indexes[i]:]
                if check_bin in item_possibilities:
                    for character in new_bin:
                        if character == "1":
                            potential_mines += 1
                    if num_flags + potential_mines <= mine_count:
                        new_board_possibilities.append(new_bin)
                    #Check if there will be too many mines on the board
                
        
    
        # print(board_possibilities)
        # print(big_overlap_indexes)
        # print(item_possibilities)
        # print(small_overlap_indexes)
        board_possibilities = new_board_possibilities
        # print(new_board_possibilities)
        keys += stripped_item_keys 
        # for key in keys:
        #     print("keys", key.row, key.column)
        pygame.event.get()

        print(board_possibilities)
        for i in range(len(board_possibilities[0])):
            small_success = True
            number = board_possibilities[0][i]
            for q in range(1, len(board_possibilities)):       
                if number != board_possibilities[q][i]:
                    small_success = False
                    break

            if small_success:
                big_success = True
                print("big_success")

                if number == "0":
                    keys[i].reveal()

                elif number == "1":
                    keys[i].flag = True
                wait()
        if big_success:
            for key in keys:
                print(key.row, key.column, "key")
            break  

    if not big_success:
        random_num = rand(0, len(keys)-1)
        keys[random_num].reveal()
        print(keys[random_num].row, keys[random_num].column, "random selection")
        wait()
        print("random")



game("c")



            


        
            





        
        


    
            


    
    
    

    

                    
            
    
    



        








            
        
