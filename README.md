# EquationAlphabet

An exploratory mathematical analysis for investigating constraint satisfaction problems involving **triplet equations**. These are equations where letters must map to distinct integers under addition and multiplication constraints.

## Overview

This project provides a comprehensive framework for generating, verifying, and analyzing systems of $m$ equations of the form:

$$X \oplus Y = Z$$

where:
- $X$, $Y$, and $Z$ are variables represented by distinct capital letters (A, B, C, ...)
- $\oplus \in \{+, \times\}$ (addition or multiplication)
- Each variable must be assigned a unique integer from $\{1, 2, ..., n\}$ for a system with $n$ variables

### The Triplet Equation Problem

Given a set of $n$ variables, some research questions we want to answer is:
1. **Solution Space**: For a given set of equations, how many valid assignments exist?
2. **Uniqueness**: Which equation bundles have exactly one solution?
