"""
Context Managers

A context manager sets something up when a `with` block starts and cleans
it up when the block ends, even if the block raises an exception. You have
already used one:

    with open("data.csv") as f:
        rows = f.readlines()

`open` returns a file object, and the `with` statement makes sure the file
is closed afterwards. ML code uses context managers for the same kind of
job: `torch.no_grad()` turns gradient tracking off for a block and back on
afterwards, and timers and loggers measure or record just one part of a
training loop.

Writing

    with manager as x:
        body

does roughly this:

    x = manager.__enter__()
    try:
        body
    except BaseException as e:
        if not manager.__exit__(type(e), e, e.__traceback__):
            raise
    else:
        manager.__exit__(None, None, None)

So `__enter__` runs first, and its return value is what `as` binds to.
`__exit__` always runs at the end. If the body raised an exception,
`__exit__` receives it, and its return value decides what happens next:
a true value swallows the exception, and anything else lets it propagate.

This file has four parts. Work through them in order:

1. `Timer` is a finished example. Read it carefully, then run
   `timing_demo` and answer the question below it.
2. You write `seeded`.
3. Read `Announce` and `nested_demo`, then answer the questions below them.
4. Read `SkipBadBatch` and `count_good_batches`, then answer the questions
   below them.

Answer the questions by setting the answer variables (they start out as
`None`). You may run code to check your answers.

When you are done, run this file with `python j_context_managers.py`. It
should print exactly:

    OK: seeded(42): shuffle of range(8)
    OK: seeded: the outer random stream continues as if the block never ran
    OK: seeded: the outer random stream is restored when the block raises

A line that starts with NOT YET tells you what `seeded` still gets wrong.

⭐ CORE: Q1, `seeded`, Q3a and Q3b.

DO NOT MODIFY THE FUNCTION SIGNATURES.
"""

import contextlib
import random
import time


# ---------------------------------------------------------------------------
# 1. Timer (finished example, with a question)
# ---------------------------------------------------------------------------


class Timer:
    """
    Measures how long the body of a `with` block takes, in seconds.

    Example:
        >>> with Timer() as t:
        ...     total = sum(range(1_000_000))
        >>> t.elapsed > 0
        True
    """

    def __init__(self):
        self.elapsed = None

    def __enter__(self):
        self.start = time.perf_counter()
        # Whatever `__enter__` returns is bound to the name after `as`.
        # Returning `self` lets the caller read `t.elapsed` afterwards.
        return self

    def __exit__(self, exc_type, exc, tb):
        # `exc_type`, `exc` and `tb` describe the exception the body raised,
        # or are all `None` if the body finished normally. The timer does not
        # care which; it stops either way.
        self.elapsed = time.perf_counter() - self.start
        # Returning `False` (or `None`) means: do not swallow any exception.
        return False


def loop_sum(n):
    total = 0
    for i in range(n):
        total += i
    return total


def builtin_sum(n):
    return sum(range(n))


def timing_demo(n=1_000_000, precision=4):
    with Timer() as t_loop:
        loop_sum(n)
    with Timer() as t_builtin:
        builtin_sum(n)
    # `{x:.{precision}f}` puts a variable into the format: with
    # `precision=4` it means `{x:.4f}`, a float with four decimals.
    print(f"loop:    {t_loop.elapsed:.{precision}f} s")
    print(f"builtin: {t_builtin.elapsed:.{precision}f} s")


# ⭐ CORE
# Q1. Run `timing_demo()`. Both functions compute the same sum. Which one
#     is faster? Answer "loop" or "builtin".
FASTER_SUM = "builtin"


# ---------------------------------------------------------------------------
# 2. seeded (you write this)
# ---------------------------------------------------------------------------


# ⭐ CORE
@contextlib.contextmanager
def seeded(seed):
    """
    Seeds Python's `random` module for the body of a `with` block, then puts
    the random state back the way it was before the block.

    Use this to make one part of a program reproducible, like shuffling a
    validation set, without changing the random numbers the rest of the
    program sees.

    - Before the block: save the current state with `random.getstate()`,
      then call `random.seed(seed)`.
    - After the block: restore the saved state with `random.setstate(...)`.
      This must also happen when the block raises an exception.
    - The `with` statement binds nothing useful, so `with seeded(0):` is
      enough.

    `@contextlib.contextmanager` turns a generator function into a context
    manager. Everything before the `yield` runs as `__enter__`, and
    everything after it runs as `__exit__`. If the body raises, the exception
    is raised again at the `yield`, inside your function.

    Example:
        >>> with seeded(0):
        ...     a = random.random()
        >>> with seeded(0):
        ...     b = random.random()
        >>> a == b
        True

    (_Hint: wrap the `yield` in `try`/`finally`._)
    """

    # Write your solution here, in place of the placeholder below, which only keeps
    # the file running.
    new_seed = random.getstate()
    random.seed(seed)
    try:
        yield
    finally:
        random.setstate(new_seed)


# ---------------------------------------------------------------------------
# 3. Nested blocks and exceptions (questions)
# ---------------------------------------------------------------------------


class Announce:
    """Prints a line when its block starts and when it ends."""

    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print(f"enter {self.name}")
        return self

    def __exit__(self, exc_type, exc, tb):
        print(f"exit {self.name}")
        return False


def nested_demo():
    with Announce("outer"):
        with Announce("inner"):
            print("body")
            raise ValueError("bad batch")
            print("after raise")
        print("after inner")
    print("after outer")


# ⭐ CORE
# Q3a. Which lines do the `print` calls produce when you call
#      `nested_demo()`, in order? Give a list of strings, one per line,
#      e.g. ["enter outer", ...]. Leave out the traceback (the error
#      message) that Python prints if an exception is not caught.
NESTED_LINES = ["enter outer", "enter inner", "body", "exit inner", "exit outer"]

# ⭐ CORE
# Q3b. Does the `ValueError` reach the code that called `nested_demo()`?
#      Answer True or False.
NESTED_RAISES = True


# ---------------------------------------------------------------------------
# 4. Swallowing exceptions (questions)
# ---------------------------------------------------------------------------


class SkipBadBatch:
    """Swallows a `ValueError` raised in its block, and nothing else."""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return exc_type is ValueError


def count_good_batches(batches):
    good = 0
    for batch in batches:
        with SkipBadBatch():
            if len(batch) == 0:
                raise ValueError("empty batch")
            good += 1
    return good


# Q4a. What does `count_good_batches([[1, 2], [], [3], []])` return?
GOOD_BATCHES = 2

# Q4b. What happens when you call `count_good_batches([[1, 2], None, [3]])`?
#      If it returns, give the return value. If an exception reaches the
#      caller, give the name of the exception as a string, e.g. "KeyError".
GOOD_BATCHES_WITH_NONE = "TypeError"


# ---------------------------------------------------------------------------
# Driver
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


def _seeded_shuffle():
    """`range(8)`, shuffled inside `seeded(42)`."""
    random.seed(123)  # the "outer" random stream
    items = list(range(8))
    with seeded(42):
        random.shuffle(items)
    return items


def _outer_stream_untouched(raise_in_block):
    """Whether the outer stream continues as if the block never ran."""
    random.seed(123)
    expected = random.random()
    random.seed(123)
    try:
        with seeded(42):
            random.random()
            if raise_in_block:
                raise ValueError("bad batch")
    except ValueError:
        pass
    return random.random() == expected


if __name__ == "__main__":
    _check("seeded(42): shuffle of range(8)", _seeded_shuffle, [3, 4, 6, 7, 2, 5, 0, 1])
    _check(
        "seeded: the outer random stream continues as if the block never ran",
        lambda: _outer_stream_untouched(raise_in_block=False),
        True,
    )
    _check(
        "seeded: the outer random stream is restored when the block raises",
        lambda: _outer_stream_untouched(raise_in_block=True),
        True,
    )
