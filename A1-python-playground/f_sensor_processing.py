"""
Sensor Readings

A sensor sends a stream of noisy numbers. Before a model can use them, you
clean them up step by step. In this file you build the cleaning steps from
small reusable functions. The main idea: in Python, a function is a value.
You can store it in a list, pass it to another function, and return it from
a function.

The parts, in order:

1. `compose` joins functions into one. Finished example, then a question.
2. You write `pipeline`, which runs a list of steps one after the other.
3. You write `make_clipper`, which builds a new function.
4. Questions about scopes: which variable does a function see? This covers
   closures, lambdas in a loop, assigning to a variable from an outer
   scope, and a variable with the same name in two places.
5. Questions about what Python checks, and when.

Answer the questions by setting the answer variables (they start out as
`None`). You may run code to check your answers.

⭐ CORE: Q1, Q5b and Q5c.

DO NOT MODIFY THE FUNCTION SIGNATURES.
"""

import random


# ---------------------------------------------------------------------------
# 1. compose (finished example)
# ---------------------------------------------------------------------------


def compose(*fns):
    """
    Returns a function that applies `fns` from right to left, so
    `compose(f, g)(x)` is `f(g(x))`.

    A function is a value: you can pass it to another function and return it
    from one. Here `composed` is created inside `compose` and returned.
    It still remembers `fns` after `compose` has finished. A function that
    remembers variables from the place where it was made is a closure.

    Example:
        >>> compose(str, abs)(-3)
        '3'
    """

    def composed(x):
        for fn in reversed(fns):
            x = fn(x)
        return x

    return composed


def add_one(x):
    return x + 1


def double(x):
    return x * 2


def compose_demo():
    first = compose(add_one, double)(3)
    second = compose(double, add_one)(3)
    return first, second


# ⭐ CORE
# Q1. What does `compose_demo()` return? Give a tuple of two numbers.
COMPOSE_RESULT = (7, 8)


# ---------------------------------------------------------------------------
# 2. pipeline (you write this)
# ---------------------------------------------------------------------------


def pipeline(data, *stages):
    """
    Runs `data` through the stages, from left to right, and returns the
    result. Each stage is a pair `(fn, kwargs)`: call `fn` with the current
    result as the first argument and `kwargs` as keyword arguments. With no
    stages, `data` comes back unchanged.

    Example:
        >>> def scale(x, factor=1.0): return [v * factor for v in x]
        >>> def shift(x, amount=0.0): return [v + amount for v in x]
        >>> pipeline([1.0, 2.0], (scale, {"factor": 2.0}), (shift, {"amount": -1.0}))
        [1.0, 3.0]
    """
    # Write your solution here.
    current = data
    for fn, kwargs in stages:
        current = fn(current, **kwargs)
    return current


# ---------------------------------------------------------------------------
# 3. make_clipper (you write this)
# ---------------------------------------------------------------------------


def make_clipper(lo, hi):
    """
    Returns a function. That function takes a list of readings and returns
    a new list in which every reading is clamped to the range `[lo, hi]`:
    smaller values become `lo`, larger values become `hi`. The input list
    is not changed.

    Example:
        >>> clip = make_clipper(0.0, 1.0)
        >>> clip([-0.5, 0.3, 2.0])
        [0.0, 0.3, 1.0]
    """

    # Write your solution here, in place of the placeholder below, which only keeps
    # the file running.
    return lambda readings: [max(lo, min(hi, r)) for r in readings]


# ---------------------------------------------------------------------------
# 4. Scopes (questions)
# ---------------------------------------------------------------------------


def late_binding_demo():
    fns = [lambda x: x + i for i in range(3)]  # noqa: B023
    return [f(10) for f in fns]


# Q4a. What does `late_binding_demo()` return? Give a list of three numbers.
LATE_BINDING_RESULT = [12, 12, 12]


def default_arg_demo():
    fns = [lambda x, i=i: x + i for i in range(3)]
    return [f(10) for f in fns]


# Q4b. What does `default_arg_demo()` return?
DEFAULT_ARG_RESULT = [10, 11, 12]


def make_counter():
    n = 0

    def count():
        n += 1  # noqa: F823
        return n

    return count


def counter_demo():
    count = make_counter()
    try:
        return count()
    except Exception as error:
        return type(error).__name__


# Q4c. What does `counter_demo()` return? Give a string.
COUNTER_RESULT = "UnboundLocalError"


threshold = 0.5


def set_threshold(value):
    threshold = value  # noqa: F841


def shadowing_demo():
    set_threshold(0.9)
    return threshold


# Q4d. What does `shadowing_demo()` return?
SHADOWING_RESULT = 0.5


# ---------------------------------------------------------------------------
# 5. Types and errors at run time (questions)
# ---------------------------------------------------------------------------

# Python is dynamically typed: a name can point to an object of any type,
# and Python only checks a type when an operation on it runs. Type
# annotations like `readings: list[float]` say what a function expects.
# Tools like mypy and ruff read the code before it runs and warn about
# mistakes they can find.


def amplify(readings: list[float], gain: int) -> list[float]:
    """Meant to multiply every reading by `gain`."""
    return readings * gain


# Q5a. What does `amplify([1.0, 2.0], 2)` return?
AMPLIFY_LIST = [1.0, 2.0, 1.0, 2.0]

# ⭐ CORE
# Q5b. What does `amplify("ab", 2)` return? If an exception is raised, give
#      its name as a string.
AMPLIFY_STR = "abab"


# `mean_or_none` has a typo. ruff and mypy both report it, which is why the
# line carries comments that silence them.


def mean_or_none(readings):
    """The mean of the readings, or None if there are none."""
    if len(readings) == 0:
        return Nnoe  # type: ignore[name-defined]  # noqa: F821
    return sum(readings) / len(readings)


def typo_demo():
    first = mean_or_none([1.0, 3.0])
    try:
        mean_or_none([])
    except Exception as e:
        return first, type(e).__name__
    return first, "no error"


# ⭐ CORE
# Q5c. What does `typo_demo()` return? Give a tuple of a number and a string.
TYPO_RESULT = (2.0, "NameError")


# ---------------------------------------------------------------------------
# Preprocessing helpers  (provided, do not modify)
# ---------------------------------------------------------------------------


def _center(readings, mean=0.0):
    """Subtracts mean from every reading."""
    return [x - mean for x in readings]


def _scale(readings, factor=1.0):
    """Multiplies every reading by factor."""
    return [x * factor for x in readings]


def _smooth(readings, window_size=3):
    """Replaces each reading with the mean of its surrounding window."""
    half = window_size // 2
    out = []
    for i in range(len(readings)):
        lo = max(0, i - half)
        hi = min(len(readings), i + half + 1)
        out.append(sum(readings[lo:hi]) / (hi - lo))
    return out


def _round_readings(readings, decimals=3):
    """Rounds every reading to `decimals` decimal places."""
    return [round(x, decimals) for x in readings]


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def _check(label, compute, expected):
    """Prints OK if `compute()` returns `expected`, NOT YET otherwise."""
    try:
        got = compute()
    except Exception as e:
        print(f"NOT YET: {label} raised {type(e).__name__}: {e}")
        return
    if got == expected:
        print(f"OK: {label}")
    else:
        print(f"NOT YET: {label} gave {got!r}, expected {expected!r}")


def _clip_example():
    """The clipped list and the input list after the call."""
    readings = [-0.5, 0.3, 2.0]
    clipped = make_clipper(0.0, 1.0)(readings)
    return clipped, readings


if __name__ == "__main__":
    # Checks of the functions you write, with the docstring examples.
    _check(
        'pipeline([1.0, 2.0], (_scale, {"factor": 2.0}), (_center, {"mean": 1.0}))',
        lambda: pipeline([1.0, 2.0], (_scale, {"factor": 2.0}), (_center, {"mean": 1.0})),
        [1.0, 3.0],
    )
    _check("pipeline([1.0, 2.0]) with no stages", lambda: pipeline([1.0, 2.0]), [1.0, 2.0])
    _check(
        "make_clipper(0.0, 1.0)([-0.5, 0.3, 2.0]) and the input list afterwards",
        _clip_example,
        ([0.0, 0.3, 1.0], [-0.5, 0.3, 2.0]),
    )
    print()

    random.seed(42)

    # 20 raw temperature readings (Celsius) with noise and a few spikes.
    raw = [20.0 + random.gauss(0, 0.5) + random.choice([0] * 9 + [5]) for _ in range(20)]
    print("Raw:", [round(x, 3) for x in raw])

    # Step 1: compose a normaliser. The last function runs first, so this
    # is: center, then scale.
    sample_mean = sum(raw) / len(raw)
    sample_range = max(raw) - min(raw)
    normalise = compose(
        lambda readings: _scale(readings, factor=2.0 / sample_range),
        lambda readings: _center(readings, mean=sample_mean),
    )
    normalised = normalise(raw)
    print("Normalised:", [round(x, 3) for x in normalised])

    # Step 2: clip the readings with a function made by make_clipper.
    clipped = make_clipper(-0.8, 0.8)(normalised)
    print("Clipped:", [round(x, 3) for x in clipped])

    # Step 3: a pipeline of steps, left to right.
    cleaned = pipeline(
        clipped,
        (_smooth, {"window_size": 3}),
        (_round_readings, {"decimals": 3}),
    )
    print("Cleaned:", cleaned)
