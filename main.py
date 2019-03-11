



def main():
  maze,start,goal = readFile("pathfinding_a.txt")

  showMaze(maze)


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