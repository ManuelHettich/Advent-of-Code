import os


SAMPLE_INPUT = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

# ------- Part 1 -------

def parse_input(input_data):
    """
    Parse the puzzle input into a more manageable format.

    Parameters:
    - input_data (list of str): The puzzle input as a string.

    Returns:
    list of str: A list of strings representing the steps.
    """
    return input_data.split(",")

def hash_algorithm(step):
    """
    Hashes a step into a number.

    Parameters:
    - step (str): The step to hash.

    Returns:
    int: The hashed step.
    """
    # Start with a current value of 0.
    # For each character, increase the current value by its ASCII code, then multiply by 17, and finally take the remainder when divided by 256.

    current_value = 0
    for char in step:
        current_value = (current_value + ord(char)) * 17 % 256
    return current_value
    
def part1(input_data):
    """
    Solve for the answer to part 1.

    Parameters:
    - input_data (list of str): The puzzle input as a string, representing the steps.

    Returns:
    int: The answer to part 1.
    """
    steps = parse_input(input_data)
    return sum(hash_algorithm(step) for step in steps)

# ------- Part 2 -------

def add_lens(boxes, box_number, label, focal_length):
    """
    Adds or replaces a lens in the specified box.

    Parameters:
    - boxes (dict): The state of all boxes.
    - box_number (int): The box number where the lens is to be added.
    - label (str): The label of the lens.
    - focal_length (int): The focal length of the lens.
    """
    # Ensure the box exists in the boxes dictionary.
    if box_number not in boxes:
        boxes[box_number] = []

    # Check if a lens with the same label already exists.
    for i, lens in enumerate(boxes[box_number]):
        if lens["label"] == label:
            # Replace the old lens with the new lens.
            boxes[box_number][i] = {"label": label, "focal_length": focal_length}
            return

    # If the lens doesn"t exist, add it to the end of the box.
    boxes[box_number].append({"label": label, "focal_length": focal_length})


def remove_lens(boxes, box_number, label):
    """
    Removes a lens from the specified box.

    Parameters:
    - boxes (dict): The state of all boxes.
    - box_number (int): The box number from which the lens is to be removed.
    - label (str): The label of the lens to be removed.
    """
    if box_number in boxes:
        boxes[box_number] = [lens for lens in boxes[box_number] if lens["label"] != label]


def calculate_focusing_power(boxes):
    """
    Calculates the total focusing power of the lenses.

    Parameters:
    - boxes (dict): The state of all boxes.

    Returns:
    int: The total focusing power.
    """
    total_power = 0
    for box_number, lenses in boxes.items():
        for slot, lens in enumerate(lenses, start=1):
            power = (1 + box_number) * slot * lens["focal_length"]
            total_power += power
    return total_power


def part2(input_data):
    """
    Solve for the answer to part 2.

    Parameters:
    - input_data (str): The puzzle input as a string, representing the steps.

    Returns:
    int: The answer to part 2.
    """
    steps = parse_input(input_data)
    boxes = {}

    for step in steps:
        # Split the label and the operation
        if "=" in step:
            label, focal_length = step.split("=")
            operation = "="
        else:
            label = step[:-1]
            operation = "-"
            focal_length = None

        box_number = hash_algorithm(label)

        if operation == "=":
            add_lens(boxes, box_number, label, int(focal_length))
        elif operation == "-":
            remove_lens(boxes, box_number, label)

    return calculate_focusing_power(boxes)

# Main Execution

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_file_path = os.path.join(dir_path, "input.txt")
    with open(input_file_path, "r") as input_file:
        input_data = input_file.read()

    print("Part 1:", part1(input_data))
    print("Part 2:", part2(input_data))


if __name__ == "__main__":
    main()
