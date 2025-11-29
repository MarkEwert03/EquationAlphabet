from src.equations import (
    CompactEquation,
    stringify_equation,
    generate_all_equations,
    verify_solution_set,
    relabel,
)


def test_generate_all_equations_count_small():
    # n=2 -> 2 * 2^3 = 16
    eqs = generate_all_equations(2)
    assert len(eqs) == 16
    # structure sanity
    assert all(isinstance(t, tuple) and len(t) == 4 for t in eqs)


def test_verify_solution_set_simple_add():
    # A + B = C with n=3 has two solutions over permutations of {1,2,3}:
    # A=1,B=2,C=3 and A=2,B=1,C=3
    eqs: list[CompactEquation] = [("A", "+", "B", "C")]
    sols = verify_solution_set(3, eqs)
    assert len(sols) == 2
    assert {"A": 1, "B": 2, "C": 3} in sols
    assert {"A": 2, "B": 1, "C": 3} in sols


def test_stringify_equation():
    eq: CompactEquation = ("A", "*", "B", "C")
    assert stringify_equation(eq) == "A*B=C"


def test_relabel_and_canonicalize():
    # Suppose labels map non-canonically; relabel should reorder operands for +/*
    solution_set = {
        "equations": ["C+A=B", "B*A=C"],
        "labels": {"A": 1, "B": 3, "C": 2},
    }
    out = relabel(solution_set)
    # Equations should be canonical and sorted
    assert out["equations"] == sorted(["A+B=C", "A*B=C"])
    # Labels should map A->1, B->2, C->3
    assert out["labels"] == {"A": 1, "B": 2, "C": 3}
