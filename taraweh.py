from math import floor
from random import uniform, randint
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from time import sleep
import matplotlib.pyplot as plt
from math import sqrt


screen_width = 1000
screen_height = 600

rect_width = 25
rect_height = 50

# these are the variables that can be changed during  run time.

# this controls the probability that, when a follower blinks, the follower adjacent to it will blink as well. 
# if a follower has two adjancet followers, the process is seperate for each follower, each with a 50% percent chance.
follower_prob = 0.5

# this controls the probability that a follower will blink at the same time as the imam.
# Whether this probability hits or not for each square will be computed for each square once in the start_blink function.
imam_prob = 0.5

row_multiplier = 0.01

# number of consecutive rectangles that can be arranged horizontally
horizontal_rects = floor(screen_width/rect_width)
# number of consecutive rectanlges that can be arranged vertiaclly
vertically_rects = floor(screen_height/rect_height)
total_rects = horizontal_rects * (vertically_rects-1)

# Import and initialize the pygame library
pygame.init()

screen = pygame.display.set_mode([screen_width, screen_height])

class Imam():
    def __init__(self, x, y, blink, ID) -> None:
        self.x = x
        self.y = y
        self.blink = blink
        self.ID = ID
        self.red = 255
        self.green = 85
        self.blue = 85
        
class follower():
    def __init__(self,x_position, row, imam_prob, follower_prob,natural_blink, ID, done_blinking = False) -> None:
        self.x_position = x_position
        self.row = row
        # probability that follower will follow imam's blink
        self.imam_prob = imam_prob
        # probability that follower will stop their blinking early when another follower blinks
        self.follower_prob = follower_prob
        # the natural blink that a follower has. Does not change.
        self.natural_blink = natural_blink
        self.active_blink = natural_blink 
        self.ID = ID
        self.prompter = -1
        self.red = 255
        self.green = 85
        self.blue = 85
        self.done = done_blinking
        self.ImamProbability = 0
        self.adjacent_blink = False
        self.prompter = 0
        
    # used to update each follower's ImamProbability every new event, where the value is from the slider.
    def setImamProbability(self):
        self.ImamProbability = imam_prob - (row* row_multiplier)
        if self.ImamProbability < 0:
            self.ImamProbability = 0

            
            
 # used to create TwoDListOfProbability               
def get_follower(x_position, row, objects_list):
    for i in objects_list:
        if (i.x_position == x_position) &  (i.row == row):
            return i
   
 # used to make printing text on screen easier.
def print_text(text, x = 100, y = 100):
    font = pygame.font.Font('freesansbold.ttf', 14)
    # create a text surface object,
    # on which text is drawn on it.
    text1 = font.render((str(text)),True,"Black")
    
    # create a rectangular object for the
    # text surface object
    text_rect = text1.get_rect()
    text_rect.center = (x,y)
    screen.blit(text1,text_rect)
    


# will be used to create unique ID's for each Imam and follower. This will be used to for follower-to-follower interactions.
id_counter = 1
# creating Imam objects
NumOfImams = 5
ListOfImams = []
# finding x-coordinate, so that the center of the Imam is the center of the board.
rect_center = screen_width/2
x_adjusted = rect_center-(rect_width)
for i in range(NumOfImams):
    blink_length = round(uniform(1,5),3)
    temp_imam = Imam(x_adjusted,0,blink_length, id_counter)
    ListOfImams.append(temp_imam)
    id_counter += 1
    
# creating follower objects
ListOfFollowers = []
id_counter = 1
for row in range(2,vertically_rects+1):
    for Xposition in range(1,horizontal_rects+1):
        natural_blink = round(uniform(1,5),3)
        temp_follower = follower(Xposition,row,imam_prob,follower_prob,natural_blink, id_counter)
        ListOfFollowers.append(temp_follower)
        id_counter += 1

TwoDListOfFollowers = [] 
def update_Followers():
    #   a 2d list of follower objects 
    global TwoDListOfFollowers
    TwoDListOfFollowers = []
    for i in range(vertically_rects):
        TwoDListOfFollowers.append([])
        
    for row in range(vertically_rects):
        for x_position in range(horizontal_rects):
            temp_follower = get_follower(x_position + 1,row + 1, ListOfFollowers)
            TwoDListOfFollowers[row].append(temp_follower)
update_Followers()


# dictionary containing 1-1 translation from (row) to y values
RowToY = {}
for row in range(1,vertically_rects+2):
    RowToY[row] = rect_height*(row-1)
    
# dictionary containing 1-1 translation from (position) to x values
PosToX = {}
for pos in range(1,horizontal_rects+1):
    PosToX[pos] = rect_width * (pos-1)

# starts the blinking event
def start_blink(ActiveImam, prob = True):
    global same_counter; same_counter = 0
    global rects_stopped; rects_stopped = 0    
    global start_blinking; start_blinking = False    
    # gets start time of event
    start = pygame.time.get_ticks()
    # prob exists so that these are only called the first time start_blink is called every event.
    if  prob:
        for i in ListOfFollowers:
            # this sets a unique probability value for each row based on the Row multiplier variable
            i.setImamProbability()
            if randint(1,100) <= (i.ImamProbability * 100) :
                i.active_blink = ActiveImam.blink
    update_Followers()
    return start

def stop_blink(ActiveImam):
    global start_blinking
    global total_rects
    start_blinking = False
    # variable so that a new blinking event is set only when only all of the squares have turned red.
    turned_white = 0
    for i in ListOfFollowers:
        if ((i.red == 255) and (i.green == 85) and (i.blue == 85)):
            turned_white += 1
            i.done = False    
            i.adjacent_blink = False
            if turned_white == total_rects:
                get_groups()
                start_blinking = True 
        else:  
            # if counter is divisble by 10, add or subtract until the desired values are gotten.
            # this is done so that  a gradual transition of color is created rather than a singular flash.
            if counter % 10 == 0:
                if i.red >= 250:
                    i.red = 255
                else:
                    i.red += 3
                if i.green > 85:
                    i.green -= 1
                elif i.green < 85:
                    i.green += 1
                if i.blue > 85:
                    i.blue -= 1
                elif i.blue < 85:
                    i.blue += 1

                        
    # if the event blink is done, reset the imam (either randomize or choose).
    # reset the blink of the followers.
    doneList = []
    for i in ListOfFollowers:
        doneList.append(i.done)  
    if True in doneList:
        pass
    else:
        reset_imam(ActiveImam)
        for i in ListOfFollowers:
            i.active_blink = i.natural_blink

def blink(elapsed,imam):
    
    global rects_stopped
    
    for i in ListOfFollowers:
        # checks if the blink time has elapsed
        if elapsed >= i.active_blink:
            # in this case, the colors are still resetting in the stop_blink function
            if i.done:
                continue
            else:
                # adds one to the counter, and changes the color of the block if it was blinked naturally.
                rects_stopped += 1
                # if the probability of the imam hit, then the color is changed to green
                if i.adjacent_blink:
                    i.red, i.green, i.blue = 100,100,100
                elif i.active_blink == imam.blink:
                    i.red, i.green, i.blue = 20,100,20
                    i.prompter  =  imam.ID
                else:
                    i.red,i.green,i.blue = 0,0,0
                    i.prompter = i.ID
                i.done = True
                # this controls the adjacent blinkage.
                # row 1 is the one containing the imam.
                if i.row == 1:
                    continue
                else:
                    index_list = blink_adjacent(i)
                    # if the probability hits for either of the adjacent squares, blink them. but set the color to grey.
                    for j in index_list:
                        if randint(1,100) <= (follower_prob * 100):    
                            adjacent = TwoDListOfFollowers[i.row-1][(i.x_position-1) + j]
                            adjacent.active_blink = i.active_blink
                            if i.red == 0:
                                adjacent.prompter = i.ID
                            elif i.red == 100:
                                adjacent.prompter = i.prompter
                            elif i.red == 20:
                                adjacent.prompter = i.ID
                            
                            adjacent.adjacent_blink = True 
                            
def blink_adjacent(blinker):
    # finds out if active square(blinker) is a the first or last on the grid.
    index_add_list = []
    row_a = int(blinker.row - 1)
    x = int(blinker.x_position - 1)
    # making sure that there does a follower to ther right and that this follower has not blinked yet.
    if blinker.x_position != horizontal_rects:
        if TwoDListOfFollowers[row_a][x+1].done == False and TwoDListOfFollowers[row_a][x+1].active_blink != blinker.active_blink:
            index_add_list.append(1)
    #     # making sure that there does a follower to ther left and that this follower has not blinked yet.    
    if blinker.x_position != 1:
        if TwoDListOfFollowers[row_a][x-1].done == False and TwoDListOfFollowers[row_a][x-1].active_blink != blinker.active_blink:
            index_add_list.append(-1)
    return index_add_list 
    
    
# activates imam square.    
def activate_imam():
    global total_rects
    global ListOfFollowers
    global imam_prob
    global id_counter
    
    imam = ListOfImams[randint(0,4)]
    # since imam mode 1 makes the imam part of the followers list, the total_rects needs to be increased by one.
    if imam_mode == 1:
        imam_x = horizontal_rects/2
        total_rects += 1
        ImamAsFollower = follower(imam_x,1,1,0,imam.blink, imam.ID)
        ListOfFollowers.append(ImamAsFollower)
    elif imam_mode == 2:
        pass
    imam_start = pygame.time.get_ticks()
    return imam,imam_start

# resets the imam square.
def reset_imam(AI):
    global imam_mode
    # resets value total_rects and listOfFollowers.
    if imam_mode == 1:
        global total_rects; total_rects -= 1
        ListOfFollowers.pop()
    # setting color only for imam mode 2 
    if imam_mode == -2:
        AI.red, AI.green, AI.blue = 255,85,85
        imam_mode = 2
    
# setting default values.
imam_mode = 1
counter = 0
rects_stopped = 0
start_blinking = True
running = True

#  creates the sliders. Uses the pygame_widgets module.
x_multiplier = screen_width / 100
y_multiplier = screen_height / 50

def update_sliders():
    global slider_ImamProbability
    global output_ImamProbability
    # this slider controls the imam probability variable
    slider_ImamProbability = Slider(screen, int(x_multiplier * 1.5) , int(y_multiplier * 1.5), int(x_multiplier*7.5), int(y_multiplier * 2), min = 0, max = 1, step = 0.05)
    output_ImamProbability = TextBox(screen, 0, 0, int(x_multiplier * 3), int(y_multiplier * 1.5), fontSize = 15)
    
    global slider_RowMultiplier
    global output_RowMultiplier
    slider_RowMultiplier = Slider(screen, int(x_multiplier * 30), int(y_multiplier * 1.5), int(x_multiplier*7.5), int(y_multiplier * 2), min = 0, max = 0.1, step = 0.005)
    output_RowMultiplier = TextBox(screen, int(x_multiplier * 28), 0, int(x_multiplier * 3), int(y_multiplier * 1.5), fontSize = 15)
    
    # this slider controls the follower probability variable
    global slider_FollowerProbability
    global output_FollowerProbability
    #global output_right
    slider_FollowerProbability = Slider(screen, int(x_multiplier * 52), int(y_multiplier * 1.5), int(x_multiplier * 7.5), int(y_multiplier * 2), min = 0, max = 1, step = 0.05)
    output_FollowerProbability = TextBox(screen, int(x_multiplier * 50), 0, int(x_multiplier * 3.2), int(y_multiplier * 1.5), fontSize = 15)    
    
update_sliders()


BlinkGroups_list = []
GroupsSecondList = []
# will be used to find the number of Blink groups in each blinking event and graph them.
def get_groups():
    
    global BlinkGroups_list
    global GroupsSecondList
    global plot_switch
    
    done = []
    BlinkGroups = 0
    for i in ListOfFollowers:
        if i.prompter not in done:
            done.append(i.prompter)
            BlinkGroups += 1
        else:
            continue
    
    BlinkGroups_list.append(BlinkGroups)
    GroupsSecondList.append([imam_prob, (row_multiplier * follower_prob)])
    imam_prob_list = []
    for i in GroupsSecondList:
        imam_prob_list.append(i[0])
    rowfollower_list = []
    for i in GroupsSecondList:
        rowfollower_list.append(i[1])

    if plot_switch:
        plt.figure('Imam Probability')
        plt.ylabel('Num of Blink Groups')
        plt.xlabel('Imam Probability')
        plt.scatter(imam_prob_list, BlinkGroups_list, color = 'orange')
        plt.figure('Row Multiplier * Follower Probability')
        plt.ylabel('Num of Blink Groups')
        plt.xlabel('Row Multiplier * Follower Probability')
        plt.scatter(rowfollower_list, BlinkGroups_list, color = 'green')
        plt.ion()
        plt.show()
        
    
plot_switch = False
clicked = False


while running:
    # counter exists so that the color values are added every time the counter is divisble by a number x
    # this can be seen in the blink_reset function
    if counter == 1000:
        counter = 0    

    
    screen.fill((220,220,200))
    # if X is pressed, stop the program.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
  
    # drawing clickable circle that turns on or off plots.  
    pygame.draw.circle(screen, (0,0,0), (x_multiplier * 90, y_multiplier* 2.5), y_multiplier * 1.5)
    print_text("Click to Enable or Disable Plot", x_multiplier * 80, y_multiplier/2)
    mouse_x = pygame.mouse.get_pos()[0]
    mouse_y = pygame.mouse.get_pos()[1]
    distance_formula = int(sqrt((mouse_x- (90 * x_multiplier))**2 + (mouse_y - (2.5*y_multiplier))**2))
    print_text(plot_switch, x_multiplier * 95, y_multiplier*2)
    if distance_formula <= y_multiplier*1.5:
        if pygame.mouse.get_pressed()[0] and not clicked:
            clicked = True
            if plot_switch:
                plt.close()
                plt.close()
                plot_switch = False
            else:
                plot_switch = True
        if not pygame.mouse.get_pressed()[0]:
            clicked = False
    
    
    # print the follower, and maybe imam - depends on the imam_mode variable - squares. 
    for i in ListOfFollowers:
        x = PosToX[i.x_position]
        y = RowToY[i.row]
        pygame.draw.rect(screen,(i.red,i.green,i.blue),(x,y,rect_width-1,rect_height-2))
        
    # if blinking is done.
    if rects_stopped == total_rects:
        stop_blink(imam)
        pygame.display.update()
        counter += 1
        continue
    
    # If not in follower blinking event, start one. 
    if  start_blinking:
        imam,imam_start = activate_imam()
        start_time = start_blink(imam)
        
    # imam_mode 1 makes it so the imam is one of the followers so it does not need to be printed twiced
    if imam_mode != 1:
        pygame.draw.rect(screen,(imam.red,imam.green,imam.blue),(imam.x,imam.y,rect_width-1,rect_height-2)) 
    
    if imam_mode != 2:
        # elapsed time since start of event
        elapsed = (pygame.time.get_ticks() - start_time)/1000
        # checks to see if the elapsed time is greater or equal to than the time of each
        # follower's blinking time.
        blink(elapsed,imam)
    
    # checks if the time for blinking of the imam has passed
    elif imam_mode == 2:
        elapsed_imam = (pygame.time.get_ticks() - imam_start)/1000
        if elapsed_imam >= imam.blink:
            imam.red, imam.green, imam.blue = 0,0,0
            start_time = start_blink(imam, False)
            imam_mode = -2      
    
    # getting the probabilities from the sliders. Values are updated every frame, but only the start_blink function 
    # updates it so that the new values are used in computing the probabilities.
    events = pygame.event.get()
    NewImamProbability = round(slider_ImamProbability.getValue(),2)
    imam_prob = NewImamProbability
    
    NewFollowerProbability = round(slider_FollowerProbability.getValue(),2)
    follower_prob = NewFollowerProbability
    
    NewRowMultiplier = round(slider_RowMultiplier.getValue(),2)
    row_multiplier = NewRowMultiplier
    
    # draws the probabilities and the textbox.
    print_text("Imam Probability", int(x_multiplier * 9), int(y_multiplier/1.7))
    output_ImamProbability.setText(NewImamProbability)
    print_text("Follower Probability", int(x_multiplier * 38), int(y_multiplier/1.7))
    output_FollowerProbability.setText(NewFollowerProbability)
    print_text("Row Multiplier", int(x_multiplier * 58.5), int(y_multiplier/1.7))
    output_RowMultiplier.setText(NewRowMultiplier)
    pygame_widgets.update(events)

        
    pygame.display.update()


# Test codes. Unused

def sameImamPerRow(imam):
    same_counter_list = []
    for i in TwoDListOfFollowers:
        list_counter = 0
        for j in i:
            if j == None:
                continue
            if j.active_blink == imam.blink:
                list_counter += 1
        same_counter_list.append(list_counter)        
            
    
    for j in range(1,vertically_rects+1):
        follower_temp = TwoDListOfFollowers[j][10]
        x = PosToX[follower_temp.x_position]
        y = RowToY[follower_temp.row]
        print_text(same_counter_list[j], x, y+10)
