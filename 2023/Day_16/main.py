import os
from collections import deque

# ------- Part 1 -------

def parse_input(input_text):
    """
    Parses the input text into a grid.

    Parameters:
    - input_text (str): The raw input text representing the grid.

    Returns:
    list of list of str: A grid representation of the puzzle input.
    """
    # Split the input text into lines and then split each line into a list of characters
    return [list(line) for line in input_text.splitlines()]

def simulate_light_beam(grid, start_position, direction):
    """
    Simulates the light beam's travel through the grid and counts the number of energized tiles.

    Parameters:
    - grid (list of list of str): The grid representation of the puzzle input.
    - start_position (tuple): The starting position of the light beam.
    - direction (tuple): The initial direction of the light beam.

    Returns:
    int: The count of energized tiles.
    """
    beam_queue = deque([(start_position, direction)])  # Queue to manage the beam's position and direction
    visited = set()  # Set to keep track of visited positions and directions
    energized_tiles = set()  # Set to keep track of energized tiles

    while beam_queue:
        (row, col), (delta_row, delta_col) = beam_queue.pop()

        # Continue moving the beam while it's within the grid and hasn't been in this state before
        while 0 <= row < len(grid) and 0 <= col < len(grid[0]) and ((row, col, delta_row, delta_col) not in visited):
            visited.add((row, col, delta_row, delta_col))  # Mark the current state as visited
            energized_tiles.add((row, col))  # Mark the current tile as energized

            current_tile = grid[row][col]

            # Reflect or split the beam based on the encountered tile
            if current_tile == "/":
                delta_row, delta_col = -delta_col, -delta_row
            elif current_tile == "\\":
                delta_row, delta_col = delta_col, delta_row
            elif current_tile == "-" and delta_row != 0:
                delta_row, delta_col = 0, 1
                beam_queue.append(((row, col - 1), (0, -1)))
            elif current_tile == "|" and delta_col != 0:
                delta_row, delta_col = 1, 0
                beam_queue.append(((row - 1, col), (-1, 0)))

            row += delta_row
            col += delta_col

    return len(energized_tiles)


# ------- Part 2 -------

def find_max_energized_tiles(grid):
    """
    Finds the maximum number of energized tiles by starting the beam from different edges of the grid.

    Parameters:
    - grid (list of list of str): The grid representation of the puzzle input.

    Returns:
    int: The maximum count of energized tiles.
    """
    max_energized = 0  # Variable to store the maximum number of energized tiles
    grid_height = len(grid)  # Height of the grid
    grid_width = len(grid[0])  # Width of the grid

    # Check all possible starting positions on the grid's perimeter
    for row in range(grid_height):
        max_energized = max(max_energized, simulate_light_beam(grid, start_position=(row, 0), direction=(0, 1)))
        max_energized = max(max_energized, simulate_light_beam(grid, start_position=(row, grid_width - 1),
                                                                    direction=(0, -1)))

    for col in range(grid_width):
        max_energized = max(max_energized, simulate_light_beam(grid, start_position=(0, col), direction=(1, 0)))
        max_energized = max(max_energized, simulate_light_beam(grid, start_position=(grid_height - 1, col),
                                                                    direction=(-1, 0)))

    return max_energized

# Main function

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_file_path = os.path.join(dir_path, "input.txt")
    with open(input_file_path, "r") as input_file:
        input_data = input_file.read()
        input_data = rf"{input_data}"

    grid = parse_input(input_data)
    energized_tiles = simulate_light_beam(grid, start_position=(0, 0), direction=(0, 1))

    print("Part 1:", energized_tiles)
    print("Part 2:", find_max_energized_tiles(grid))


if __name__ == "__main__":
    main()
