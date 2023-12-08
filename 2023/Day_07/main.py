import os
from collections import Counter

SAMPLE_INPUT = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""


def calculate_hand_rank(hand: tuple[int]) -> int:
    """
    Calculate the rank of a hand in Camel Cards.

    Args:
    hand (tuple[int]): A tuple representing the hand, with cards encoded as integers.

    Returns:
    int: The rank of the hand.
    """
    # Count occurrences of each card, excluding jokers.
    card_counts = Counter(card for card in hand if card >= 0).most_common(2)
    highest_count = card_counts[0][1] if card_counts else 0
    second_highest_count = card_counts[1][1] if len(card_counts) > 1 else 0
    joker_count = sum(card < 0 for card in hand)

    # Determine the rank based on counts and jokers.
    if highest_count + joker_count >= 5:
        return 6
    if highest_count + joker_count >= 4:
        return 5
    if highest_count + second_highest_count + joker_count >= 5:
        return 4
    if highest_count + joker_count >= 3:
        return 3
    if highest_count + second_highest_count + joker_count >= 4:
        return 2
    if highest_count + joker_count >= 2:
        return 1
    return 0

def compute_total_winnings(data: str, part_2: bool = False) -> int:
    """
    Compute the total winnings from the Camel Card hands.

    Args:
    data (str): String data representing hands and bids.
    card_order (str): String representing the order of cards.

    Returns:
    int: Total winnings calculated.
    """
    card_order = "23456789TQKA" if part_2 else "23456789TJQKA"

    # Process each line in the data to calculate the hand rank and bid.
    hands = [
        (calculate_hand_rank(hand := tuple(map(card_order.find, words[0]))), hand, int(words[1]))
        for line in data.splitlines()
        if len(words := line.split(maxsplit=1)) == 2
    ]
    # Calculate the total winnings.
    return sum((i + 1) * bid for i, (_, _, bid) in enumerate(sorted(hands)))

def main():
    # Read the input file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_file_path = os.path.join(dir_path, "input.txt")
    with open(input_file_path, "r") as input_file:
        input_data = input_file.read()

    # Calculate and display total winnings for both parts
    print("Part 1:", compute_total_winnings(input_data))
    print("Part 2:", compute_total_winnings(input_data, part_2=True))

if __name__ == "__main__":
    main()
