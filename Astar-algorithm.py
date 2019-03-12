import math

maze = [['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', '_', '_', '_', 'X', 'X', '_', 'X', '_', 'X'],
        ['X', '_', 'X', '_', '_', 'X', '_', '_', '_', 'X'],
        ['X', 'S', 'X', 'X', '_', '_', '_', 'X', '_', 'X'],
        ['X', '_', 'X', '_', '_', 'X', '_', '_', '_', 'X'],
        ['X', '_', '_', '_', 'X', 'X', '_', 'X', '_', 'X'],
        ['X', '_', 'X', '_', '_', 'X', '_', 'X', '_', 'X'],
        ['X', '_', '_', 'G', '_', 'X', '_', '_', '_', 'X'],
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']]

def ec_distance(p1,p2):
    distance = 0
    for i in range(len(p1)):
        distance += (p1[i] - p2[i])**2
    distance = math.sqrt(distance)
    return distance

def neighbors(coordinate,maze):
    l = len(maze)
    x = coordinate[0]
    y = coordinate[1]
    if x>=1 and y>=1 and y+1<l and x+1<l:
        return [[x-1,y],[x,y+1],[x+1,y],[x,y-1]]
    elif x == 0:
        if y == 0:
            return [[0,1],[1,0]]
        elif y == l-1:
            return [[0,y-1],[1,y]]
        else:
            return [[0,y-1],[1,y],[0,y+1]]
    elif y == 0:
        if x == l-1:
            return [[x,y+1],[x-1,y]]
    if y == l-1 and x == l-1:
        return [[x-1,y],[x,y-1]]
    
    
def aStar(maze,start,goal): #2-d array
    frontier = []
    frontier.append(start)  #coordinate
    path = [start]
    while frontier:
        current = frontier[0]
        
        if current == goal:
            break
        
        temp = neighbors(current,maze)
        l = []
        
        for next1 in temp:
            new_cost = ec_distance(next1,goal)
            if maze[next1[0]][next1[1]] != 'X':
                l.append(new_cost)
        min_l = min(l)
        
        for i in temp:
            if ec_distance(i,goal) == min_l:
                next_selection = i
        
        frontier[0] = next_selection
        path.append(next_selection)
        
    return path



print(aStar(maze,[3,1],[7,3]))
    
