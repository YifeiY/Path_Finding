
from math import sqrt
from copy import copy
from random import random
import sys
import threading
sys.setrecursionlimit(1024 * 512)
threading.stack_size(671088640)

def main():
  #print(sys.getrecursionlimit())
  maze,start,goal,illegal = readFile("pathfinding_a.txt")

  print("Got Maze:")
  showMaze(maze)

  # Greedy Search
  greedy_solution = writeSolutionToMaze(maze,greedy(maze,start,goal,[]))
  print("\nGreedy Algorithm Solution:")
  showMaze(greedy_solution)

  #checkEachAlgorithm([greedy])

## Greedy Search, return a list of solution
def greedy(maze,start,goal,tried):

  # Base case: solution found
  if start == goal:
    return [goal]

  # identify where can we move to
  legal_points = legalPoints(maze,start,tried)

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
    solution = [start]
    tried.append(point)
    solution += greedy(new_maze,point,goal,tried)
    if solution[-1] == goal:
      return solution
  return [] # No solution found


## Update the maze, replace a maze with solution path replaced by "P"
def writeSolutionToMaze(maze,solution):
  if solution == []:
    return["\tGreedy algorithm found no solution exists"]

  for p in solution:
    maze[p[0]][p[1]] = "P"
  maze[solution[0][0]][solution[0][1]] = "S"
  maze[solution[-1][0]][solution[-1][1]] = "G"
  return maze


## Identify where the next move can be, return an array of legal moves
def legalPoints(maze,center,tried):
    bound_y = len(maze)
    bound_x = len(maze[0])
    illegal = ["X","S"]
    coordinates = []
    if center[0] - 1 >= 0 and maze[center[0] - 1][center[1]] not in illegal and [center[0] - 1,center[1]] not in tried:
      coordinates.append([center[0] - 1,center[1]])
    if center[0] + 1 < bound_y and maze[center[0] + 1][center[1]] not in illegal and [center[0] + 1,center[1]] not in tried:
      coordinates.append([center[0] + 1,center[1]])
    if center[1] - 1 >= 0 and maze[center[0]][center[1] - 1] not in illegal and [center[0],center[1] - 1] not in tried:
      coordinates.append([center[0],center[1] - 1])
    if center[1] + 1 < bound_x and maze[center[0]][center[1] + 1] not in illegal and [center[0],center[1] + 1] not in tried:
      coordinates.append([center[0],center[1] + 1])
    return coordinates


## convert input file to list representation of the maze
## return maze, start coordinates, goal coordinates
def readFile(filename):
  file = open(filename, "r")
  arr = []
  start = [0,0]
  goal = [0,0]
  illegal = []

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
        illegal.append(start)
      elif token == "G":
        goal = [i,j]
      elif token == "X":
        illegal.append([i,j])
    maze.append(line)
  return maze, start, goal,illegal

## prints the maze
def showMaze(maze):
  for row in maze:
    print(row)

def checkEachAlgorithm(algorithms):
    incorrect_mazes = []
    mazes = []
    for i in range(100):
      maze = [["X"]*1024]
      for j in range(1022):
        row = ["X"]
        for k in range(1022):
          row.append("X" if random() < 0.2 else "_")
        row.append("X")
        maze.append(row)
      mazes.append(maze)
    print("finished initializing mazes")
    correctness = True

    ### BEG For Yifei's testing
    success = 0
    for maze in mazes:
      starting = [int(1021 * random()) + 1, int(1021 * random()) + 1]
      goaling = [int(1021 * random()) + 1, int(1021 * random()) + 1]
      print("Trying...",starting,goaling)
      if algorithms[0](maze,starting,goaling,[]) != False:
        print(1)
        success += 1
    print("successfully found solution for ",success,"mazes")
    exit(9)
    ### END For Yifei's testing

    for maze in mazes:
      correctness_of_maze = True
      start = [random(1,1024),random(1,1024)]
      goal = [random(1,1024),random(1,1024)]
      results = []
      for a in algorithms:
        if a(maze,start,goal) != False:
          result = True
        else:
          result = False
        results.append(result)
      last_result = results[0]
      for r in results:
        if last_result != r:
          correctness_of_maze = False
      if not correctness_of_maze:
        incorrect_mazes.append(maze)

    return incorrect_mazes


main()
