import math
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np
from matplotlib import animation
from matplotlib.animation import FuncAnimation


#color defining
white = (255,255,255)
black = (0,0,0)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

scale = 1

# Dimensions of the maze specified in the question.
width= 300
height = 200


coord_polygon = np.array([(25 , 185 ),
                       (75 , 185 ),
                       (100 , 150 ),
                       (75 , 120 ),
                       (50 , 150 ),
                       (20 , 120 )], dtype='int')

coord_rectangle = np.array([(30 , 67.5 ),
                            (35 , 76 ),
                            (100 , 38.6),
                            (95 , 30 )], dtype='int')

coord_rhombus = np.array([(225, 40),
                            (250 , 25),
                            (225, 10),
                            (200, 25)], dtype='int')

coord_circle = [(25 ), (225, 150)]

coord_ellipse = [(80 , 40 ), (150, 100)]

# fig = plt.figure()
# fig.set_dpi(100)
# fig.set_size_inches(8.5,6)
# ax = plt.axes(xlim=(0,width),ylim=(0,height))
# circle = plt.Circle((coord_circle[1]),coord_circle[0],fc='green')
# rectangle = plt.Polygon(coord_rectangle,fc ='green')
# rhombus = plt.Polygon(coord_rhombus,fc='green')
# polygon = plt.Polygon(coord_polygon,fc='green')
# ellipse= Ellipse((coord_ellipse[1]),coord_ellipse[0][0],coord_ellipse[0][1],0,fc='green')
# obstacles = [circle,rectangle,rhombus,polygon,ellipse]

###################################################################################
###################     showPAth for animation    #################################
###################################################################################

def showPath(START_POINT, GOAL_POINT, STEP_OBJECT_LIST, pathValues):
    fig = plt.figure()
    fig.set_dpi(100)
    fig.set_size_inches(8.5, 6)

    axis = plt.axes(xlim=(0, 300), ylim=(0, 200))
    xTrace = []
    yTrace = []

    xTrack = []
    yTrack = []

    traced, = plt.plot([], [], 'o', color = 'yellow', markersize = 1)
    tracked, = plt.plot([], [], 'o', color = 'blue',  markersize = 1)

    def init():
        axis.set_xlim(0,300)
        axis.set_ylim(0,200)
        return traced, tracked,

    def animate(itr):
        if itr < len(STEP_OBJECT_LIST):
#             for eachNode in STEP_OBJECT_LIST:
            xTrace.append(STEP_OBJECT_LIST[itr][0])
            yTrace.append(STEP_OBJECT_LIST[itr][1])
            traced.set_data(xTrace,yTrace)

#             for trackNode in pathValues:
        if itr>=len(STEP_OBJECT_LIST):
            xTrack.append(pathValues[itr-len(STEP_OBJECT_LIST)][0])
            yTrack.append(pathValues[itr-len(STEP_OBJECT_LIST)][1])
            tracked.set_data(xTrack,yTrack)

        return traced, tracked,

    anim = FuncAnimation(fig, animate, frames = len(STEP_OBJECT_LIST)+len(pathValues), init_func = init, interval = 1, blit = False, repeat = False)
    circle = plt.Circle((coord_circle[1]),coord_circle[0],fc='green')
    rectangle = plt.Polygon(coord_rectangle,fc ='green')
    rhombus = plt.Polygon(coord_rhombus,fc='green')
    polygon = plt.Polygon(coord_polygon,fc='green')
    ellipse= Ellipse((coord_ellipse[1]),coord_ellipse[0][0],coord_ellipse[0][1],0,fc='green')
    obstacles = [circle,rectangle,rhombus,polygon,ellipse]
    goalLoc = plt.scatter(GOAL_POINT[0], GOAL_POINT[1], s = 10, color = 'red')
    startLoc = plt.scatter(START_POINT[0], START_POINT[1], s = 10, color = 'red')
    for item in obstacles:
        plt.gca().add_patch(item)
    plt.show()

###################################################################################
#############################   Rounding Off  #####################################
###################################################################################

#round off function
def rounding_off(coord):
    x = str(float(coord))
    
    res_x = x.index('.')
    val_x = int(x[res_x +1])
    
    if val_x<=2:
        return float(math.floor(coord))
    elif 2<val_x<=7:
        return math.floor(coord)+0.5
    else :
        return float(math.ceil(coord))


###################################################################################
#######################    distance calculation   #################################
###################################################################################

#distance calculation
def distance(one,two):
    '''Calculate straight line distance between two points'''
    x1,y1 = one,two
    x2,y2 = goal[0],goal[1]
    return (math.sqrt((x1-x2)**2+(y1-y2)**2))*2.5

###################################################################################
###########   obstacle_space & checking if inside obstacle space   ################
###################################################################################

def obstacle_space(x,y,r):
    c=0
    if ((x-math.ceil(225))**2+math.ceil(y-(150))**2-math.ceil(25+r)**2)<0:#circle
        c=1
    if (y - 1.4*x - (80+r) <= 0) and (y + 1.4*x  - (290+r) <= 0) and (y - 1.2*x - (30+r) >= 0) and (y + 1.2*x -(210+r) >= 0):#rhombus
        c=1
    if (y - (185+r) <= 0) and (y - 13*x + (140-r) <= 0) and (y - x - (100+r) >= 0) and (y - 1.4*x - (80+r) >= 0):#triangle
        c=1
    if (y + 0.6*x - (145+r) >= 0) and (y- 0.6*x + (95-r) <= 0) and (y+ 0.6*x - (175+r) <= 0) and (y- 0.6*x + (125+r) >= 0):#rhombus
        c=1
    if (y- (3**(1/2))*x + (134.54482+2*r) >= 0) and (y - (3**(1/2))*x - (15.455173+2*r) <= 0) and (y + (1/(3**(1/2)))*x - (84.84827-(r)) >= 0) and (y + (1/(3**(1/2)))*x - (96.39528096+(r)) <= 0):
        c=1   
    if ((x-math.ceil(150))/math.ceil(40+r))**2 + ((y - math.ceil(100))/math.ceil(20+r))**2 - 1 <0:#ellipse
        c=1
    return c

#find if point is in obstacle or not
def Is_obstacle(x,y,clearance):
    if obstacle_space(x,y,clearance) == 1:
        return 1
    else:
        return 0

###################################################################################
#################################    goal_space     ###############################
#####################################  is_goal  ###################################
def goal_space(a,b):
    g=0
    if ((goal[0]-math.ceil(a))**2+math.ceil(goal[1]-(b))**2-math.ceil(1.5)**2)<0:#circle
        g=1
    return g


def Is_goal(x,y):
    if goal_space(x,y) == 1:
        return 1
    else:
        return 0

###################################################################################
##########################  to_come_cost  #########################################
############################ to_go_cost ###########################################

def heuristic(coming_cost, going_cost):
    return coming_cost+going_cost
    
###################################################################################
#################################### Angles #######################################
###################################################################################

def angles(prev_theta,new_theta):
    theta = prev_theta + new_theta
    if theta < 0:
        theta = 360 + theta
    elif theta > 360:
        theta = theta % 360        
    return theta

###################################################################################
##########################    next 5 coordinates    ###############################
###################################################################################

#step:1 all angles (5 next coordinates)
def new_points(x,y,z,come_cost):
    for i in [0, 30, 60, -30, -60]:
        theta = angles(z,i)
        x_6 = x + math.cos(math.radians(theta))
        y_6 = y + math.sin(math.radians(theta))
        #print(x_6, y_6)
        #print(x_6, y_6, i)
        if (x_6 >=0 and x_6 <=300) and (y_6 >=0 and y_6 <=200):
            if Is_obstacle(x_6,y_6,tot_rad)==0:
                x_6 = rounding_off(x_6)
                y_6 = rounding_off(y_6)
                if [x_6,y_6,theta] not in visited:
                    cost_2_go = distance(x_6,y_6)
                    heuristic_fn = heuristic(come_cost , cost_2_go)
                    frontier_list.append([x_6,y_6, theta, come_cost+1 ,heuristic_fn])
                    visited.append([x_6,y_6, theta])
                    explored.append([x_6, y_6])
                    parent[(x_6,y_6,theta)]= (x,y,z)
                    if Is_goal(x_6,y_6)==1:
                        return 1
    return 0

###################################################################################
#############   main()-getting input and running functions    #####################
###################################################################################

#getting input
x, y, z = [int(x) for x in input("Enter three values(start point with angle): ").split()]
a,b = [int(x) for x in input("Enter two values(goal point): ").split()]
rad,clear = [int(x) for x in input("Enter the radius and clearance(two values): ").split()]
tot_rad = rad + clear
start = [x,y,z] 
start_1=[x,y]
goal = [a,b]

current = [x,y,z,0]
frontier_list = []
visited = [start]
explored = [[start[0], start[1]]]
parent = {}
while True:
    if new_points(current[0],current[1],current[2],current[3]) == 0: 
        frontier_list = sorted(frontier_list,key = lambda x: x[4])
        #print(frontier_list)
        current = frontier_list.pop(0)
        #print("current", current)
        #print(explored)
    else:
        current = frontier_list.pop(-1)
        break
        
curr = (current[0],current[1], current[2])
l1 = [curr]

while(l1[-1] != (start[0], start[1], start[2])):
    l1.append(parent[curr])
    curr = l1[-1]

l1.reverse()
bt = [[x[0],x[1]] for x in l1]

#To see a faster but static output please uncomment the following commented section and comment the last line
#This gives you the backtracking of final path (x,y,theta) and the final output
# Also comment the function showpath (line 60 to 106) and uncomment from line - 45 to 54 and the program
# for j in explored:
#     plt.plot(j[0],j[1],'bo',markersize = 1)
#     print(j)
    
# for i in l1:
#     plt.plot(i[0],i[1],'ro',markersize = 1)
#     print(i)
# for obstacle in obstacles:
#     plt.gca().add_patch(obstacle)
#     plt.show()

showPath(start,goal,explored,bt)