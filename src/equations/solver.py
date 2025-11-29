from __future__ import annotations

import re
import string
from collections import Counter
from itertools import permutations, combinations
from typing import Dict, List

from .models import CompactEquation, stringify_equation, SimpleEquation
from .generate import generate_all_equations


def verify_solution_set(n: int, equations: List[CompactEquation]) -> List[Dict[str, int]]:
    """
    Finds all valid solutions for a given number of variables and a set of equations.

    This function exhaustively checks every possible unique assignment of integers
    from 1 to n against the provided list of simple equations.

    Args:
        n (int):
            The number of variables (and the range of integer values).
        equations (List[Equation]):
            A list of encoded equations to verify.
            Example: [('A', '+', 'C', 'D'), ('B', '*', 'C', 'F')]

    Returns:
        A list of all valid solution assignments. Each solution is a dictionary
        mapping variable names to their integer values.
    """
    if n < 1 or n > 26:
        raise ValueError("n must be between 1 and 26.")

    variables = [chr(ord("A") + i) for i in range(n)]
    values = list(range(1, n + 1))

    valid_solutions: List[Dict[str, int]] = []

    # Generate all possible unique assignments of values to variables (n! permutations)
    for p in permutations(values):
        assignment = {var: val for var, val in zip(variables, p)}

        is_valid_assignment = True
        # Check if the current assignment satisfies ALL equations
        for eq in equations:
            var1_name, op, var2_name, res_name = eq

            val1 = assignment[var1_name]
            val2 = assignment[var2_name]
            res_val = assignment[res_name]

            # Use SimpleEquation for clarity/consistency (no auto-validation)
            se = SimpleEquation(op=op, var1=val1, var2=val2, var3=res_val)
            if se.evaluate() != res_val:
                is_valid_assignment = False
                break

        if is_valid_assignment:
            valid_solutions.append(assignment)

    return valid_solutions


def generate_all_solutions(n: int, num_eqs_to_use: int):
    """
    Enumerate all equation bundles of a given size and find their solution sets.

    Args:
        n: Number of variables (also max integer value).
        num_eqs_to_use: The bundle size (number of equations per bundle).

    Returns:
        (solution_counter, unique_solution_options) where:
          - solution_counter: Counter keyed by number of solutions -> count of bundles
          - unique_solution_options: List of dicts with:
                { "equations": List[str], "labels": Dict[str, int] }
            for bundles that have exactly one solution.
    """
    my_equations = generate_all_equations(n)
    equation_bundles = list(combinations(my_equations, num_eqs_to_use))

    solution_counter: Counter[int] = Counter()
    unique_solution_options: List[Dict[str, object]] = []

    for eq_bundle in equation_bundles:
        solutions = verify_solution_set(n=n, equations=list(eq_bundle))
        solution_counter[len(solutions)] += 1
        if len(solutions) == 1:
            presented_solution = {
                "equations": [stringify_equation(eq) for eq in eq_bundle],
                "labels": solutions[0],
            }
            unique_solution_options.append(presented_solution)

    return solution_counter, unique_solution_options


def relabel(solution_set: Dict[str, object]) -> Dict[str, object]:
    """
    Relabels equations and a solution set based on the sorted values of the solutions.

    Args:
        solution_set: A dict containing:
            equations: A list of strings, where each string is an equation "A+B=C".
            labels: A dictionary mapping uppercase letters to integer values.

    Returns:
        dict: A dictionary containing the relabeled and sorted "equations" and the new "labels".
    """
    equations: List[str] = solution_set["equations"]  # e.g., ["A+B=C", "B*A=C"]
    labels: Dict[str, int] = solution_set["labels"]

    # Create a mapping from old letters to new letters based on sorted values.
    sorted_old_labels = sorted(labels.keys(), key=lambda k: labels[k])

    # Generate new labels ('A', 'B', 'C', ...)
    new_labels_alpha = list(string.ascii_uppercase[: len(sorted_old_labels)])

    # Create the mapping from old letter to new letter
    relabel_map = dict(zip(sorted_old_labels, new_labels_alpha))
    translation_table = str.maketrans(relabel_map)

    # Relabel the equations using the map and canonicalize commutative operands
    relabeled_equations: List[str] = []
    for eq in equations:
        # Apply the letter relabeling
        relabeled_eq = eq.translate(translation_table)

        # Canonicalize for commutative operations
        # Split 'A+B=C' into ('A', '+', 'B', 'C')
        parts = re.split(r"([+*])", relabeled_eq)
        left1 = parts[0]
        op = parts[1]
        left2, result = parts[2].split("=")

        if op in ("+", "*") and left1 > left2:
            left1, left2 = left2, left1  # Swap operands so left1 <= left2

        canonical_eq = f"{left1}{op}{left2}={result}"
        relabeled_equations.append(canonical_eq)

    # Sort the final list of canonical equations alphabetically
    relabeled_equations.sort()

    # Create the new simplified labels dictionary {'A': 1, 'B': 2, ...}
    new_labels_dict = {new_label: i + 1 for i, new_label in enumerate(new_labels_alpha)}

    return {"equations": relabeled_equations, "labels": new_labels_dict}
