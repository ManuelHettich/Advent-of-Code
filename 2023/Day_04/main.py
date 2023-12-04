# !/usr/bin/env python

# --- Day 4: Scratchcards ---

import os


SAMPLE_INPUT = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""

# --- Part One ---

def parse_scratchcard_matches(data):
    """
    Parses the scratchcard data and yields the number of matching numbers for each card.

    Args:
    data (str): Multiline string representing scratchcard data.

    Yields:
    int: The number of matching numbers for each scratchcard.
    """
    for line in data.splitlines():
        if not line:
            continue
        # Extract the part of the line after the colon
        line = line[line.index(":") + 1 :]
        winning_numbers, player_numbers = line.split("|")

        # Convert number strings to sets for comparison
        winning_numbers_set = set(winning_numbers.split())
        player_numbers_set = set(player_numbers.split())

        # Yield the number of matching numbers
        yield len(winning_numbers_set & player_numbers_set)

def calculate_total_points(data):
    """
    Calculates the total points for all scratchcards based on the number of matching numbers.

    Args:
    data (str): Multiline string representing scratchcard data.

    Returns:
    int: The total points of all scratchcards.
    """
    total_points = 0

    # Iterate through each card's number of matches
    for match_counts in parse_scratchcard_matches(data):
        # For each card, calculate points: 1 point for first match, doubled for each subsequent match
        if match_counts > 0:
            card_points = 2 ** (match_counts - 1)  # Calculate points as 2^(match_counts - 1)
        else:
            card_points = 0

        # Add the points for this card to the total points
        total_points += card_points

    return total_points

def calculate_total_scratchcards(data):
    """
    Calculates the total number of scratchcards won, including copies of subsequent cards.

    Args:
    data (str): Multiline string representing scratchcard data.

    Returns:
    int: The total number of scratchcards, including originals and copies.
    """
    # List of the number of matches for each card
    match_counts = list(parse_scratchcard_matches(data))
    total_cards = [1 for _ in match_counts]  # Initial count of 1 for each original card

    # Add copies of subsequent cards based on the number of matches
    for idx, match_count in enumerate(match_counts):
        for counter in range(match_count):
            if idx + counter + 1 < len(total_cards):
                total_cards[idx + counter + 1] += total_cards[idx]

    return sum(total_cards)


def main():
    # Read the input file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_file = open(dir_path + "/input.txt", "r")
    input_data = input_file.read()

    # Calculate the sum of part numbers and total gear ratios
    print("Part 1:", calculate_total_points(input_data))
    print("Part 2:", calculate_total_scratchcards(input_data))


if __name__ == "__main__":
    main()
