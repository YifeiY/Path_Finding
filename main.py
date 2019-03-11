
from math import sqrt
from copy import copy

def main():
  maze,start,goal = readFile("pathfinding_a.txt")

  print("Got Maze:")
  showMaze(maze)

  # Greedy Search
  greedy_solution = writeSolutionToMaze(maze,greedy(maze,start,goal))
  print("\nGreedy Algorithm Solution")
  showMaze(greedy_solution)



def greedy(maze,start,goal):

  # Base case: solution found
  if start == goal:
    return [goal]

  # identify where can we move to
  legal_points = legalPoints(maze,start)

  # Base case: dead end
  if len(legal_points) == 0:
    return []

  #calculate distance square of the points identified to the goal
  for next in legal_points:
    next.append((next[0] - goal[0])**2 + (next[1] - goal[1])**2)

  # sort according to the heuristics (distance square)
  legal_points.sort(key = lambda x: x[2])

  # search for solution
  for point in legal_points:
    point = point[:-1]
    new_maze = copy(maze)
    maze[start[0]][start[1]] = "S"
    solution = [start]
    solution += greedy(new_maze,point,goal)
    if solution[-1] == goal:
      return solution
  return [] # No solution found

def writeSolutionToMaze(maze,solution):
  for p in solution:
    maze[p[0]][p[1]] = "P"
  maze[solution[0][0]][solution[0][1]] = "S"
  maze[solution[-1][0]][solution[-1][1]] = "G"
  return maze


def legalPoints(maze,center):
    bound = len(maze)
    illegal = ["X","S"]
    coordinates = []
    if center[0] - 1 >= 0 and maze[center[0] - 1][center[1]] not in illegal:
      coordinates.append([center[0] - 1,center[1]])
    if center[0] + 1 <= bound and maze[center[0] + 1][center[1]] not in illegal:
      coordinates.append([center[0] + 1,center[1]])
    if center[1] - 1 >= 0 and maze[center[0]][center[1] - 1] not in illegal:
      coordinates.append([center[0],center[1] - 1])
    if center[1] + 1 <= bound and maze[center[0]][center[1] + 1] not in illegal:
      coordinates.append([center[0],center[1] + 1])
    return coordinates


## convert input file to list representation of the maze
## return maze, start coordinates, goal coordinates
def readFile(filename):
  file = open(filename, "r")
  arr = []
  start = [0,0]
  goal = [0,0]

  for line in file:
    if line[-1] == '\n':
      line = line[:-1]
    arr.append(list(line))

  maze = []
  for i in range(len(arr)):
    line = arr[i]
    for j in range(len(line)):
      token = line[j]
      if token == "S":
        start = [i,j]
      elif token == "G":
        goal = [i,j]
    maze.append(line)
  return maze, start, goal

## prints the maze
def showMaze(maze):
  for row in maze:
    print(row)





main()