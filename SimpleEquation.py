from __future__ import annotations
import re


class SimpleEquation:
    """
    Represents a 'simple equation' of the form: `var1 <op> var2 ?= var3`

    Attributes:
      op (str): The operator performed on var1 and var2. It is in `{'+', '*'}`.
      var1 (int): The first positive integer in the equation.
      var2 (int): The second positive integer in the equation.
      var3 (int): The third positive integer in the equation. Note this is not necessarily chosen to make the equation true.
    """

    VALID_OPS = {"+", "*"}
    op: str
    var1: int
    var2: int
    var3: int

    def __init__(self, op: str, var1: int, var2: int, var3: int):
        self.op = op
        self.var1 = var1
        self.var2 = var2
        self.var3 = var3

    # Core Functionality
    def evaluate(self) -> int:
        """
        Compute var1 op var2 and return the numerical result.
        """
        if self.op == "+":
            return self.var1 + self.var2
        elif self.op == "*":
            return self.var1 * self.var2
        else:
            raise ValueError(f"Unsupported operator: {self.op}")

    def is_valid(self, require_consistency: bool = True) -> bool:
        """
        Return True if equation fields are valid.
        If require_consistency is True, also checks that evaluate() == var3.
        """
        if self.op not in self.VALID_OPS:
            return False
        if not all(isinstance(v, int) and v > 0 for v in [self.var1, self.var2, self.var3]):
            return False
        if require_consistency and self.evaluate() != self.var3:
            return False
        return True

    def validate(self, require_consistency: bool = True) -> None:
        """
        Raise ValueError if equation is not valid. Optionally enforce consistency.
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
    def to_dict(self) -> dict:
        """
        Return a dictionary representation of the equation.
        """
        return {"op": self.op, "var1": self.var1, "var2": self.var2, "var3": self.var3}

    @classmethod
    def from_dict(cls, data: dict) -> "SimpleEquation":
        """
        Create a SimpleEquation from a dictionary.
        """
        return cls(data["op"], data["var1"], data["var2"], data["var3"])

    # Parsing
    @classmethod
    def parse(cls, equation_str: str) -> "SimpleEquation":
        """
        Parse a string like '3 + 4 = 7' (whitespace flexible) into a SimpleEquation using regex.
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

    # Checking answers
    def is_sound(self) -> bool:
        """
        Return True if: `var1 <op> var2 == var3`
        """
        return self.evaluate() == self.var3

    # Comparison
    def equivalent(self, other: "SimpleEquation") -> bool:
        """
        Return True if equations express the same relation (commutative for + and *).
        """
        if self.op != other.op:
            return False
        if self.var3 != other.var3:
            return False
        # For + or *, order of operands does not matter
        return {self.var1, self.var2} == {other.var1, other.var2}

    # Dunder methods
    def __str__(self) -> str:
        """
        Return a human-readable string representation.
        """
        eq_symbol = "=" if self.is_sound() else "≠"
        return f"{self.var1} {self.op} {self.var2} {eq_symbol} {self.var3}"

    def __repr__(self) -> str:
        """
        Return a detailed representation for debugging.
        """
        return (
            f"SimpleEquation(op={self.op!r}, var1={self.var1}, var2={self.var2}, var3={self.var3})"
        )
