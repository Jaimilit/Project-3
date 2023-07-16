
# Legend
#  "." = water or empty space
#  "O" = part of ship
#  "X" = part of ship that was hit by a shot
#  "#" = a shot that missed and lands in water

import random
import time


# Global variable for grid
grid = [[]]
# Global variable for grid size
grid_size = 10
# Global variable for number of ships placed on grid
num_of_ships = 5
# Global variable for shots left
shots_left = 25
# Global variable for game over
game_over = False
# Global variable for number of ships sunk
num_of_ships_sunk = 0
# Global variable for ship positions
ship_positions = [[]]
# Global variable for alphabet
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def create_grid_and_place_ships(start_row, end_row, start_col, end_col):
    """
    Checks rows & columns for ship placement
    """
    global grid
    global ship_positions

    all_valid = True
    for r in range(start_row, end_row):
        for c in range(start_col, end_col):
            if grid[r][c] != ".":
                all_valid = False
                break
    if all_valid:
        ship_positions.append([start_row, end_row, start_col, end_col])
        for r in range(start_row, end_row):
            for c in range(start_col, end_col):
                grid[r][c] = "O"
    return all_valid


def place_ships(row, col, direction, length):
    """
    Place ships on grid - random method
    """
    global grid_size

    start_row, end_row, start_col, end_col = row, row + 1, col, col + 1
    if direction == "left":
        if col - length < 0:
            return False
        start_col = col - length + 1

    elif direction == "right":
        if col + length >= grid_size:
            return False
        end_col = col + length

    elif direction == "up":
        if row - length < 0:
            return False
        start_row = row - length + 1

    elif direction == "down":
        if row + length >= grid_size:
            return False
        end_row = row + length

    return create_grid_and_place_ships(start_row, end_row, start_col, end_col)


def create_grid():
    """
    creates a 10x10 grid & randomly place ships
       of different sizes in different directions
       """
    global grid
    global grid_size
    global num_of_ships
    global ship_positions

    random.seed(time.time())

    rows, cols = (grid_size, grid_size)

    grid = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(".")
        grid.append(row)

    num_of_ships_placed = 0

    ship_positions = []

    while num_of_ships_placed != num_of_ships:
        random_row = random.randint(0, rows - 1)
        random_col = random.randint(0, cols - 1)
        direction = random.choice(["left", "right", "up", "down"])
        ship_size = random.randint(3, 5)
        if place_ships(random_row, random_col, direction, ship_size):
            num_of_ships_placed += 1


def print_grid():
    """
    Will print the grid with rows A-J and columns 0-9
    """
    global grid
    global alphabet

    debug_mode = False

    alphabet = alphabet[0: len(grid) + 1]

    for row in range(len(grid)):
        print(alphabet[row], end=") ")
        for col in range(len(grid[row])):
            if grid[row][col] == "O":
                if debug_mode:
                    print("O", end=" ")
                else:
                    print(".", end=" ")
            else:
                print(grid[row][col], end=" ")
        print("")

    print("  ", end=" ")
    for i in range(len(grid[0])):
        print(str(i), end=" ")
    print("")


def accept_valid_placement():
    """
    Will get valid row and column to place shot
    """
    global alphabet
    global grid

    is_valid_placement = False
    row = -1
    col = -1
    while is_valid_placement is False:
        placement = input("Enter row A-J and column 0-9. Example C6: ")
        placement = placement.upper()
        if len(placement) <= 0 or len(placement) > 2:
            print("Error: Please enter only one row and column such as C6:")
            continue
        row = placement[0]
        col = placement[1]
        if not row.isalpha() or not col.isnumeric():
            print("Error: Please enter letter A-J for row and 0-9 for column")
            continue
        row = alphabet.find(row)
        if not (-1 < row < grid_size):
            print("Error: Please enter letter A-J for row and 0-9 for column")
            continue
        col = int(col)
        if not (-1 < col < grid_size):
            print("Error: Please enter letter A-J for row and 0-9 for column")
            continue
        if grid[row][col] == "#" or grid[row][col] == "X":
            print("You have already made this shot. Try another location")
            continue
        if grid[row][col] == "." or grid[row][col] == "O":
            is_valid_placement = True

    return row, col


def check_for_ship_sunk(row, col):
    """
    If all parts of a shit have been shot it is sunk and we count how many ships sunk
    """
    global ship_positions
    global grid

    for position in ship_positions:
        start_row = position[0]
        end_row = position[1]
        start_col = position[2]
        end_col = position[3]
        if start_row <= row <= end_row and start_col <= col <= end_col:
            # Ship found, now check if its all sunk
            for r in range(start_row, end_row):
                for c in range(start_col, end_col):
                    if grid[r][c] != "X":
                        return False
    return True


def attempt_shot():
    """
    Updates grid and ships based on where the shot was located
    """
    global grid
    global num_of_ships_sunk
    global shots_left

    row, col = accept_valid_placement()
    print("")
    print("----------------------------")

    if grid[row][col] == ".":
        print("You missed, no ship was shot")
        grid[row][col] = "#"
    elif grid[row][col] == "O":
        print("You hit!", end=" ")
        grid[row][col] = "X"
        if check_for_ship_sunk(row, col):
            print("Yay! A ship was completely sunk!")
            num_of_ships_sunk += 1
        else:
            print("Good job. A ship was shot")

    shots_left -= 1


def check_for_game_over():
    """
    If all ships have been sunk or we run out of shots its game over
    """
    global num_of_ships_sunk
    global num_of_ships
    global shots_left
    global game_over

    if num_of_ships == num_of_ships_sunk:
        print("Congrats you won the game!")
        game_over = True
    elif shots_left <= 0:
        print("Sorry, you lost! You ran out of shots, try again next time!")
        game_over = True


def main():
    """
    Main entry point of application that runs the game loop
    """
    global game_over

    print("-----Welcome to Battleships-----")
    print("You have 25 shots to take down 5 ships, may the battle begin!")

    create_grid()

    while game_over is False:
        print_grid()
        print("Number of ships remaining: " + str(num_of_ships - num_of_ships_sunk))
        print("Number of shots left: " + str(shots_left))
        attempt_shot()
        print("----------------------------")
        print("")
        check_for_game_over()

main()

