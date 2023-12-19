from math import prod
import os


SAMPLE_INPUT = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""

def parse_data(input_data):
    """
    Parses the input data into workflows and parts.

    Parameters:
    - input_data (str): Multiline string representing the puzzle input.

    Returns:
    Tuple containing a dictionary of workflows and a list of parts.
    """
    def parse_rules(data):
        """
        Parses the rules for each workflow.
        """
        for line in data.splitlines():
            # Skip empty lines and lines without a workflow name
            if "{" not in line or not line.endswith("}"):
                continue
            # Parse the workflow name and rules
            workflow_name = line[:line.index("{")]
            rules = [
                (rule.split(":")[1], (rule[0], rule[1], int(rule[2:rule.index(":")])))
                if ":" in rule else (rule, None)
                for rule in line[line.index("{") + 1 : -1].split(",")
            ]
            yield workflow_name, rules

    def parse_points(data):
        """
        Parses the rating points for each part.
        """
        for line in data.splitlines():
            # Skip empty lines and lines without a part
            if not line.startswith("{") or not line.endswith("}"):
                continue
            # Parse the ratings
            part_ratings = {kv[0]: int(kv[2:]) for kv in line[1:-1].split(",") if kv[1] == "="}
            yield part_ratings

    # Split the input data into rules and parts
    rules, parts_data = input_data.split("\n\n", maxsplit=1)
    # Parse the rules and parts
    workflows = dict(parse_rules(rules))
    parts = list(parse_points(parts_data))
    return workflows, parts

def evaluate_part(part, workflows):
    """
    Evaluates a part through the workflows.

    Parameters:
    - part (dict): A dictionary representing the part's ratings.
    - workflows (dict): A dictionary of workflows.

    Returns:
    bool: True if the part is accepted, False otherwise.
    """

    # Start at the "in" workflow
    name = "in"

    while name in workflows:
        # Evaluate the part through the workflow
        for next_name, condition in workflows[name]:
            if not condition:
                name = next_name
                break
            key, compare, value = condition
            if (
                compare == "<" and part[key] < value
                or compare == ">" and part[key] > value
            ):
                name = next_name
                break
        else:
            raise RuntimeError("Workflow rule not found.")

        # Check if the part is accepted
        if name == "A":
            return True
        elif name == "R":
            return False

    return False

def part1(input_data):
    """
    Solves part 1 of the puzzle.

    Parameters:
    - input_data (str): Multiline string representing the puzzle input.

    Returns:
    int: Sum of the ratings for all parts that are accepted.
    """
    workflows, parts = parse_data(input_data)
    
    # Evaluate each part through the workflows
    total = 0
    for part in parts:
        if evaluate_part(part, workflows):
            total += sum(part.values())  # Sum up the ratings
    return total

# ------- Part 2 -------

def part2(input_data):
    """
    Solves part 2 of the puzzle.

    Parameters:
    - input_data (str): Multiline string representing the puzzle input.

    Returns:
    int: The number of distinct combinations of ratings that will be accepted.
    """
    # Parse the input data
    workflows, _ = parse_data(input_data)

    def evaluate_combinations(workflow_name, bounds):
        """
        Recursively evaluates combinations of ratings through the workflows.

        Parameters:
        - workflow_name (str): The current workflow to evaluate.
        - bounds (dict): The current bounds for each rating category.

        Returns:
        int: The number of combinations that lead to acceptance in the current state.
        """
        if any(lower_bound > upper_bound for lower_bound, upper_bound in bounds.values()):
            return 0  # No valid combinations in this branch

        if workflow_name == "A":
            return prod(upper_bound - lower_bound + 1 for lower_bound, upper_bound in bounds.values())

        if workflow_name not in workflows:
            return 0  # Workflow not found, no valid combinations

        total = 0
        # Evaluate the part through the workflow
        for next_name, condition in workflows[workflow_name]:
            # Evaluate the next workflow
            if not condition:
                total += evaluate_combinations(next_name, bounds)
                break
            # Evaluate the next workflow with a new bound
            key, compare, value = condition
            low, high = bounds[key]
            # Check if the new bound is valid
            if compare == "<":
                new_bounds = bounds.copy()
                new_bounds[key] = (low, min(high, value - 1))
                total += evaluate_combinations(next_name, new_bounds)
                bounds[key] = (value, high)
            elif compare == ">":
                new_bounds = bounds.copy()
                new_bounds[key] = (max(low, value + 1), high)
                total += evaluate_combinations(next_name, new_bounds)
                bounds[key] = (low, min(high, value))
        return total

    initial_bounds = {k: (1, 4000) for k in "xmas"}
    return evaluate_combinations("in", initial_bounds)

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
