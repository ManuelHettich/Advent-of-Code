# !/usr/bin/env python

# --- Day 2: Cube Conundrum ---

import os
import re
import operator
from functools import reduce

SAMPLE_INPUT_1 = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

SAMPLE_INPUT_2 = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""


# Function to find the maximum number of cubes of a specific color in a game
def get_max_color(regex, game):
    matches = re.findall(regex, game)
    return max(int(match) for match in matches) if matches else 0

def main():
    # Read the input file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_file = open(dir_path + "/input.txt", "r")
    input_data = input_file.read()

    # Extract game information using regex
    games_info = re.findall(r"Game (\d+): (.*)", input_data)

    # Process each game to find the maximum number of each color cube shown
    games = {
        int(game_id): (
            get_max_color(r"(\d+) red", game_data),
            get_max_color(r"(\d+) green", game_data),
            get_max_color(r"(\d+) blue", game_data),
        )
        for game_id, game_data in games_info
    }

    # Calculate the sum of IDs for games that are possible with the given cube limits
    possible_game_ids_sum = sum(
        game_id for game_id, (max_red, max_green, max_blue) in games.items()
        if max_red <= 12 and max_green <= 13 and max_blue <= 14
    )

    print("Part 1:", possible_game_ids_sum)

    # Calculate the power of the minimum set of cubes for each game
    powers = [reduce(operator.mul, max_colors) for max_colors in games.values()]

    # Sum the powers to find the total
    total_power = sum(powers)

    print("Part 2:", total_power)



if __name__ == "__main__":
    main()
