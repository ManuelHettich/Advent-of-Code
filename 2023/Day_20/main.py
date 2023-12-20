import os
from collections import deque
from itertools import count
from math import lcm

def parse_input(input_data):
    """
    Parse the input data to construct the network, flip_flops, and conjunctions.

    Args:
    - input_data: A string containing the input data.

    Returns:
    A tuple containing the network, flip_flops, and conjunctions dictionaries.
    """
    # Initialize dictionaries to store the network structure and states
    flip_flops = {}
    conjunctions = {}
    network = {}

    # Process each line of the input
    lines = input_data.strip().split("\n")
    for line in lines:
        # Split each line into source and destinations
        source, destinations = line.split("->")
        source = source.strip()
        destinations = list(map(str.strip, destinations.split(",")))

        # Determine the type of the source and update the respective dictionary
        if source[0] == "%":
            source = source[1:]
            flip_flops[source] = False
        elif source[0] == "&":
            source = source[1:]
            conjunctions[source] = {}

        # Update the network graph
        network[source] = destinations

    # Set up the initial state for conjunctions
    for source, destinations in network.items():
        for dest in filter(conjunctions.__contains__, destinations):
            conjunctions[dest][source] = False

    return network, flip_flops, conjunctions

def transmit_signal(network, flip_flops, conjunctions, sender, receiver, signal):
    """
    Transmit a signal through the network, updating flip-flops and conjunctions.

    Args:
    - network: The network graph.
    - flip_flops: A dictionary of flip-flop states.
    - conjunctions: A dictionary of conjunction states.
    - sender: The module sending the signal.
    - receiver: The module receiving the signal.
    - signal: The signal being transmitted.

    Yields:
    A tuple containing the sender, receiver, and signal for the next transmission.
    """
    # Process the received signal and update the network state accordingly
    if receiver in flip_flops:
        if signal:
            return
        next_signal = flip_flops[receiver] = not flip_flops[receiver]
    elif receiver in conjunctions:
        conjunctions[receiver][sender] = signal
        next_signal = not all(conjunctions[receiver].values())
    elif receiver in network:
        next_signal = signal
    else:
        return

    # Propagate the signal to the next nodes in the network
    for next_receiver in network[receiver]:
        yield receiver, next_receiver, next_signal

def simulate_network(network, flip_flops, conjunctions):
    """
    Simulate the signal propagation in the network.

    Args:
    - network: The network graph.
    - flip_flops: A dictionary of flip-flop states.
    - conjunctions: A dictionary of conjunction states.

    Returns:
    A tuple containing the low and high signal counts.
    """
    # Initialize the queue with the starting point of the simulation
    queue = deque([("button", "broadcaster", False)])
    low_signal_count = high_signal_count = 0

    # Process the queue until it's empty
    while queue:
        sender, receiver, signal = queue.popleft()
        high_signal_count += signal
        low_signal_count += not signal
        # Extend the queue with new signals to be processed
        queue.extend(transmit_signal(network, flip_flops, conjunctions, sender, receiver, signal))

    return low_signal_count, high_signal_count

def detect_cycles(network, flip_flops, conjunctions):
    """
    Detect cycles in the network signal propagation.

    Args:
    - network: The network graph.
    - flip_flops: A dictionary of flip-flop states.
    - conjunctions: A dictionary of conjunction states.

    Yields:
    The iteration number at which the cycle was detected.
    """
    # Identify receivers relevant for cycle detection
    relevant_receivers = set()
    for rx_source, destinations in network.items():
        if destinations == ["rx"]:
            assert rx_source in conjunctions
            break

    for source, destinations in network.items():
        if rx_source in destinations:
            assert source in conjunctions
            relevant_receivers.add(source)

    # Iterate over the network to detect cycles
    for iteration in count(1):
        queue = deque([("button", "broadcaster", False)])

        while queue:
            sender, receiver, signal = queue.popleft()

            if not signal:
                if receiver in relevant_receivers:
                    yield iteration

                    relevant_receivers.discard(receiver)
                    if not relevant_receivers:
                        return

            queue.extend(transmit_signal(network, flip_flops, conjunctions, sender, receiver, signal))


def part1(network, flip_flops, conjunctions):
    """
    Calculate the result for Part 1 of the challenge.

    Args:
    - network: The network graph.
    - flip_flops: A dictionary of flip-flop states.
    - conjunctions: A dictionary of conjunction states.

    Returns:
    The product of the total low and high signal counts.
    """
    # Simulate the network and calculate the total signal counts
    total_high_signal = total_low_signal = 0
    for _ in range(1000):
        high_signal, low_signal = simulate_network(network, flip_flops, conjunctions)
        total_high_signal += high_signal
        total_low_signal += low_signal
    return total_low_signal * total_high_signal

def part2(network, flip_flops, conjunctions):
    """
    Calculate the result for Part 2 of the challenge.

    Args:
    - network: The network graph.
    - flip_flops: A dictionary of flip-flop states.
    - conjunctions: A dictionary of conjunction states.

    Returns:
    The least common multiple of the cycle detection iterations.
    """
    # Detect cycles in the network and calculate their least common multiple
    return lcm(*detect_cycles(network, flip_flops, conjunctions))

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_file_path = os.path.join(dir_path, "input.txt")

    with open(input_file_path, "r") as input_file:
        input_data = input_file.read()

    network, flip_flops, conjunctions = parse_input(input_data)
    print("Part 1:", part1(network, flip_flops, conjunctions))
    print("Part 2:", part2(network, flip_flops, conjunctions))

if __name__ == "__main__":
    main()
