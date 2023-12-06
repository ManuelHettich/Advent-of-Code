import os

SAMPLE_INPUT = """Time:      7  15   30
Distance:  9  40  200
"""

def calculate_ways_to_win(time, record):
    """
    Calculates the number of ways to win the race by holding the button for different durations.

    Args:
    time (int): Total time allowed for the race.
    record (int): The record distance to beat.

    Returns:
    int: The number of ways to win the race.
    """
    ways_to_win = 0
    for hold_time in range(time + 1):
        move_time = time - hold_time
        distance = hold_time * move_time
        if distance > record:
            ways_to_win += 1

    return ways_to_win

def multiply_ways_to_win(times, dists):
    """
    Multiplies the number of ways to win across all races.

    Args:
    times, dists (list): A list of times and distances of different races.

    Returns:
    int: The product of the number of ways to win for each race.
    """
    product = 1
    for time, record in zip(times, dists):
        product *= calculate_ways_to_win(time, record)

    return product

def calculate_ways_to_win_single_race(time, dist):
    """
    Calculates the number of ways to win the single race.

    Args:
    time, dist (str): The time and distance for a single race.

    Returns:
    int: The number of ways to win the single race.
    """
    return calculate_ways_to_win(time, dist)

def main():
    # Read the input file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_file = open(dir_path + "/input.txt", "r")
    input_data = input_file.readlines()

    times = map(int, input_data[0][9:].split())
    dists = map(int, input_data[1][9:].split())

    print("Part 1:", multiply_ways_to_win(times, dists))


    time = int(input_data[0][9:].replace(" ", ""))
    dist = int(input_data[1][9:].replace(" ", ""))
    print("Part 2:", calculate_ways_to_win_single_race(time, dist))


if __name__ == "__main__":
    main()
