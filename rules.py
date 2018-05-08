# Cellular automaton
# Carter Sifferman, 2018
# For CSCI 474 Artificial Intelligence: Dr. Branton, Drury University

import random

# Cells die every round, are born if they have 3 neighbors.
def seeds(grid, next_grid):
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid) - 1):
            if grid[i][j] == 0:
                neighbors = [grid[i - 1][j], grid[i + 1][j], grid[i][j - 1], grid[i][j + 1],
                             grid[i - 1][j + 1], grid[i - 1][j - 1], grid[i + 1][j + 1],
                             grid[i + 1][j - 1]]
                if sum(neighbors) == 2:
                    next_grid[i][j] = 1
    return next_grid


# If cell is alive with 2 or 3 neighbors it stays alive, else it dies.
# If dead with three neighbors it becomes alive else it stays dead
def life(grid, next_grid):
    for i in range(1, len(grid)-1):
        for j in range(1, len(grid)-1):
            neighbors = [grid[i - 1][j], grid[i + 1][j], grid[i][j - 1], grid[i][j + 1],
                         grid[i - 1][j + 1], grid[i - 1][j - 1], grid[i + 1][j + 1],
                         grid[i + 1][j - 1]]
            if grid[i][j] == 1:
                if sum(neighbors) < 2 or sum(neighbors) > 3:
                    next_grid[i][j] = 0
                if sum(neighbors) in (2, 3):
                    next_grid[i][j] = 1
            else:
                if sum(neighbors) == 3:
                    next_grid[i][j] = 1
    return next_grid


# Cells never die, are born if they have 3 neighbors
def life_without_death(grid, next_grid):
    for i in range(1, len(grid)-1):
        for j in range(1, len(grid)-1):
            neighbors = [grid[i - 1][j], grid[i + 1][j], grid[i][j - 1], grid[i][j + 1],
                         grid[i - 1][j + 1], grid[i - 1][j - 1], grid[i + 1][j + 1],
                         grid[i + 1][j - 1]]
            if sum(neighbors) == 3:
                grid[i][j] = 1
    return grid


def bubbles(grid, next_grid):
    for i in range(1, len(grid)-1):
        for j in range(1, len(grid)-1):
            if grid[i][j] == 1:
                choice = random.choice([1, 2, 3, 4])

                if choice == 1:                 # drift left
                    next_grid[i-1][j+1] = 1

                elif choice == 2:               # drift right
                    next_grid[i+1][j+1] = 1

                elif choice == 3:               # straight up
                    next_grid[i][j+1] = 1

                elif choice == 4:               # split or DIE
                    if random.choice([0, 0, 0, 1, 1, 1, 1]):
                        if random.choice([0,1]):
                            next_grid[i+1][j+1] = 1
                            next_grid[i-1][j] = 1
                        else:
                            next_grid[i+1][j] = 1
                            next_grid[i-1][j+1] = 1

    return next_grid
