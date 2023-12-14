import os
from operator import itemgetter


SAMPLE_INPUT = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""

# ------- Part 1 -------

def parse_input(input_data):
    """
    Parse the puzzle input into a more manageable format.

    Parameters:
    - input_data (list of str): The puzzle input as a list of strings, each representing a row.

    Returns:
    list of list of str: A 2D grid representing the platform.
    """
    return [list(row.strip()) for row in input_data]

def tilt_platform_north(grid):
    """
    Tilts the platform to the north, causing all rounded rocks to move up.

    Parameters:
    - grid (list of list of str): The 2D grid representing the platform.

    Returns:
    list of list of str: Updated grid after tilting north.
    """
    for column_index in range(len(grid[0])):
        fixed_positions = set()
        movable_positions = set()
        for row_index in range(len(grid)):
            if grid[row_index][column_index] == "O":
                movable_positions.add((row_index, column_index))
            elif grid[row_index][column_index] == "#":
                fixed_positions.add((row_index, column_index))

        # Move the rounded rocks upwards
        new_movable_positions = fixed_positions.copy()
        for position in sorted(movable_positions, key=itemgetter(0)):
            row, col = position
            row -= 1
            while row >= 0 and (row, col) not in new_movable_positions:
                row -= 1
            new_movable_positions.add((row + 1, col))

        # Update the grid with the new positions
        for row, col in new_movable_positions - fixed_positions:
            grid[row][col] = "O"
        for row, col in movable_positions - (new_movable_positions - fixed_positions):
            grid[row][col] = "."

    return grid

def calculate_total_load(grid):
    """
    Calculates the total load on the north support beams.

    Parameters:
    - grid (list of list of str): The 2D grid representing the platform.

    Returns:
    int: The total load on the north support beams.
    """
    total_load = 0
    for row_index, row in enumerate(grid):
        load_per_row = sum(1 for cell in row if cell == "O")
        total_load += load_per_row * (len(grid) - row_index)
    return total_load

def part1(input_data):
    """
    Part 1 of the puzzle: Calculates the total load on the north support beams after tilting.

    Parameters:
    - input_data (list of str): The puzzle input.

    Returns:
    int: Total load on the north support beams.
    """
    grid = parse_input(input_data)
    tilted_grid = tilt_platform_north(grid)
    return calculate_total_load(tilted_grid)


# ------- Part 2 -------

def spin_cycle(fixed_positions, movable_positions, grid_height, grid_width, iterations):
    """
    Performs the 'spin cycle' by tilting the platform in four directions for a given number of iterations,
    detects repeating patterns, and calculates the total load after the specified number of cycles.

    Parameters:
    - fixed_positions (set of tuples): Set of coordinates for fixed objects on the grid.
    - movable_positions (set of tuples): Set of coordinates for movable objects on the grid.
    - grid_height (int): The height of the grid.
    - grid_width (int): The width of the grid.
    - iterations (int): Number of iterations to perform.

    Returns:
    int: Total load on the north support beams after the specified number of cycles.
    """
    seen_states = {frozenset(movable_positions): 0}

    # Cache to store the fixed positions after each 90-degree rotation
    rotation_cache = [(fixed_positions, grid_height)]
    for _ in range(3):
        last_fixed_positions, last_height = rotation_cache[-1]
        rotated_fixed_positions = rotate_90_degrees(last_fixed_positions, last_height)
        rotation_cache.append((rotated_fixed_positions, grid_width))
        grid_height, grid_width = grid_width, grid_height

    for current_iteration in range(1, iterations + 1):
        for fixed, height in rotation_cache:
            movable_positions = rotate_90_degrees(move_objects_north(fixed, movable_positions), height)

        state_key = frozenset(movable_positions)
        if state_key in seen_states:
            break

        seen_states[state_key] = current_iteration
        seen_states[current_iteration] = state_key

    cycle_start_iteration = seen_states[state_key]
    cycle_length = current_iteration - cycle_start_iteration
    remaining_iterations = iterations - cycle_start_iteration
    final_iteration = remaining_iterations % cycle_length + cycle_start_iteration

    return calculate_load_from_positions(seen_states[final_iteration], grid_height)

def rotate_90_degrees(coordinates, height):
    """
    Rotates the set of coordinates by 90 degrees.

    Parameters:
    - coordinates (set of tuples): Set of coordinates to rotate.
    - height (int): The height of the grid, used for rotation calculation.

    Returns:
    set of tuples: Rotated coordinates.
    """
    return set((col, height - row - 1) for row, col in coordinates)

def calculate_load_from_positions(positions, grid_height):
    """
    Calculates the total load on the north support beams based on the positions of the movable objects.

    Parameters:
    - positions (set of tuples): Set of coordinates of the movable objects.
    - grid_height (int): The height of the grid.

    Returns:
    int: Total load on the north support beams.
    """
    return sum(grid_height - row for row, _ in positions)

def move_objects_north(fixed_positions, movable_positions):
    """
    Moves the movable objects (rounded rocks) north considering the positions of fixed objects (cube-shaped rocks).

    Parameters:
    - fixed_positions (set of tuples): Set of coordinates for fixed objects on the grid.
    - movable_positions (set of tuples): Set of coordinates for movable objects on the grid.

    Returns:
    set of tuples: Updated positions of the movable objects after moving them north.
    """
    new_movable_positions = fixed_positions.copy()

    for position in sorted(movable_positions, key=itemgetter(0)):
        row, column = position
        # Move each movable object north until it hits a fixed object or the edge
        row -= 1
        while row >= 0 and (row, column) not in new_movable_positions:
            row -= 1

        new_movable_positions.add((row + 1, column))

    # Return the updated positions of movable objects, excluding the original fixed positions
    return new_movable_positions - fixed_positions

def part2(input_data):
    """
    Calculates the total load on the north support beams after 1,000,000,000 cycles of the spin cycle.

    Parameters:
    - grid (list of str): The puzzle input represented as a list of strings, each string being a row of the grid.

    Returns:
    int: Total load on the north support beams after 1,000,000,000 cycles.
    """
    grid = parse_input(input_data)

    height, width = len(grid), len(grid[0])
    fixed_positions = set()
    movable_positions = set()

    for row_index, row in enumerate(grid):
        for col_index, char in enumerate(row):
            if char == "#":
                fixed_positions.add((row_index, col_index))
            elif char == "O":
                movable_positions.add((row_index, col_index))

    return spin_cycle(fixed_positions, movable_positions, height, width, 1000000000)


# Main Execution

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_file_path = os.path.join(dir_path, "input.txt")
    with open(input_file_path, "r") as input_file:
        input_data = input_file.readlines()

    print("Part 1:", part1(input_data))
    print("Part 2:", part2(input_data))


if __name__ == "__main__":
    main()
