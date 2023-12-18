import os


SAMPLE_INPUT = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""

def parse_data(input_data):
    """
    Parses the dig plan into a list of directions and lengths.

    Parameters:
    - input_data (str): Multiline string representing the dig plan.

    Returns:
    list of tuples: Each tuple contains a direction ("R", "L", "U", "D") and a length.
    """

    dig_plan = []

    for line in input_data.splitlines():
        dig_plan.append((line[0], int(line[2:4])))

    return dig_plan

def calculate_lagoon_volume(steps):
    """
    Calculates the total volume of the lagoon based on the digger's steps.

    Parameters:
    - steps (list of tuples): The digger's steps as a list of directions and lengths.

    Returns:
    int: The total volume of the lagoon in cubic meters.
    """
    # Dictionary to convert directions to row and column movements
    direction_to_movement = {"R": (0, 1), "D": (1, 0), "L": (0, -1), "U": (-1, 0)}

    # Starting position
    current_row, current_col = 0, 0

    # Lists to store x and y coordinates of the vertices
    x_coordinates, y_coordinates = [current_col], [current_row]

    # Calculate the vertices of the polygon
    for direction, length in steps:
        move_row, move_col = direction_to_movement[direction]
        current_row += move_row * length
        current_col += move_col * length
        x_coordinates.append(current_col)
        y_coordinates.append(current_row)

    # Calculate the area using the Shoelace formula
    # Area = 1/2 * |sum(x[i] * (y[i+1] - y[i-1]) for i = 0 to n)|
    area = 0
    num_vertices = len(x_coordinates)
    for i in range(num_vertices - 1):
        area += x_coordinates[i] * (y_coordinates[i - 1] - y_coordinates[i + 1])
    area = abs(area) // 2

    # Calculate the circumference of the polygon
    circumference = sum(length for _, length in steps)

    # Adjust the area using Pick's theorem: Area = Interior + Boundary/2 - 1
    interior = area - circumference // 2 + 1
    total_area = interior + circumference

    # Volume is the area multiplied by the depth (1 meter)
    return total_area


# ------- Part 1 -------


def part1(input_data):
    """
    Solves part 1 of the puzzle.

    Parameters:
    - input_data (str): Multiline string representing the dig plan.

    Returns:
    int: The volume of lava the lagoon can hold.
    """
    dig_plan = parse_data(input_data)
    return calculate_lagoon_volume(dig_plan)

# ------- Part 2 -------

def parse_data_part2(input_data):
    """
    Parse input data to extract hexadecimal codes and convert them into digging instructions.

    Parameters:
    - input_data (str): Multiline string representing the dig plan with hexadecimal codes.

    Returns:
    list of tuples: Each tuple contains a direction ('R', 'L', 'U', 'D') and a length.
    """
    steps = []
    hex_to_dir = {"0": "R", "1": "D", "2": "L", "3": "U"}

    for line in input_data.split("\n"):
        _, _, hex_code = line.split()
        # Remove "(", "#" and ")"
        hex_code = hex_code[2:-1]
        direction = hex_to_dir[hex_code[-1]]
        # Convert hexadecimal to decimal
        distance = int(hex_code[:-1], 16)
        steps.append((direction, distance))
    return steps

def part2(input_data):
    """
    Solves part 2 of the puzzle.

    Parameters:
    - input_data (str): Multiline string representing the dig plan with hexadecimal codes.

    Returns:
    int: The volume of lava the lagoon can hold after following the corrected dig plan.
    """
    steps = parse_data_part2(input_data)
    return calculate_lagoon_volume(steps)

# Main function

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_file_path = os.path.join(dir_path, "input.txt")
    with open(input_file_path, "r") as input_file:
        input_data = input_file.read()

    print("Part 1:", part1(input_data))
    print("Part 2:", part2(input_data))


if __name__ == "__main__":
    main()
