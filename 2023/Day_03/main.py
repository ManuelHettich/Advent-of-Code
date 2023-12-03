# !/usr/bin/env python

# --- Day 3: Gear Ratios ---

import os
import re
from collections import defaultdict
from math import prod

SAMPLE_INPUT_1 = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

SAMPLE_INPUT_2 = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

# Regular expressions to find numbers and symbols in the schematic
NUMBER_PATTERN = re.compile(r"\d+")
SYMBOL_PATTERN = re.compile(r"[^\s\d.]")

def parse_engine_schematic(schematic):
    """
    Parses the engine schematic and yields the coordinates of the adjacent symbol and value of each number.

    Args:
    schematic (str): A multiline string representing the engine schematic.

    Yields:
    tuple: A tuple containing the coordinates (x, y) of the corresponding symbol and the number.
    """
    # Split the schematic into lines
    lines = schematic.splitlines()

    # Iterate over each line and its index (y-coordinate)
    for line_index, line in enumerate(lines):
        # Find each number in the line
        for number_match in NUMBER_PATTERN.finditer(line):
            number = int(number_match.group(0))
            # Find indices of the number
            number_start, number_end = number_match.span()

            # Check adjacent lines and within the span of the number + 1 for symbols
            for adjacent_line_index in range(max(line_index - 1, 0), min(line_index + 2, len(lines))):
                for symbol_match in SYMBOL_PATTERN.finditer(lines[adjacent_line_index],
                                                            number_start - 1,
                                                            number_end + 1):
                    # Yield the position and the number
                    yield symbol_match.start(), adjacent_line_index, number

def calculate_sum_of_part_numbers(schematic: str) -> int:
    """
    Calculates the sum of all part numbers in the schematic that are adjacent to a symbol.

    Args:
    schematic (str): A multiline string representing the engine schematic.

    Returns:
    int: The sum of all part numbers adjacent to a symbol.
    """
    # Sum all numbers that are adjacent to symbols
    return sum(number for _, _, number in parse_engine_schematic(schematic))

def calculate_total_gear_ratios(schematic: str) -> int:
    """
    Calculates the total of gear ratios in the schematic. A gear is represented by a 
    symbol '*' that is adjacent to exactly two part numbers. The gear ratio is 
    the product of these two numbers.

    Args:
    schematic (str): A multiline string representing the engine schematic.

    Returns:
    int: The total of all gear ratios.
    """
    # Dictionary to store part numbers adjacent to each gear
    gears_with_part_numbers = defaultdict(list)
    for symbol_start_index, symbol_line_index, number in parse_engine_schematic(schematic):
        gears_with_part_numbers[symbol_start_index, symbol_line_index].append(number)

    # Sum the product of part numbers for each gear
    return sum(prod(part_numbers) for part_numbers in gears_with_part_numbers.values() if len(part_numbers) == 2)



def main():
    # Read the input file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_file = open(dir_path + "/input.txt", "r")
    input_data = input_file.read()

    # Calculate the sum of part numbers and total gear ratios
    print("Part 1:", calculate_sum_of_part_numbers(input_data))
    print("Part 2:", calculate_total_gear_ratios(input_data))


if __name__ == "__main__":
    main()
