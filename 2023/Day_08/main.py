import os
import re
import math

SAMPLE_INPUT_1 = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

SAMPLE_INPUT_2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""

SAMPLE_INPUT_3 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""

def extract_network(input_data: str) -> dict:
    """
    Extract the network from the input data.

    Args:
    input_data (str): The input data.

    Returns:
    dict: The network of three-letter strings and tuples.
    """

    # Initialize an empty dictionary for the three-letter strings and tuples
    network = {}

    for line in input_data.split("\n"):
        # Use regular expressions to extract the network information
        match = re.match(r"([0-Z]+) = \(([0-Z]+), ([0-Z]+)\)", line)
        if match:
            key, value1, value2 = match.groups()
            network[key] = (value1, value2)

    return network

def extract_directions(input_data: str) -> [str]:
    """
    Extract the directions from the input data.

    Args:
    input_data (str): The input data.

    Returns:
    [str]: The list of directions.
    """

    return list(input_data.split("\n")[0])

def find_path(directions: [str], network: dict) -> int:
    """
    Get the next direction based on the current direction and turn.

    Args:
    directions ([str]): The list of directions.
    network (dict): The network of three-letter strings and tuples.

    Returns:
    int: The number of steps taken to reach ZZZ.
    """

    steps = 0
    position = "AAA"

    while position != "ZZZ":
        for direction in directions:
            if direction == "L":
                position = network[position][0]
            elif direction == "R":
                position = network[position][1]
            steps += 1
            if position == "ZZZ":
                break

    return steps


def find_all_paths(directions: [str], network: dict, starting_positions: [str]) -> int:
    """
    Get the next direction based on the current direction and turn.

    Args:
    directions ([str]): The list of directions.
    network (dict): The network of three-letter strings and tuples.
    starting_positions ([str]): The list of starting positions.

    Returns:
    int: The number of steps taken to reach only positions ending on Z from all starting positions simultaneously.
    """

    steps = 0
    positions = starting_positions.copy()
    cycles = {pos: 0 for pos in positions}

    while any(cycle == 0 for cycle in cycles.values()):
        for direction in directions:
            # Take a step for each position
            for idx, position in enumerate(positions):
                if direction == "L":
                    positions[idx] = network[position][0]
                elif direction == "R":
                    positions[idx] = network[position][1]
            steps += 1

            # Check if any position ends in Z
            for idx, position in enumerate(positions):
                if position[2] == "Z" and cycles[starting_positions[idx]] == 0:
                    cycles[starting_positions[idx]] += steps
            if all(cycle > 0 for cycle in cycles.values()):
                break

    return cycles


def main():
    # Read the input file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_file_path = os.path.join(dir_path, "input.txt")
    with open(input_file_path, "r") as input_file:
        input_data = input_file.read()

    directions = extract_directions(input_data)
    network = extract_network(input_data)

    # Part 1

    print("Part 1:", find_path(directions, network))

    # Part 2

    # Find all starting positions in the input text
    matches = re.findall(r"([0-Z]+A) =", input_data)

    # Convert the matches into a list
    starting_positions = list(matches)

    print("Part 2:", math.lcm(*find_all_paths(directions, network, starting_positions).values()))

if __name__ == "__main__":
    main()
