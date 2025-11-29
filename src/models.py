from __future__ import annotations
from typing import Tuple, Dict
import re

# Public alias for simple tuple representation
# (x, op, y, z) where each is a single capital letter or op in {"+", "*"}
CompactEquation = Tuple[str, str, str, str]


class SimpleEquation:
    """
    Represents an equation of the form: var1 op var2 = var3
    where op is '+' or '*', and var1, var2, var3 are intended to be positive integers.

    Notes:
        - Initialization does NOT enforce correctness; use is_valid() or validate().
        - This class is useful for evaluating or checking numeric equations after
          mapping variables to numeric assignments.
    """

    VALID_OPS = {"+", "*"}

    def __init__(self, op: str, var1: int, var2: int, var3: int):
        """
        Create a SimpleEquation. Does not validate correctness automatically.

        Args:
            op: Operator ('+' or '*').
            var1: First operand (int).
            var2: Second operand (int).
            var3: Stated result (int).
        """
        self.op = op
        self.var1 = var1
        self.var2 = var2
        self.var3 = var3

    def evaluate(self) -> int:
        """
        Compute var1 op var2 and return the numerical result.

        Returns:
            int: The evaluated result.
        """
        if self.op == "+":
            return self.var1 + self.var2
        if self.op == "*":
            return self.var1 * self.var2
        raise ValueError(f"Unsupported operator: {self.op}")

    def is_valid(self, require_consistency: bool = True) -> bool:
        """
        Return True if equation fields are valid.

        Args:
            require_consistency: If True, also checks that evaluate() == var3.

        Returns:
            bool: True if valid under the chosen rules.
        """
        if self.op not in self.VALID_OPS:
            return False
        if not all(isinstance(v, int) and v > 0 for v in (self.var1, self.var2, self.var3)):
            return False
        if require_consistency and self.evaluate() != self.var3:
            return False
        return True

    def validate(self, require_consistency: bool = True) -> None:
        """
        Raise ValueError if equation is not valid. Optionally enforce consistency.

        Args:
            require_consistency: If True, also checks that evaluate() == var3.

        Raises:
            ValueError: If operator, types, positivity, or consistency are invalid.
        """
        if self.op not in self.VALID_OPS:
            raise ValueError(f"Operator must be one of {sorted(self.VALID_OPS)}.")
        for name, v in (("var1", self.var1), ("var2", self.var2), ("var3", self.var3)):
            if not (isinstance(v, int) and v > 0):
                raise ValueError(f"{name} must be a positive integer (>0). Got: {v!r}")
        if require_consistency and self.evaluate() != self.var3:
            raise ValueError(
                f"Inconsistent equation: {self.var1} {self.op} {self.var2} = {self.var3} "
                f"(expected {self.evaluate()})."
            )

    # Serialization
    def to_dict(self) -> Dict[str, int | str]:
        """
        Return a dictionary representation of the equation.

        Returns:
            dict: {'op': str, 'var1': int, 'var2': int, 'var3': int}
        """
        return {"op": self.op, "var1": self.var1, "var2": self.var2, "var3": self.var3}

    @classmethod
    def from_dict(cls, data: Dict[str, int | str]) -> "SimpleEquation":
        """
        Create a SimpleEquation from a dictionary.

        Args:
            data: Dict containing 'op', 'var1', 'var2', 'var3'.

        Returns:
            SimpleEquation: The constructed equation.
        """
        return cls(data["op"], data["var1"], data["var2"], data["var3"])

    @classmethod
    def parse(cls, equation_str: str) -> "SimpleEquation":
        """
        Parse a string like '3 + 4 = 7' (whitespace flexible) into a SimpleEquation.

        Args:
            equation_str: The textual equation.

        Returns:
            SimpleEquation: Parsed instance.

        Raises:
            ValueError: If structure or parts are invalid.
        """
        pattern = re.compile(r"^\s*(\d+)\s*([+*])\s*(\d+)\s*=\s*(\d+)\s*$")
        m = pattern.fullmatch(equation_str)
        if not m:
            raise ValueError(
                "Invalid equation format. Expected 'a <op> b = c' with positive integers."
            )
        a_str, op_found, b_str, right = m.groups()
        if any(int(x) <= 0 for x in (a_str, b_str, right)):
            raise ValueError("All numbers must be positive integers (>0).")
        return cls(op_found, int(a_str), int(b_str), int(right))

    def replace(self, **changes) -> "SimpleEquation":
        """
        Return a new equation with specified fields replaced.

        Args:
            **changes: op/var1/var2/var3 overrides.

        Returns:
            SimpleEquation: New instance with changes applied.
        """
        return SimpleEquation(
            op=changes.get("op", self.op),
            var1=changes.get("var1", self.var1),
            var2=changes.get("var2", self.var2),
            var3=changes.get("var3", self.var3),
        )

    def check_answer(self, answer: int) -> bool:
        """
        Return True if answer equals var3 (the stated result).

        Args:
            answer: Proposed result.

        Returns:
            bool: True if equal to var3 and positive.
        """
        return isinstance(answer, int) and answer > 0 and answer == self.var3

    def feedback(self, answer: int) -> str:
        """
        Return feedback string for a given answer.

        Args:
            answer: Proposed result.

        Returns:
            str: 'Correct!' or error/explanation string.
        """
        if not (isinstance(answer, int) and answer > 0):
            return "Answer must be a positive integer."
        return "Correct!" if answer == self.var3 else f"Incorrect. Expected {self.var3}."


def stringify_equation(eq: CompactEquation, sep: str = "") -> str:
    """
    Return a compact string representation like 'A+B=C' for an Equation tuple.

    Args:
        eq: The equation tuple (x, op, y, z).
        sep: Optional separator inserted around operator and '='.

    Returns:
        str: Compact string, e.g., 'A+B=C' or 'A + B = C' if sep=' '.
    """
    var1, op, var2, res = eq
    return f"{var1}{sep}{op}{sep}{var2}{sep}={sep}{res}"


# Backward-compatibility alias (original camelCase)
stringifyEquation = stringify_equation
