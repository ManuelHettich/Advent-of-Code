import os

SAMPLE_INPUT = """
#...#...#
.#..#..#.
...##...#
#....#..#
.#..#..#.
#...#...#
#...#...#
.#..#..#.
...##...#
"""

# -------- Part 1 --------

def find_reflection_line(pattern, comparison_function):
    """
    Finds the line of reflection in a given pattern.

    Parameters:
    - pattern (list of str or list of tuples): The pattern in which the reflection line is to be found.
    - comparison_function (function): A function that takes two halves of a pattern and returns
      True if they are reflected.

    Returns:
    int: The index at which the reflection line is found, or 0 if no reflection line is found.
    """
    pattern_list = list(pattern) if not isinstance(pattern, list) else pattern

    for index in range(1, len(pattern_list)):
        if comparison_function(pattern_list[index - 1 :: -1], pattern_list[index:]):
            return index
    return 0

def calculate_pattern_summary(data, comparison_function):
    """
    Calculates the summary value of each pattern in the data.

    Parameters:
    - data (str): Multiline string data representing different patterns.
    - comparison_function (function): Function to compare pattern halves for reflection.

    Returns:
    int: The total summary value for all patterns.
    """
    total = 0
    for group in data.strip().split("\n\n"):
        lines = group.splitlines()
        horizontal_reflection = 100 * find_reflection_line(lines, comparison_function)
        vertical_reflection = find_reflection_line(zip(*lines), comparison_function)
        total += horizontal_reflection + vertical_reflection
    return total

def are_reflected_horizontally(x, y):
    """
    Checks if two halves of a pattern are mirrored horizontally.

    Parameters:
    - x, y (list of str): Two halves of a pattern.

    Returns:
    bool: True if halves are mirrored horizontally, False otherwise.
    """
    length = min(len(x), len(y))
    return x[:length] == y[:length]

def part1(data):
    """
    Part 1 of the challenge: Finds the reflection line in each pattern and calculates the summary value.

    Parameters:
    - data (str): Multiline string data representing different patterns.

    Returns:
    int: Summary value calculated.
    """

    return calculate_pattern_summary(data, are_reflected_horizontally)

# -------- Part 2 --------

def are_reflected_with_one_smudge_corrected(x, y):
    """
    Checks if two halves of a pattern are mirrored with one smudge corrected.

    Parameters:
    - x, y (list of str or list of tuples): Two halves of a pattern.

    Returns:
    bool: True if halves are mirrored with one smudge corrected, False otherwise.
    """
    return sum(c != d for a, b in zip(x, y) for c, d in zip(a, b)) == 1

def part2(data):
    """
    Part 2 of the challenge: Finds the reflection line in each pattern with one smudge corrected
    and calculates the summary value.

    Parameters:
    - data (str): Multiline string data representing different patterns.

    Returns:
    int: Summary value calculated.
    """

    return calculate_pattern_summary(data, are_reflected_with_one_smudge_corrected)


def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_file_path = os.path.join(dir_path, "input.txt")
    with open(input_file_path, "r") as input_file:
        data = input_file.read()

    print("Part 1:", part1(data))
    print("Part 2:", part2(data))


if __name__ == "__main__":
    main()
