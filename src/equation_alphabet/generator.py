from __future__ import annotations

from itertools import product, combinations
from typing import List

from .models import CompactEquation


def generate_all_equations(n: int) -> List[CompactEquation]:
    """
    Generate ALL possible simple equations using n variable symbols.
    A 'simple equation' is x op y = z where x,y,z are any of the n symbols (reuse allowed),
    and op in {'+','*'}.

    Total count = 2 * n^3 (if n >= 1).

    Args:
        n: number of distinct symbols (1..26). Symbols map as: 0->'A', 1->'B', ...

    Returns:
        List of 4-tuples: (x, op, y, z)
    """
    if not 1 <= n <= 26:
        return []

    symbols = [chr(ord("A") + i) for i in range(n)]
    ops = ["+", "*"]
    result: List[CompactEquation] = []
    for x, y, z in product(symbols, symbols, symbols):
        for op in ops:
            result.append((x, op, y, z))
    return result


def generate_representative_equations(n: int) -> List[CompactEquation]:
    """
    Generate a reduced representative set of equations across 3-symbol subsets.

    For n < 3: emits a small hand-picked set for coverage.
    For n >= 3: for each 3-variable subset (x,y,z), emits 8 forms:
        (x op x = x), (x op x = y), (x op y = x), (x op y = z)
    for both '+' and '*'.

    NOTE: This does NOT generate all 2*n^3 equations; it is a compressed sample.

    Args:
        n: number of distinct symbols (1..26).

    Returns:
        List of 4-tuples: (x, op, y, z)
    """
    if not 1 <= n <= 26:
        return []

    if n < 3:
        forms: List[CompactEquation] = [("A", "+", "A", "A"), ("A", "*", "A", "A")]
        if n == 2:
            forms.extend(
                [
                    ("A", "+", "A", "B"),
                    ("A", "*", "A", "B"),
                    ("A", "+", "B", "A"),
                    ("A", "*", "B", "A"),
                ]
            )
        return forms

    all_variables = [chr(ord("A") + i) for i in range(n)]
    final_equations: List[CompactEquation] = []

    for subset in combinations(all_variables, 3):
        x, y, z = subset
        forms_for_subset: List[CompactEquation] = [
            (x, "+", x, x),
            (x, "*", x, x),
            (x, "+", x, y),
            (x, "*", x, y),
            (x, "+", y, x),
            (x, "*", y, x),
            (x, "+", y, z),
            (x, "*", y, z),
        ]
        final_equations.extend(forms_for_subset)
    return final_equations
