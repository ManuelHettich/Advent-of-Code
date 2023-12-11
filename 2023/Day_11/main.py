import os

SAMPLE_INPUT = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""

def parse_input(puzzle_input):
    """
    Parse the cosmic data into a grid representation.
    
    Args:
    puzzle_input (str): Multiline string representing the cosmic data.

    Returns:
    list of list of str: A grid representation of the cosmic data.
    """
    return [list(line) for line in puzzle_input.splitlines()]

def count_galaxies(grid):
    """
    Count the number of galaxies in each row and column of the grid.

    Args:
    grid (list of list of str): Grid representation of the cosmic data.

    Returns:
    tuple: Two lists containing the count of galaxies in each row and column.
    """
    row_galaxy_counts = [0] * len(grid)
    column_galaxy_counts = [0] * len(grid[0])
    for row_index, row in enumerate(grid):
        for column_index, cell in enumerate(row):
            if cell == "#":
                row_galaxy_counts[row_index] += 1
                column_galaxy_counts[column_index] += 1
    return row_galaxy_counts, column_galaxy_counts

def adjust_counts(galaxy_counts, expansion_factor):
    """
    Adjust the galaxy counts for rows or columns considering the expansion factor.

    Args:
    galaxy_counts (list of int): Counts of galaxies in rows or columns.
    expansion_factor (int): Factor by which empty spaces are expanded.

    Returns:
    list of int: Adjusted counts considering the expansion factor.
    """
    adjusted_counts = []
    current_position = 0
    for count in galaxy_counts:
        for _ in range(count):
            adjusted_counts.append(current_position)
        current_position += 1 if count else expansion_factor
    return adjusted_counts

def sum_distances(adjusted_counts):
    """
    Calculate the sum of distances based on adjusted galaxy counts.

    Args:
    adjusted_counts (list of int): Adjusted counts of galaxies.

    Returns:
    int: Total sum of the distances calculated.
    """
    total_distance = 0
    accumulated_distance = 0
    for index, value in enumerate(adjusted_counts):
        total_distance += index * value - accumulated_distance
        accumulated_distance += value
    return total_distance

def solve(row_counts, col_counts, expansion_factor):
    """
    Solve the puzzle for given row and column counts and expansion factor.

    Args:
    row_counts (list of int): Counts of galaxies in each row.
    col_counts (list of int): Counts of galaxies in each column.
    expansion_factor (int): Expansion factor for empty spaces.

    Returns:
    int: Total sum of shortest path lengths in the expanded universe.
    """
    return sum_distances(adjust_counts(row_counts, expansion_factor)) + \
           sum_distances(adjust_counts(col_counts, expansion_factor))

# Main function

def main():
    # Reading input data
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_file_path = os.path.join(dir_path, "input.txt")
    with open(input_file_path, "r") as input_file:
        input_data = input_file.read()

    grid = parse_input(input_data)
    row_counts, col_counts = count_galaxies(grid)

    # Part 1: Loop tracing
    print("Part 1:", solve(row_counts, col_counts, 2))

    # Part 2: Interior area calculation
    print("Part 2:", solve(row_counts, col_counts, 1000000))

if __name__ == "__main__":
    main()
