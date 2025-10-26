import os
import numpy as np
from queue import Queue
import time

pwd = os.getcwd()
file_path = os.path.join(pwd, "maze3.txt")

RED = '\033[1;31m'
GREEN = '\033[1;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[1;34m'
RESET = '\033[0m'



def isMapValid(file_path):
    with open(file_path, "r", encoding="UTF-8") as file:
        lines = file.readlines()

    row_count = len(lines)
    max_len = max(len(line.strip("\n")) for line in lines)

    for i, line in enumerate(lines):
        line_len = len(line.strip("\n"))
        if line_len < max_len:
            lines[i] = line.strip("\n") + (" " * (max_len - line_len)) + "\n"

    with open(file_path, "w", encoding="UTF-8") as file:
        file.writelines(lines)

    return row_count, max_len


def getCharsMap():
    rows, cols = isMapValid(file_path)
    chars = []
    with open(file_path, "r", encoding="UTF-8") as file:
        for line in file:
            line = line.strip("\n")
            chars.extend(list(line))
    return np.array(chars).reshape(rows, cols)


def get_neighbours(current, maze_chars):

    x, y = current
    rows, cols = maze_chars.shape

    directions = {
        "┼": ["up", "down", "left", "right"],
        "┐": ["down", "left"],
        "┤": ["up", "down", "left"],
        "╵": ["up"],
        "│": ["up", "down"],
        "┘": ["up", "left"],
        "┴": ["up", "right", "left"],
        "╷": ["down"],
        "─": ["right", "left"],
        "└": ["up", "right"],
        "├": ["up", "down", "right"],
        "╴": ["left"],
        " ": [],
        "┌": ["down", "right"],
        "┬": ["down", "right", "left"],
        "╶": ["right"]
    }

    moves = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1)
    }

    opposite = {"up": "down", "down": "up", "left": "right", "right": "left"}

    current_char = maze_chars[x, y]
    allowed_dirs = directions.get(current_char, [])
    neighbours = []

    for dir_name in allowed_dirs:
        dx, dy = moves[dir_name]
        nx, ny = x + dx, y + dy

        if 0 <= nx < rows and 0 <= ny < cols:
            neighbour_char = maze_chars[nx, ny]
            neighbour_dirs = directions.get(neighbour_char, [])
            if opposite[dir_name] in neighbour_dirs:
                neighbours.append((nx, ny))

    return neighbours


def display_maze(maze_chars, visited, queue, start, goal):
    os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(len(maze_chars)):
        for j in range(len(maze_chars[0])):
            pos = (i, j)
            if pos == start:
                print(RED + "S" + RESET, end="")
            elif pos == goal:
                print(BLUE + "E" + RESET, end="")
            elif pos in visited:
                print(GREEN + "." + RESET, end="")
            elif pos in queue:
                print(YELLOW + "?" + RESET, end="")
            else:
                print(maze_chars[i][j], end="")
        print()

def getPosition():
    maze_chars = getCharsMap()
    rows, cols = maze_chars.shape
    while True:
        try:
            x = int(input(f"Enter start X (0-{rows-1}): "))
            y = int(input(f"Enter start Y (0-{cols-1}): "))
            x1 = int(input(f"Enter end X (0-{rows-1}): "))
            y1 = int(input(f"Enter end Y (0-{cols-1}): "))
        except ValueError:
            print(" Wprowadź liczby całkowite.")
            continue

        if maze_chars[x][y] != " " and maze_chars[x1][y1] != " ":
            print(f"Start: ({x},{y}), End: ({x1},{y1})")
            return x, y, x1, y1
        else:
            print(" Start i koniec nie mogą być puste.")


def bfsMaze():
    visited = []
    processed = Queue()
    xStart, yStart, xEnd, yEnd = getPosition()
    path = []
    parents = {}
    steps = 0

    start = (xStart, yStart)
    goal = (xEnd, yEnd)
    maze_chars = getCharsMap()

    processed.put(start)
    visited.append(start)

    while not processed.empty():
        current = processed.get()
        steps += 1

        display_maze(maze_chars, visited, list(processed.queue), start, goal)
        time.sleep(0.1)

        if current == goal:
            while current in parents:
                path.append(current)
                current = parents[current]
            path.append(start)
            path.reverse()
            print(GREEN + f"\n Ścieżka znaleziona w {steps} krokach!" + RESET)
            print(GREEN + f"Ścieżka: {path}" + RESET)
            return path

        for neighbor in get_neighbours(current, maze_chars):
            if neighbor not in visited:
                processed.put(neighbor)
                visited.append(neighbor)
                parents[neighbor] = current

    print(RED + "\nbf Brak ścieżki!" + RESET)
    print(f"Ilość kroków: {steps}")
    return None


def dfsMaze():
    visited = []
    stack = []
    xStart, yStart, xEnd, yEnd = getPosition()
    path = []
    parents = {}
    steps = 0

    start = (xStart, yStart)
    goal = (xEnd, yEnd)
    maze_chars = getCharsMap()

    stack.append(start)
    visited.append(start)

    while stack:
        current = stack.pop()
        steps += 1

        display_maze(maze_chars, visited, stack, start, goal)
        time.sleep(0.1)

        if current == goal:
            while current in parents:
                path.append(current)
                current = parents[current]
            path.append(start)
            path.reverse()
            print(GREEN + f"\n Ścieżka znaleziona w {steps} krokach!" + RESET)
            print(GREEN + f"Ścieżka: {path}" + RESET)
            return path

        for neighbor in get_neighbours(current, maze_chars):
            if neighbor not in visited:
                stack.append(neighbor)
                visited.append(neighbor)
                parents[neighbor] = current

    print(RED + "\n Brak ścieżki!" + RESET)
    print(f"Ilość kroków: {steps}")
    return None


if __name__ == "__main__":
    print("=== LABIRYNT — Przeszukiwanie BFS / DFS ===")
    algo = input("Wybierz algorytm (BFS/DFS): ").upper()
    if algo == "BFS":
        bfsMaze()
    elif algo == "DFS":
        dfsMaze()
    else:
        print(" Niepoprawny wybór algorytmu.")


