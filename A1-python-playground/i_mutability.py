"""
Mutability

In Python, a variable is a name that points to an object. Assignment never
copies anything: after `b = a`, both names point to the *same* object. If
that object is mutable (a list, a dict, a set, most class instances), a
change made through one name is visible through the other. If it is
immutable (an int, a float, a str, a tuple), nothing can change it, so the
question never comes up. A tuple can hold mutable objects, though: the tuple
itself always holds the same objects, but a list inside it can still change.

This matters a lot in ML code. A function that quietly changes the list or
array you passed in, or two models that accidentally share one config dict,
causes bugs that are hard to find, because the code that changes the data
and the code that notices it are far apart.

Two operations look alike but are very different:

- *Changing an object in place*, like `x.append(1)` or `x[0] = 5`. Every
  name pointing to that object sees the change.
- *Rebinding a name*, like `x = x + [1]`. This builds a new object and
  points `x` at it. Other names still point to the old object.

Use `is` to check whether two names point to the same object, and `==` to
check whether two objects have equal values. Every object has an identity,
a number you get with `id(x)`, and `a is b` means the same as
`id(a) == id(b)`.

Python frees memory by itself. CPython, the standard Python, counts how
many references point to each object, and frees the object as soon as
that count drops to zero.

This file has five parts. Work through them in order:

1. Aliasing and identity (questions).
2. Mutable default arguments (questions).
3. Shallow and deep copies (questions).
4. Fix the bug in `center`.
5. Read `SharedDataset` and answer the questions, then write `ListDataset`.

Answer the questions by setting the answer variables (they start out as
`None`). You may run code to check your answers.

⭐ CORE: Q1a, Q1b, Q1d, Q1e, the bug in `center`, and `ListDataset`.

DO NOT MODIFY THE FUNCTION SIGNATURES.
"""

import copy


# ---------------------------------------------------------------------------
# 1. Aliasing and identity (questions)
# ---------------------------------------------------------------------------


def aliasing_demo():
    a = [1, 2]
    b = a
    b.append(3)
    c = a
    c = c + [4]
    d = a
    d += [5]
    return a, b, c, d


def tuple_demo():
    t = (1, 2)
    u = t
    u += (3,)
    return t, u


def id_demo():
    x = 1
    y = x
    before = id(x) == id(y)
    x += 1
    after = id(x) == id(y)
    return before, after


class Tracked:
    """Prints a line when Python frees it."""

    def __del__(self):
        # `__del__` runs just before the object is freed.
        print("freed")


def free_demo():
    a = Tracked()
    b = a
    del a  # removes the name `a`
    print("after del a")
    b = None  # noqa: F841
    print("end")


# ⭐ CORE
# Q1a. What does `aliasing_demo()` return? Give a tuple of four lists.
ALIASING_RESULT = ([1, 2, 3, 5], [1, 2, 3, 5], [1, 2, 3, 4], [1, 2, 3, 5])

# ⭐ CORE
# Q1b. At the end of `aliasing_demo`, which of the names `b`, `c` and `d`
#      point to the same object as `a`? Give a list of names as strings,
#      in alphabetical order, e.g. ["b", "c"].
SAME_OBJECT_AS_A = ["b", "d"]

# Q1c. What does `tuple_demo()` return? Give a tuple of two tuples.
TUPLE_DEMO_RESULT = ((1, 2), (1, 2, 3))

# ⭐ CORE
# Q1d. What does `id_demo()` return? Give a tuple of two booleans.
ID_DEMO_RESULT = (True, False)

# ⭐ CORE
# Q1e. Which lines does `free_demo()` print, in order? Give a list of
#      strings, one per line.
FREE_DEMO_LINES = ["after del a", "freed", "end"]


# ---------------------------------------------------------------------------
# 2. Mutable default arguments (questions)
# ---------------------------------------------------------------------------


def add_batch(batch, history=[]):  # noqa: B006
    history.append(batch)
    return history


# Python evaluates a default value once, when the `def` statement runs, not
# every time the function is called.

# Suppose you start a fresh Python session, import this file, and then run
# these four calls in this order:
#
#     add_batch("a")
#     add_batch("b")
#     add_batch("c", [])
#     add_batch("d")
#
# Give each return value as it looks right after its call.

# Q2a. What does `add_batch("b")` return?
SECOND_CALL = ["a", "b"]

# Q2b. What does `add_batch("c", [])` return?
EXPLICIT_LIST_CALL = ["c"]

# Q2c. What does `add_batch("d")` return?
FOURTH_CALL = ["a", "b", "d"]


# ---------------------------------------------------------------------------
# 3. Shallow and deep copies (questions)
# ---------------------------------------------------------------------------


def copy_demo():
    config = {"lr": 0.1, "layers": [64, 32]}
    shallow = copy.copy(config)
    deep = copy.deepcopy(config)
    shallow["lr"] = 0.01
    shallow["layers"].append(16)
    deep["layers"].append(8)
    return config


# `copy.copy` makes a *shallow* copy: a new dict, but its values are the same
# objects as in the original. `copy.deepcopy` copies the values too, all the
# way down.

# Q3a. In the dict that `copy_demo()` returns, what is the value of "lr"?
CONFIG_LR = 0.1

# Q3b. In the same dict, what is the value of "layers"?
CONFIG_LAYERS = [64, 32, 16]


# ---------------------------------------------------------------------------
# 4. center (fix the bug)
# ---------------------------------------------------------------------------


# ⭐ CORE
def center(rows):
    """
    Returns a centered copy of a table, so that every column has mean 0.

    `rows` is a list of rows, and each row is a list of numbers of the same
    length. `center` must not change `rows` or any of its rows.

    This function has one bug: it changes the caller's data. Find it and fix
    it with the smallest change you can.

    Example:
        >>> table = [[1.0, 10.0], [3.0, 30.0]]
        >>> center(table)
        [[-1.0, -10.0], [1.0, 10.0]]
        >>> table
        [[1.0, 10.0], [3.0, 30.0]]
    """

    means = [sum(column) / len(rows) for column in zip(*rows)]
    result = copy.deepcopy(rows[:])
    for row in result:
        for j in range(len(row)):
            row[j] -= means[j]
    return result


# ---------------------------------------------------------------------------
# 5. SharedDataset (questions) and ListDataset (you write this)
# ---------------------------------------------------------------------------


class SharedDataset:
    """A dataset with a mistake in it."""

    samples: list = []

    def __init__(self, samples):
        for sample in samples:
            self.samples.append(sample)


# Suppose you start a fresh Python session, import this file, and run:
#
#     train = SharedDataset([1, 2, 3])
#     test = SharedDataset([4, 5])

# Q5a. What is `len(test.samples)`?
TEST_LENGTH = 5

# Q5b. Is `train.samples is test.samples` True or False?
SAMPLES_SHARED = True


# ⭐ CORE
class ListDataset:
    """
    A dataset that holds its samples in a list, with the same interface as
    a PyTorch `Dataset`: you can ask for its length, index into it, and loop
    over it.

    Every instance has its own samples. Unlike `SharedDataset`, two
    instances never share a list, and changing the list that was passed to
    `__init__` afterwards does not change the dataset.

    - `__init__(samples)`: stores a copy of `samples` in `self.samples`.
    - `__len__()`: the number of samples, so `len(ds)` works.
    - `__getitem__(i)`: the sample at index `i`, so `ds[i]` works. Negative
      indices and `IndexError` work the same as for a list.
    - `__iter__()`: yields the samples in order, so `for x in ds` works.
    - `append(sample)`: adds a sample at the end.

    Example:
        >>> data = [1, 2, 3]
        >>> ds = ListDataset(data)
        >>> data.append(4)
        >>> len(ds)
        3
        >>> ds[-1]
        3
        >>> ds.append(5)
        >>> list(ds)
        [1, 2, 3, 5]
        >>> ListDataset([7]).samples is ListDataset([7]).samples
        False
    """

    def __init__(self, samples):
        self.samples = list(samples)

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, index):
        return self.samples[index]

    def __iter__(self):
        for i in range(len(self.samples)):
            yield self.samples[i]

    def append(self, sample):
        self.samples.append(sample)


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


def _center_example():
    """The docstring example of `center`: the result, then the table."""
    table = [[1.0, 10.0], [3.0, 30.0]]
    result = center(table)
    return result, table


def _list_dataset_example():
    """The values from the docstring example of `ListDataset`."""
    data = [1, 2, 3]
    ds = ListDataset(data)
    data.append(4)
    length, last = len(ds), ds[-1]
    ds.append(5)
    return length, last, list(ds), ListDataset([7]).samples is ListDataset([7]).samples


def _list_dataset_index_error():
    """The exception that `ds[3]` raises for a dataset of three samples."""
    try:
        ListDataset([1, 2, 3])[3]
    except IndexError:
        return "IndexError"
    return "no IndexError"


if __name__ == "__main__":
    _check(
        "center([[1.0, 10.0], [3.0, 30.0]]), then the table",
        _center_example,
        ([[-1.0, -10.0], [1.0, 10.0]], [[1.0, 10.0], [3.0, 30.0]]),
    )
    _check(
        "ListDataset: len(ds), ds[-1], list(ds), ListDataset([7]).samples is ListDataset([7]).samples",
        _list_dataset_example,
        (3, 3, [1, 2, 3, 5], False),
    )
    _check("ListDataset: ds[3] for a dataset of three samples", _list_dataset_index_error, "IndexError")
