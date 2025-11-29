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
        
    Examples:
    >>> generate_all_equations(0)
    []
    >>> generate_all_equations(1)
    [('A', '+', 'A', 'A'), ('A', '*', 'A', 'A')]
    >>> generate_all_equations(2)
    [
        ('A', '+', 'A', 'A'), ('A', '*', 'A', 'A'),
        ('A', '+', 'A', 'B'), ('A', '*', 'A', 'B'),
        ('A', '+', 'B', 'A'), ('A', '*', 'B', 'A'),
        ('A', '+', 'B', 'B'), ('A', '*', 'B', 'B'),
        ('B', '+', 'A', 'A'), ('B', '*', 'A', 'A'),
        ('B', '+', 'A', 'B'), ('B', '*', 'A', 'B'),
        ('B', '+', 'B', 'A'), ('B', '*', 'B', 'A'),
        ('B', '+', 'B', 'B'), ('B', '*', 'B', 'B')
    ]
    >>> len(generate_all_equations(2))
    16
    """
    if not 1 <= n <= 26:
        return []

    symbols = [chr(ord("A") + i) for i in range(n)]
    ops = ["+", "*"]
    result: List[CompactEquation] = []
    for x, y, z in product(symbols, symbols, symbols):
        for op in ops:
            result.append((op, x, y, z))
    return result
