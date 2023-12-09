import os

# Example input data for testing purposes
SAMPLE_INPUT_1 = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""

# -------- Part 1 --------

def generate_difference_sequence(values):
    """
    Generate a sequence of differences between adjacent values in a list.

    Args:
    values (list): A list of integers.

    Returns:
    list: A list of differences between consecutive integers in the input list.
    """
    return [values[i+1] - values[i] for i in range(len(values) - 1)]

def extrapolate_next_value(history):
    """
    Extrapolate the next value in a sequence based on its history.

    Args:
    history (list): A list of integers representing the history of values.

    Returns:
    int: The extrapolated next value in the sequence.
    """
    # Start with the original history
    sequences = [history]

    # Generate sequences of differences until all differences are zero
    while sequences[-1] != [0] * len(sequences[-1]):
        sequences.append(generate_difference_sequence(sequences[-1]))

    # Work backwards to extrapolate the next value
    for i in range(len(sequences) - 2, -1, -1):
        next_value = sequences[i][-1] + sequences[i+1][-1]
        sequences[i].append(next_value)

    return sequences[0][-1]

def sum_extrapolated_values(input_data):
    """
    Calculate the sum of the extrapolated next values for each history.

    Args:
    input_data (str): A string containing multiple lines, each representing a history.

    Returns:
    int: The sum of extrapolated next values for each history.
    """
    histories = [list(map(int, line.split())) for line in input_data.strip().split("\n")]
    return sum(extrapolate_next_value(history) for history in histories)

# -------- Part 2 --------

def extrapolate_previous_value(history):
    """
    Extrapolate the previous value in a sequence based on its history.

    Args:
    history (list): A list of integers representing the history of values.

    Returns:
    int: The extrapolated previous value in the sequence.
    """
    # Start with the original history
    sequences = [history]

    # Generate sequences of differences until all differences are zero
    while sequences[-1] != [0] * len(sequences[-1]):
        sequences.append(generate_difference_sequence(sequences[-1]))

    # Add a zero at the beginning of the sequence of zeroes
    sequences[-1].insert(0, 0)

    # Work upwards to extrapolate the previous value
    for i in range(len(sequences) - 2, -1, -1):
        prev_value = sequences[i][0] - sequences[i+1][0]
        sequences[i].insert(0, prev_value)

    return sequences[0][0]

def sum_extrapolated_previous_values(input_data):
    """
    Calculate the sum of the extrapolated previous values for each history.

    Args:
    input_data (str): A string containing multiple lines, each representing a history.

    Returns:
    int: The sum of extrapolated previous values for each history.
    """
    histories = [list(map(int, line.split())) for line in input_data.strip().split("\n")]
    return sum(extrapolate_previous_value(history) for history in histories)


# Main function

def main():
    """
    Main function to execute parts 1 and 2 of the puzzle.
    """
    # Read the input file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_file_path = os.path.join(dir_path, "input.txt")
    with open(input_file_path, "r") as input_file:
        input_data = input_file.read()

    # Execute Part 1
    print("Part 1:", sum_extrapolated_values(input_data))

    # Execute Part 2
    print("Part 2:", sum_extrapolated_previous_values(input_data))

if __name__ == "__main__":
    main()
