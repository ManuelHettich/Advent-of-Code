import os
import bisect

SAMPLE_INPUT = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""

def possible_turns(current_direction, steps_taken, min_steps=1, max_steps=3):
    """
    Returns a list of possible turns based on the current direction and steps taken.
    
    Parameters:
    - current_direction (int): The current direction of movement.
    - steps_taken (int): The number of consecutive steps taken in the same direction.
    
    Returns:
    list of int: The possible turns.
    """
    turns = []
    if steps_taken < max_steps:
        # Add the current direction
        turns.append(current_direction)
    if steps_taken >= min_steps:
        # Add the two possible turns
        turns.extend([(current_direction - 1) % 4, (current_direction + 1) % 4])
    return turns

def find_least_heat_loss_path(grid, min_steps, max_steps):
    """
    Finds the path with the least heat loss in a grid, given constraints on movement.

    Parameters:
    - grid (str): Multiline string representation of the grid with heat loss values.
    - min_steps (int): Minimum consecutive steps in the same direction before a turn is required.
    - max_steps (int): Maximum consecutive steps allowed in the same direction.

    Returns:
    int: The minimum heat loss incurred on the optimal path.
    """
    # Convert the string grid into a 2D list of integers
    heat_loss_grid = [[int(cell) for cell in row] for row in grid.splitlines() if row]
    # Initialize the priority queue with the starting position and cost
    priority_queue = [(0, (0, 0, 1, 0))]  # Format: (heat_loss, (y, x, direction, steps))
    # Dictionary to keep track of the best (lowest) heat loss for each state
    best_heat_loss = {(0, 0, 1, 0): 0}

    while priority_queue:
        # Pop the state with the lowest heat loss
        current_heat_loss, (y, x, direction, steps) = priority_queue.pop(0)
        # Check if the goal state has been reached
        if y == len(heat_loss_grid) - 1 and x == len(heat_loss_grid[0]) - 1:
            return current_heat_loss
        # Check if this state has been visited before with a lower heat loss
        if current_heat_loss > best_heat_loss.get((y, x, direction, steps), float("inf")):
            continue
        # Explore next steps
        for new_direction in possible_turns(direction, steps, min_steps, max_steps):
            # Calculate the new state
            new_y, new_x = y, x
            if new_direction == 0:  # Up
                new_y -= 1
            elif new_direction == 1:  # Right
                new_x += 1
            elif new_direction == 2:  # Down
                new_y += 1
            elif new_direction == 3:  # Left
                new_x -= 1

            # Check if the new state is valid
            if not (0 <= new_y < len(heat_loss_grid) and 0 <= new_x < len(heat_loss_grid[new_y])):
                continue
            # Calculate the new heat loss and steps
            new_heat_loss = current_heat_loss + heat_loss_grid[new_y][new_x]
            new_steps = steps + 1 if direction == new_direction else 1
            new_state = (new_y, new_x, new_direction, new_steps)
            # Check if the new state has a lower heat loss
            if new_heat_loss < best_heat_loss.get(new_state, float("inf")):
                # Update the best heat loss for the new state
                best_heat_loss[new_state] = new_heat_loss
                # Add the new state to the priority queue
                bisect.insort(priority_queue, (new_heat_loss, new_state))

    return None

# ------- Part 1 -------

def part1(input_data):
    """
    Finds the least costly path in the grid with constraints on turns.
    
    Parameters:
    - input_data (str): Multiline string representation of the grid.
    
    Returns:
    int: Cost of the least costly path.
    """
    return find_least_heat_loss_path(input_data, min_steps=1, max_steps=3)

# ------- Part 2 -------

def part2(input_data):
    """
    Finds the least costly path in the grid with constraints on turns.
    
    Parameters:
    - input_data (str): Multiline string representation of the grid.
    
    Returns:
    int: Cost of the least costly path.
    """
    return find_least_heat_loss_path(input_data, min_steps=4, max_steps=10)

# Main function

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_file_path = os.path.join(dir_path, "input.txt")
    with open(input_file_path, "r") as input_file:
        input_data = input_file.read()

    print("Part 1:", part1(input_data))
    print("Part 2:", part2(input_data))


if __name__ == "__main__":
    main()
