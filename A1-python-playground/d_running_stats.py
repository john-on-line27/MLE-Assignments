"""
Running Stats

`RunningStats` computes a running mean and variance from a stream of
numbers without storing the numbers themselves. That is useful when the
data is too big for memory, for example when you compute dataset
statistics in one pass over a training set.

The class is finished, but it has two bugs in the code that is already
there. Find them and fix each one with the smallest change you can. Submit
(`make submit-d`) and look at the results on the course website to see
which bugs are still there, then read the code and the docstrings to work
out why. After that, write one new method, `__add__`, at the bottom of the
class, and answer the three questions below the class.

The class uses Welford's online algorithm. Each call to `.update(x)` does:

    n      <- n + 1
    delta  = x - mean
    mean   <- mean + delta / n
    delta2 = x - mean          # uses the *updated* mean
    M2     <- M2 + delta * delta2

M2 is the sum of squared deviations. The sample variance is M2 / (n - 1)
when n >= 2.

`@property` lets you read a method like an attribute: `rs.mean`, not
`rs.mean()`.
https://docs.python.org/3/library/functions.html#property

`__repr__` and `__str__` both turn an object into text. `__repr__` is the
text for developers: it should show exactly what the object is. `__str__`
is the text for users. `str(x)`, `print(x)` and f-strings use `__str__`,
and `repr(x)` uses `__repr__`.
https://docs.python.org/3/reference/datamodel.html#object.__repr__

Answer the questions by setting the answer variables (they start out as
`None`). You may run code to check your answers.

⭐ CORE: the bug that makes `text_demo()` crash, and Q1.

DO NOT MODIFY THE FUNCTION SIGNATURES OR THE IMPORTS.
"""

import math
from statistics import StatisticsError


# ⭐ CORE: the bug that makes `text_demo()` crash
class RunningStats:
    def __init__(self):
        self._n = 0
        self._mean = 0.0
        self._M2 = 0.0

    def update(self, x):
        """Add one value to the statistics."""
        self._n += 1
        delta = x - self._mean
        self._mean += delta / self._n
        delta2 = x - self._mean
        self._M2 += delta * delta2

    @property
    def mean(self):
        """The mean. Raises StatisticsError if there are no values."""
        if self._n == 0:
            raise StatisticsError("mean requires at least one value")
        return self._mean

    @property
    def variance(self):
        """The sample variance. Raises StatisticsError for fewer than two
        values."""
        if self._n < 1:
            raise StatisticsError("variance requires at least two values")
        return self._M2 / (self._n - 1)

    def std(self):
        """The sample standard deviation, the square root of the variance.
        Raises StatisticsError for fewer than two values."""
        return math.sqrt(self.variance)

    def __len__(self):
        """The number of values seen so far."""
        return self._n

    def __repr__(self):
        """Like `RunningStats(n=3, mean=2.000, std=1.000)`. Shows 'N/A' for
        std if there are fewer than two values, and for mean if there are
        none."""
        mean_str = "N/A" if self._n == 0 else f"{self._mean:.3f}"
        std_str = "N/A" if self._n < 2 else f"{self.std:.3f}"
        return f"RunningStats(n={self._n}, mean={mean_str}, std={std_str})"

    def __str__(self):
        """Like `2.000 +/- 1.000 (n=3)`, with the same 'N/A' rules as
        `__repr__`."""
        mean_str = "N/A" if self._n == 0 else f"{self._mean:.3f}"
        std_str = "N/A" if self._n < 2 else f"{self.std:.3f}"
        return f"{mean_str} +/- {std_str} (n={self._n})"

    def reset(self):
        """Forget all values."""
        self.__init__()

    def __add__(self, other):
        """`a + b` is a new RunningStats with the statistics of both streams
        together, as if one object had seen every value from `a` and `b`.
        Neither `a` nor `b` is changed. This is how you combine statistics
        computed on different shards of a dataset, or on different workers.

        The merge formula (Chan et al.), with n_a, mean_a, M2_a from `a` and
        n_b, mean_b, M2_b from `b`:

            n     = n_a + n_b
            delta = mean_b - mean_a
            mean  = mean_a + delta * n_b / n
            M2    = M2_a + M2_b + delta**2 * n_a * n_b / n

        If one side has seen no values, the result is still a new
        RunningStats, with the same values as the other side (not the other
        side itself). If both are empty, the result is empty (n=0).

        If `other` is not a `RunningStats` (check with `isinstance`), return
        `NotImplemented`. That is a special value, not an exception. It
        tells Python that this method does not know how to add the two
        objects. Python then gives the other operand a chance (through its
        `__radd__`), and raises a `TypeError` if that does not work either.
        https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance#Parallel_algorithm

        (It is fine to set the private attributes of the new object
        directly.)
        """
        # Write your solution here.


# ---------------------------------------------------------------------------
# Questions
# ---------------------------------------------------------------------------


def text_demo():
    rs = RunningStats()
    for x in [1, 2, 3]:
        rs.update(x)
    return str(rs), repr(rs), str([rs])


def add_number_demo():
    try:
        RunningStats() + 5
    except Exception as e:
        return type(e).__name__
    return "no error"


# ⭐ CORE
# Q1. Each of the three strings that `text_demo()` returns was made by
#     either `__str__` or `__repr__` of `rs`. Which one, for each string?
#     Give a list of three strings, each "str" or "repr".
TEXT_METHODS = None

# Q2. What does `add_number_demo()` return? Assume your `__add__` is
#     correct. Give the name of the exception as a string, or "no error".
ADD_NUMBER_RESULT = None

# Q3. Suppose `__add__` had no `isinstance` check, so it started right away
#     by reading `other._n`. What would `add_number_demo()` return then?
#     Give the name of the exception as a string, or "no error".
ADD_WITHOUT_CHECK_RESULT = None


if __name__ == "__main__":
    import random

    random.seed(0)
    stream = [random.gauss(mu=10.0, sigma=2.0) for _ in range(1000)]

    def check(label, get, expected=True):
        """Print OK if `get()` returns `expected`, NOT YET otherwise."""
        try:
            got = get()
        except Exception as e:
            print(f"NOT YET: {label} (raised {type(e).__name__}: {e})")
            return
        if got == expected:
            print(f"OK: {label}")
        elif expected is True:
            print(f"NOT YET: {label}")
        else:
            print(f"NOT YET: {label}\n    expected {expected!r}\n    got      {got!r}")

    def raised(fn):
        """The name of the exception that `fn()` raises, or "no error"."""
        try:
            fn()
        except Exception as e:
            return type(e).__name__
        return "no error"

    def make(values):
        """A RunningStats that has seen `values`."""
        stats = RunningStats()
        for x in values:
            stats.update(x)
        return stats

    def summary(stats):
        """n, mean and variance, rounded so that tiny float errors don't count."""
        return len(stats), round(stats.mean, 6), round(stats.variance, 6)

    def is_copy_of(result, stats):
        """Whether `result` is a new RunningStats with the values of `stats`."""
        return isinstance(result, RunningStats) and result is not stats and summary(result) == summary(stats)

    def adds_without_changing(a, b):
        """Whether `a + b` is a new object and leaves `a` and `b` unchanged."""
        before = summary(a), summary(b)
        result = a + b
        new = isinstance(result, RunningStats) and result is not a and result is not b
        return new and (summary(a), summary(b)) == before

    # Smoke test: checks the parts that the docstrings describe.
    one, first, second = make(stream[:1]), make(stream[:400]), make(stream[400:])
    check("variance raises StatisticsError for a single value", lambda: raised(lambda: one.variance), "StatisticsError")
    check("first + second matches one RunningStats that saw every value", lambda: summary(first + second), summary(make(stream)))
    check("first + second is a new object and changes neither side", lambda: adds_without_changing(first, second))
    check("RunningStats() + first is a new RunningStats with the values of first", lambda: is_copy_of(RunningStats() + first, first))
    check("first + RunningStats() is a new RunningStats with the values of first", lambda: is_copy_of(first + RunningStats(), first))
    check("RunningStats() + RunningStats() is empty (n=0)", lambda: len(RunningStats() + RunningStats()), 0)
    check('__add__ returns NotImplemented for "x"', lambda: RunningStats().__add__("x"), NotImplemented)
    print()

    rs = RunningStats()
    print("Before any updates:", rs)

    for x in stream:
        rs.update(x)

    print("After 1000 updates:", rs)
    print("  n        :", len(rs))
    print(f"  mean     : {rs.mean:.4f}")
    print(f"  variance : {rs.variance:.4f}")
    print(f"  std      : {rs.std:.4f}")

    rs.reset()
    print("After reset:", rs)

    first, second = RunningStats(), RunningStats()
    for x in stream[:400]:
        first.update(x)
    for x in stream[400:]:
        second.update(x)
    merged = first + second
    print("Two halves merged:", merged)
