import heapq as pq
from random import random

class pathfinding:
    def __init__(self, filename_a="pathfinding_a.txt", filename_b="pathfinding_b.txt"):
        self.filename_a = filename_a
        self.filename_b = filename_b
        self.grids_a = None
        self.grids_b = None
        self.filename_a_out = None
        self.filename_b_out = None

    def read_file(fileName):
        inputList = []
        file = open(fileName, 'r')
        stop = False
        while True:
            firstline = list(file.readline())
            firstline = firstline[:-1]
            line = [firstline]
            next = file.readline()
            while next != '\n':
                count = 0
                a = list(next)
                if a[-1] == "\n":
                    a = a[:-1]
                line.append(a)
                next = file.readline()
                if next == '':
                    stop = True
                    break
            inputList.append(line)
            if stop:
                break
        return inputList

    # Find start point and goal point
    def find_start_goal(self, grid):
        start_goal = [0, 0]
        rows = len(grid)
        cols = len(grid[0])
        for row in range(0,rows):
            for col in range(0,cols):
                if grid[row][col] == "S":
                    start_goal[0] = (row, col)
                elif grid[row][col] == "G":
                    start_goal[1] = (row, col)
        print("Start point is at:", start_goal[0], "\nEnd point is at:", start_goal[1])
        return start_goal

    def heuristic(self, x, y):
        return (sum([(a - b) ** 2 for a, b in zip(x, y)]))**0.5

    def A_star(self, grid, start, goal, move):
        frontier = []
        cost_so_far = {start: 0}
        priority = {start: self.heuristic(start, goal)}
        pq.heappush(frontier, (priority[start], start))

        visited = set()
        came_from = dict()

        while frontier:
            current = pq.heappop(frontier)[1]

            # If goal found
            if current == goal:  # If its goal its done, and print the path
                print("Goal Found")
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]  # Back trace to origin
                path = list(reversed(path))  # Reverse the path to real goal
                return path

            visited.add(current)
            for i, j in moves:
                neighbor = current[0] + i, current[1] + j
                new_cost = cost_so_far[current] + self.heuristic(current, neighbor)
                if 0 <= neighbor[0] < len(grid):
                    if 0 <= neighbor[1] < len(grid[0]):
                        if grid[neighbor[0]][neighbor[1]] == "X":
                            continue
                    else:
                        # Grid bound y walls
                        continue
                else:
                    # Grid bound x walls
                    continue

                if neighbor in visited and new_cost >= cost_so_far.get(neighbor, 0):
                    continue

                if new_cost < cost_so_far.get(neighbor, 0) or neighbor not in came_from:
                    came_from[neighbor] = current
                    cost_so_far[neighbor] = new_cost
                    priority[neighbor] = new_cost + self.heuristic(neighbor, goal)
                    pq.heappush(frontier, (priority[neighbor], neighbor))
        print("Goal Not Found")
        return None

    def greedy(self, grid, start, goal, move):
        frontier = []  # This is a priority queue
        priority = {start: self.heuristic(start, goal)}
        pq.heappush(frontier, (priority[start], start))
        visited = set()
        came_from = dict()  # Start comes from none

        while frontier:
            current = pq.heappop(frontier)[1]  # Get coordinate

            if current == goal:  # If its goal is found
                print("Goal Found")
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]  # Back trace to origin
                path = list(reversed(path))  # Reverse the path to real goal
                return path

            visited.add(current) # Add current into visited list, prevent visit again

            for i, j in moves:
                neighbor = current[0] + i, current[1] + j  # Neighbor's coordinate calculated with the move list
                if 0 <= neighbor[0] < len(grid):  # If its inside left and right wall
                    if 0 <= neighbor[1] < len(grid[0]): # If itz inside up and bottom wall
                        if grid[neighbor[0]][neighbor[1]] == "X":  # If its a internal wall
                            continue # Skip this move
                    else:
                        # Grid bound y walls
                        continue
                else:
                    # Grid bound x walls
                    continue

                if neighbor in visited:
                    continue

                if neighbor not in came_from:
                    priority[neighbor] = self.heuristic(neighbor, goal)
                    pq.heappush(frontier, (priority[neighbor], neighbor))
                    came_from[neighbor] = current
        print("Goal Not Found")
        return None

def mazes_maker(num):
    mazes = []
    for i in range(num):
        maze = [["X"]*1024]
        for j in range(1022):
            row = ["X"]
            for k in range(1022):
                row.append("X" if random() < 0.6 else "_")
            row.append("X")
            maze.append(row)
        mazes.append(maze)
    for maze in mazes:
        start = [int(1021*random() + 1),int(1021*random() + 1)]
        goal = [int(1021*random() + 1),int(1021*random() + 1)]
        maze[start[0]][start[1]] = "S"
        maze[goal[0]][goal[1]] = "G"
    print("finished initializing mazes")
    return mazes

mazes = mazes_maker(10)
pf = pathfinding()

for m in mazes:
    sg = pf.find_start_goal(m)
    a.A_star(m, sg[0], sg[1], )
