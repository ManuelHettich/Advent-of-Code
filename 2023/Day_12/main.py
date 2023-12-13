import os
from functools import cache

SAMPLE_INPUT = """#.#.### 1,1,3
.#...#....###. 1,1,3
.#.###.#.###### 1,3,1,6
####.#...#... 4,1,1
#....######..#####. 1,6,5
.###.##....# 3,2,1
"""

@cache
def count_valid_spring_arrangements(spring_conditions, damage_groups, current_length=0):
    """
    Counts the valid arrangements of operational and broken springs based on the given criteria.

    Parameters:
    - spring_conditions (str): A string representing the condition of each spring (operational '.', broken '#', or unknown '?').
    - damage_groups (tuple of int): Tuple representing the size of each contiguous group of damaged springs.
    - current_length (int): Current length of the contiguous group being evaluated.

    Returns:
    int: The total number of valid arrangements that match the criteria.
    """
    if not spring_conditions:
        return (not damage_groups and current_length == 0) or (len(damage_groups) == 1 and damage_groups[0] == current_length)

    if damage_groups and current_length > damage_groups[0] or (not damage_groups and current_length):
        return False

    first_char, remaining_conditions = spring_conditions[0], spring_conditions[1:]
    arrangements = 0

    if first_char in '#?':
        arrangements += count_valid_spring_arrangements(remaining_conditions, damage_groups, current_length + 1)

    if first_char in '.?':
        if not current_length:
            arrangements += count_valid_spring_arrangements(remaining_conditions, damage_groups, 0)
        elif current_length == damage_groups[0]:
            arrangements += count_valid_spring_arrangements(remaining_conditions, damage_groups[1:], 0)

    return arrangements

def part1(spring_data):
    """
    Part 1 of the challenge: Counts the total number of valid arrangements of operational and broken springs.

    Parameters:
    - spring_data: List of strings representing the condition of springs and damage groups.

    Returns:
    int: Total number of valid arrangements for part 1.
    """
    total = 0
    for line in spring_data:
        records, groups = line.split()
        groups = tuple(map(int, groups.split(',')))
        total += count_valid_spring_arrangements(records, groups)
    return total

def part2(spring_data):
    """
    Part 2 of the challenge: Counts the total number of valid arrangements of operational and broken springs
    for a modified condition where each record is quintupled and groups are quintupled.

    Parameters:
    - spring_data: List of strings representing the condition of springs and damage groups.

    Returns:
    int: Total number of valid arrangements for part 2.
    """
    total = 0
    for line in spring_data:
        records, groups = line.split()
        groups = tuple(map(int, groups.split(',')))
        modified_records = '?'.join([records] * 5)
        modified_groups = groups * 5
        total += count_valid_spring_arrangements(modified_records, modified_groups)
    return total


def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_file_path = os.path.join(dir_path, "input.txt")
    with open(input_file_path, "r") as input_file:
        input_data = input_file.readlines()
    
    spring_data = [line.strip() for line in input_data]

    print("Part 1:", part1(spring_data))
    print("Part 2:", part2(spring_data))


if __name__ == "__main__":
    main()
