"""
💬 Plain-English puzzle

In this puzzle you don't write the Python yourself. You tell your AI agent
what the code should do, in precise, plain English, and the agent turns
exactly what you wrote into code. Nothing more. It won't fill in a missing
step, it won't fix a mistake in your logic, and it won't peek at the
docstring to guess what you meant.

Why work like this? Reading and thinking through an algorithm is the real
skill. Syntax is the easy part. If you can state the steps clearly, you
understand the algorithm.

How precise is "precise enough"? One level above single statements. Not
"total plus-equals coef times f of a plus i times h": that is just code
written as words. But also not "implement Simpson's rule": that skips all
the thinking. Say what each step does: "add up f at the interior points,
weighted 4 at odd i and 2 at even i".

Because the agent translates exactly what you wrote, a vague or wrong
description gives wrong code, and the smoke test (run this file) or the
checks on the website will fail. When that happens, read the generated code, find the
place where your description was unclear, and describe a correction.

No agent? Write your description as comments first, then write the code
under each comment.

Part 1 is a worked example (`simpsons_rule`): the description and the code
it produced are both shown. Parts 2 and 3 are yours (`quadratic_formula`
and `softmax`).

This file has no ⭐ CORE parts.

DO NOT MODIFY THE FUNCTION SIGNATURES.
"""

import math
from collections.abc import Callable


# ---------------------------------------------------------------------------
# Part 1: worked example
# ---------------------------------------------------------------------------


def simpsons_rule(f: Callable[[float], float], a: float, b: float, n: int) -> float:
    """
    Approximates the integral of f from a to b with the composite Simpson's
    1/3 rule, using n subintervals. Raises a ValueError if n is not a
    positive even integer.

    https://en.wikipedia.org/wiki/Simpson%27s_rule

    This is the description that produced the code below:

        Check that n is a positive even number, and raise a ValueError saying
        so if it isn't. Let h be the width of one subinterval, (b - a) / n.
        Start a total at f(a) + f(b). Then for each interior point i from 1
        to n - 1, add f(a + i * h) to the total, weighted 4 if i is odd and 2
        if it's even. Return h / 3 times the total.
    """

    # Check that n is a positive even number, and raise a ValueError.
    if n <= 0 or n % 2 != 0:
        raise ValueError("n must be a positive even integer")

    # Let h be the width of one subinterval.
    h = (b - a) / n

    # Start a total at f(a) + f(b).
    total = f(a) + f(b)

    # For each interior point i from 1 to n - 1...
    for i in range(1, n):
        # ...weighted 4 if i is odd and 2 if it's even.
        weight = 4 if i % 2 == 1 else 2
        # ...add f(a + i * h) to the total.
        total += weight * f(a + i * h)

    # Return h / 3 times the total.
    return h / 3 * total


# ---------------------------------------------------------------------------
# Part 2: yours
# ---------------------------------------------------------------------------


def quadratic_formula(a: float, b: float, c: float) -> tuple:
    """
    Finds the real roots of a*x^2 + b*x + c = 0. The number `a` is never 0.

    Return a tuple with the roots in increasing order, smallest first. If
    there are no real roots, return an empty tuple. If there is exactly one
    (the discriminant is exactly 0), return a tuple with just that root.
    """
    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        return ()

    # Write your solution here.
    p2 = math.sqrt(b**2 - 4 * a * c)
    return tuple(sorted(set([(-b + p2) / (2 * a), (-b - p2) / (2 * a)])))


# ---------------------------------------------------------------------------
# Part 3: yours
# ---------------------------------------------------------------------------


def softmax(xs: list[float]) -> list[float]:
    """
    Turns a list of numbers into a list of probabilities. The output has the
    same length as the input, every entry is between 0 and 1, and the entries
    add up to 1 (up to rounding). Entry i is exp(xs[i]) divided by the sum of
    exp(xs[j]) over all j. In exact math every entry is positive, but in
    floats an entry far below the largest input comes out as exactly 0.0:
    softmax([0, -1000]) gives [1.0, 0.0].

    In machine learning, softmax turns a model's raw scores into
    probabilities.

    It must work for inputs as large as 1000. (Hint: adding the same
    constant to every input does not change the output.)

    Raises a ValueError if xs is empty.
    """

    # Write your solution here.
    if len(xs) == 0:
        raise ValueError("expected a nonnegative input, got negative discriminant")

    mx = max(xs)
    new_xs = [math.exp(number - mx) for number in xs]
    new_val = sum(new_xs)
    return [number / new_val for number in new_xs]


if __name__ == "__main__":

    def check(label, get, expected):
        """Print OK if `get()` returns `expected`, NOT YET otherwise."""
        try:
            got = get()
        except Exception as e:
            print(f"NOT YET: {label} (raised {type(e).__name__}: {e})")
            return
        if got == expected:
            print(f"OK: {label}")
        else:
            print(f"NOT YET: {label}\n    expected {expected!r}\n    got      {got!r}")

    def rounded(xs):
        """The numbers in `xs`, rounded to 3 decimals."""
        return [round(x, 3) for x in xs]

    def raised(fn):
        """The name of the exception that `fn()` raises, or "no error"."""
        try:
            fn()
        except Exception as e:
            return type(e).__name__
        return "no error"

    # Smoke test: checks your functions against what their docstrings say.

    # x^2 - 5x + 6 = 0  ->  roots (2.0, 3.0)
    check("quadratic_formula(1, -5, 6) gives (2.0, 3.0)", lambda: quadratic_formula(1, -5, 6), (2.0, 3.0))

    # x^2 + 1 = 0 has no real roots, x^2 - 2x + 1 = 0 has exactly one
    check("quadratic_formula(1, 0, 1) gives ()", lambda: quadratic_formula(1, 0, 1), ())
    check("quadratic_formula(1, -2, 1) gives (1.0,)", lambda: quadratic_formula(1, -2, 1), (1.0,))

    # integral of x^2 from 0 to 1  ->  about 0.3333 (the worked example)
    print("simpsons_rule:", simpsons_rule(lambda x: x**2, 0, 1, 4))

    # about [0.090, 0.245, 0.665]
    check("softmax([1.0, 2.0, 3.0]) is about [0.090, 0.245, 0.665]", lambda: rounded(softmax([1.0, 2.0, 3.0])), [0.09, 0.245, 0.665])

    # about [0.269, 0.731], and no OverflowError
    check("softmax([1000.0, 1001.0]) is about [0.269, 0.731]", lambda: rounded(softmax([1000.0, 1001.0])), [0.269, 0.731])

    check("softmax([]) raises a ValueError", lambda: raised(lambda: softmax([])), "ValueError")
