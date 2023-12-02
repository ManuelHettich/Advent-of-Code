# !/usr/bin/env python

import os
import re

# --- Day 1: Trebuchet?! ---


SAMPLE_INPUT_1 = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""
SAMPLE_INPUT_2 = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""

DIGITS = {
    "one": "o1e",  # Keep leading and trailing characters to handle overlaps
    "two": "t2o",
    "three": "t3e",
    "four": "f4r",
    "five": "f5e",
    "six": "s6x",
    "seven": "s7n",
    "eight": "e8t",
    "nine": "n9e"
}

def extract_numbers(line):
    # Search for the first and last digit number with a regex
    first_number = re.search(r"\d", line)
    second_number = re.search(r"\d", line[::-1])

    # Combine the two digit numbers
    line_number = int(first_number.group(0) + second_number.group(0))

    return line_number


def main():
    # Read the input file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_file = open(dir_path + "/input.txt", "r")
    input_data = input_file.read().splitlines()

    # Initialize the sums
    sum_0 = 0
    sum_1 = 0

    # Loop through each line
    for line in input_data:
        # ------- First Part -------
        sum_0 += extract_numbers(line)

        # ------- Second Part -------
        # Replace number words with digits
        for word, digit in DIGITS.items():
            line = line.replace(word, digit)

        sum_1 += extract_numbers(line)

    # Print the result of first part
    print("Part 1:", sum_0)
    print("Part 2:", sum_1)


if __name__ == "__main__":
    main()
