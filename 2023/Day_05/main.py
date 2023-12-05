import re
import os
from functools import reduce
from operator import itemgetter

SAMPLE_INPUT = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

# Regular expression pattern to find all numbers
NUMBER_PATTERN = re.compile(r"\d+")

def parse_input(data):
    """
    Parses the input data into seeds and mappings for each category.

    Args:
    data (str): Input data string.

    Returns:
    tuple: A tuple containing a list of seeds and a list of mappings for each category.
    """
    # Splitting the data into sections
    sections = data.split("\n\n")

    # Extracting seeds
    seed_matches = NUMBER_PATTERN.finditer(sections[0])
    seeds = [int(match.group(0)) for match in seed_matches]

    # Extracting mappings for each category
    mappings = []
    for section in sections[1:]:
        category_mappings = []
        for line in section.splitlines()[1:]:  # Skip the title line
            # Get all numbers from the line
            nums = [int(num) for num in NUMBER_PATTERN.findall(line)]
            if len(nums) == 3:
                src_start, dest_start, length = nums
                # Add the mapping to the list
                category_mappings.append((dest_start, dest_start + length, src_start - dest_start))
        mappings.append(sorted(category_mappings, key=itemgetter(0)))

    return seeds, mappings

def remap(number_ranges, category_mappings):
    """
    Remaps each range of numbers based on the provided category mappings.

    Args:
    number_ranges (list): List of tuples representing the number ranges.
                          Each tuple is a pair (start, end) of a range.
    category_mappings (list): List of tuples representing the mappings for a category.
                              Each tuple is a mapping (map_start, map_end, offset).

    Returns:
    generator: Yields the remapped number ranges.
    """
    for range_start, range_end in number_ranges:
        for map_start, map_end, offset in category_mappings:
            # Skip non-overlapping ranges
            if map_start >= range_end or range_start >= map_end:
                continue

            # Adjust the range start if it's before the mapping start
            if range_start < map_start:
                yield range_start, map_start
                range_start = map_start

            # Apply the mapping to the overlapping part of the range
            overlap_end = min(range_end, map_end)
            yield range_start + offset, overlap_end + offset

            # Move to the next part of the range
            range_start = overlap_end

        # Yield any remaining part of the range after all mappings are applied
        if range_start < range_end:
            yield range_start, range_end

def find_lowest_location(data, is_part2=False):
    """
    Finds the lowest location number based on the input data.

    Args:
    data (str): Input data string containing seed ranges and category mappings.
    is_part2 (bool): Flag to determine if the function is used for Part 2.
                     In Part 2, the seeds are considered as ranges.

    Returns:
    int: The lowest location number obtained after applying all category mappings.
    """
    # Parse the input data to get seeds and mappings
    seeds, category_mappings = parse_input(data)

    if is_part2:
        # For Part 2, consider each pair of seeds as a range (start, end)
        seed_ranges = []
        # Loop through seeds two at a time
        for i in range(0, len(seeds), 2):
            start = seeds[i]
            length = seeds[i + 1] if i + 1 < len(seeds) else 0
            range_end = start + length
            seed_ranges.append((start, range_end))
    else:
        # For Part 1, each seed is a single number range (start, start + 1)
        seed_ranges = [(seed, seed + 1) for seed in seeds]

    # Apply all category mappings to each seed range
    remapped_ranges = reduce(remap, category_mappings, seed_ranges)

    # Find and return the minimum starting number from the remapped ranges
    return min(map(itemgetter(0), remapped_ranges))



def main():
    # Read the input file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_file = open(dir_path + "/input.txt", "r")
    input_data = input_file.read()

    print("Part 1:", find_lowest_location(input_data))
    print("Part 2:", find_lowest_location(input_data, is_part2=True))


if __name__ == "__main__":
    main()
