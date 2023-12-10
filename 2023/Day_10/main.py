import os

SAMPLE_INPUT = """
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""

# -------- Part 1 --------

def build_pipes(layout):
    """
    Construct a network of pipes from a given layout.

    Args:
    layout (str): Multiline string representing the pipe layout.

    Returns:
    tuple: Starting coordinate and a dictionary representing pipe connections.
    """
    pipes = {}
    for y, row in enumerate(layout.splitlines()):
        for x, char in enumerate(row):
            coord = (y, x)
            if char != ".":
                pipes[coord] = connect_pipes(char, coord)
    start_coord = find_start(pipes)
    pipes[start_coord] = {pos for pos in pipes[start_coord] if start_coord in pipes.get(pos, set())}
    return start_coord, pipes

def connect_pipes(char, coord):
    """
    Determine pipe connections based on the pipe character.

    Args:
    char (str): Character representing the pipe type.
    coord (tuple): Coordinates of the pipe.

    Returns:
    set: A set of tuples representing connected coordinates.
    """
    y, x = coord
    connections = {
        "|": {(y-1, x), (y+1, x)},
        "-": {(y, x-1), (y, x+1)},
        "L": {(y-1, x), (y, x+1)},
        "J": {(y, x-1), (y-1, x)},
        "7": {(y, x-1), (y+1, x)},
        "F": {(y+1, x), (y, x+1)},
        "S": {(y-1, x), (y+1, x), (y, x-1), (y, x+1)}
    }
    return connections.get(char, set())

def find_start(pipe_map):
    """
    Find the starting position 'S' in the pipe network.

    Args:
    pipe_map (dict): Dictionary representing the pipe network.

    Returns:
    tuple: Coordinates of the starting position.
    """
    for coord, connected in pipe_map.items():
        if len(connected) == 4:
            return coord

def trace_loop(start, network):
    """
    Trace the main loop in the pipe network starting from 'S'.

    Args:
    start (tuple): Starting coordinate.
    network (dict): Pipe network.

    Returns:
    set: Set of coordinates forming the loop.
    """
    current = next(iter(network[start]))
    loop = {start, current}

    while True:
        next_pos = network[current] - loop
        if not next_pos:
            break
        current = next(iter(next_pos))
        loop.add(current)

    return loop

# -------- Part 2 --------

def find_interior_area(pipe_network, loop):
    """
    Calculate the interior area enclosed by the loop.

    Args:
    pipe_network (dict): Pipe network.
    loop (set): Set of coordinates forming the loop.

    Returns:
    set: Set of coordinates inside the loop.
    """
    max_row = max(row for row, _ in pipe_network.keys()) + 1
    max_col = max(col for _, col in pipe_network.keys()) + 1

    interior = set()
    for row in range(max_row):
        num_north = 0
        for col in range(max_col):
            if (row, col) in loop:
                if (row - 1, col) in pipe_network[(row, col)]:
                    num_north += 1
            elif num_north % 2 == 1:
                interior.add((row, col))

    return interior

# Main function

def main():
    # Reading input data
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_file_path = os.path.join(dir_path, "input.txt")
    with open(input_file_path, "r") as input_file:
        input_data = input_file.read()

    start_coord, pipe_network = build_pipes(input_data)

    # Part 1: Loop tracing
    main_loop = trace_loop(start_coord, pipe_network)
    print("Part 1: Length of Main Loop:", len(main_loop)//2)

    # Part 2: Interior area calculation
    interior = find_interior_area(pipe_network, main_loop)
    print("Part 2: Size of Interior Area:", len(interior))

if __name__ == "__main__":
    main()
