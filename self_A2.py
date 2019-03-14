import heapq as pq
from random import random

class pathfinding:
    def __init__(self, filename_a="pathfinding_a.txt", filename_b="pathfinding_b.txt"):
        self.filename_a = filename_a
        self.filename_b = filename_b
        self.filename_a_out = "pathfinding_a_out.txt"
        self.filename_b_out = "pathfinding_b_out.txt"
        self.remove_empty = lambda input_list: [x for x in input_list if x]
        self.grids_a = self.read_file(self.filename_a)
        self.grids_b = self.read_file(self.filename_b)
        self.movement_without_diagonal = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self.movement_with_diagonal = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    def read_file(self, filename):
        input_list = []
        line = True
        with open(filename, "r") as f:
            tmp = []
            while line != "":
                line = f.readline()
                if len(line) > 1:
                    tmp.append(list(line[:-1]) if line[-1]=="\n" else list(line))
                else:
                    input_list.append(tmp)
                    tmp = []
        return self.remove_empty(input_list)

    def write_file(self, filename, path, algo_type):
        with open(filename, "a+") as f:
            f.write(algo_type+"\n")
            for p in path:
                f.write("".join(p))
                f.write("\n")
            if algo_type == "A*":
                f.write("\n")
        print("Write Completes")
        return None

    def draw(self, path, grid):
        for x, y in path:
            if grid[x][y] == "G":
                continue
            grid[x][y] = "P"
        return grid

    # Find start point and goal point
    def find_start_goal(self, grid):
        start_goal = [None, None]
        rows = len(grid)
        cols = len(grid[0])
        for row in range(0,rows):
            for col in range(0,cols):
                if grid[row][col] == "S":
                    start_goal[0] = (row, col)
                elif grid[row][col] == "G":
                    start_goal[1] = (row, col)
        print("Start point is at:", start_goal[0], "\nEnd point is at:", start_goal[1])
        start_goal = self.remove_empty(start_goal)
        return start_goal if len(start_goal)==2 else None

    # Euclidean distance on a grid
    def heuristic(self, x, y):
        return (sum([(a - b) ** 2 for a, b in zip(x, y)]))**0.5

    def A_star(self, grid, start, goal, movement):
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
            for i, j in movement:
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

    def greedy(self, grid, start, goal, movement):
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
            for i, j in movement:
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

    def execute(self, is_diagonal):
        if is_diagonal:
            for grid in self.grids_b:
                start_goal = self.find_start_goal(grid)
                if start_goal:
                    greedy_path = self.greedy(grid, start_goal[0], start_goal[-1], self.movement_with_diagonal)
                    self.write_file(self.filename_b_out, self.draw(greedy_path, grid), "Greedy")
                    print("Found solution for greedy algorithm")
                    A_star_path = self.A_star(grid, start_goal[0], start_goal[-1], self.movement_with_diagonal)
                    self.write_file(self.filename_b_out, self.draw(A_star_path, grid), "A*")
                    print("Found solution for A* algorithm")
                else:
                    print("Error")
                    return None
        else:
            for grid in self.grids_a:
                start_goal = self.find_start_goal(grid)
                if start_goal:
                    greedy_path = self.greedy(grid, start_goal[0], start_goal[-1], self.movement_without_diagonal)
                    self.write_file(self.filename_a_out, self.draw(greedy_path, grid), "Greedy")
                    print("Found solution for greedy algorithm")
                    A_star_path = self.A_star(grid, start_goal[0], start_goal[-1], self.movement_without_diagonal)
                    self.write_file(self.filename_a_out, self.draw(A_star_path, grid), "A*")
                    print("Found solution for A* algorithm")
                else:
                    print("Error")
                    return None
        print("Execute Finished")
        return None

if __name__ == "__main__":
    pf = pathfinding()
    pf.execute(False)
    pf.execute(True)
