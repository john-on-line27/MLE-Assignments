"""
Batch Sampling

When a model trains, the data is not used all at once. It is cut into
batches, and the order is shuffled again for every epoch (one full pass over
the data). The parts below are small building blocks of this idea. Together
they work like PyTorch's `Sampler` and `DataLoader`.

The parts, in order:

1. `chunks` cuts a sequence into batches. Finished example.
2. Questions about generators: when do they run, what happens when you
   use one twice, and how is a generator expression different from a list
   comprehension?
3. You write `take`, then answer a question about it.
4. `first_satisfying` stops at the first match. Questions only.
5. `Sampler`, `SequentialSampler` and `OneShotSampler` use inheritance
   and the iterator protocol. You write `ShuffledSampler`, then answer
   questions about the samplers.

An abstract base class (ABC) is a class that cannot be used on its own. It
describes what its subclasses must provide.
https://docs.python.org/3/library/abc.html

Answer the questions by setting the answer variables (they start out as
`None`). You may run code to check your answers.

⭐ CORE: Q2a, Q2d, Q2e, Q4a, Q5b, `ShuffledSampler` and Q5e.

DO NOT MODIFY THE FUNCTION SIGNATURES.
"""

import random
import sys
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# 1. chunks (finished example)
# ---------------------------------------------------------------------------


def chunks(seq, size):
    """
    Yields successive lists of `size` items from `seq`. The last list can be
    shorter.

    A function with `yield` in it is a generator function: calling it gives
    you a generator, and looping over the generator gives you the values
    that the `yield`s hand out, one at a time.

    Example:
        >>> list(chunks([1, 2, 3, 4, 5], 2))
        [[1, 2], [3, 4], [5]]
    """
    for i in range(0, len(seq), size):
        yield list(seq[i : i + size])


# ---------------------------------------------------------------------------
# 2. Laziness and exhaustion (questions)
# ---------------------------------------------------------------------------


def noisy_range(n):
    """Like `range(n)`, but prints a line each time it makes a number."""
    for i in range(n):
        print(f"making {i}")
        yield i


def create_demo():
    gen = noisy_range(3)  # noqa: F841
    return None


def twice_demo():
    gen = chunks([1, 2, 3], 2)
    first = list(gen)
    second = list(gen)
    return first, second


# ⭐ CORE
# Q2a. How many lines does `create_demo()` print?
LINES_ON_CREATE = None

# Q2b. What does `twice_demo()` return? Give a tuple of two lists.
TWO_PASSES_OF_CHUNKS = None


# A list comprehension `[...]` and a generator expression `(...)` look
# almost the same, but they are not the same thing.


def comprehension_demo():
    squares_list = [x * x for x in noisy_range(3)]
    squares_gen = (x * x for x in noisy_range(3))
    return type(squares_list).__name__, type(squares_gen).__name__


# `sys.getsizeof` gives the memory an object takes up, in bytes.
def size_demo(n):
    as_list = sys.getsizeof([x * x for x in range(n)])
    as_gen = sys.getsizeof((x * x for x in range(n)))
    return as_list, as_gen


# Q2c. How many lines does `comprehension_demo()` print?
LINES_ON_COMPREHENSION = None

# ⭐ CORE
# Q2d. What does `comprehension_demo()` return? Give a tuple of two strings.
COMPREHENSION_TYPES = None

# ⭐ CORE
# Q2e. Compare `size_demo(10)` with `size_demo(10_000)`. One of the two
#      sizes stays the same. Which one? Answer "list" or "generator".
CONSTANT_SIZE = None


# ---------------------------------------------------------------------------
# 3. take (you write this)
# ---------------------------------------------------------------------------


def take(iterable, n):
    """
    Returns a list of the first `n` items of `iterable`. If the iterable has
    fewer than `n` items, returns all of them, without an error. It must
    not ask the iterable for more than `n` items.

    You MUST use `iter()` and `next()` yourself. Do not use slicing, `islice`
    or a list comprehension. `next()` raises `StopIteration` when there is
    nothing left.

    Example:
        >>> take(range(10), 4)
        [0, 1, 2, 3]
        >>> take(range(3), 5)
        [0, 1, 2]
    """
    # Write your solution here.

    iterator = iter(iterable)
    result = []
    for _ in range(n):
        try:
            result.append(next(iterator))
        except StopIteration:
            break
    return result


def take_demo():
    return take(noisy_range(100), 2)


# Q3. How many lines does `take_demo()` print? Assume `take` is correct.
LINES_ON_TAKE = None


# ---------------------------------------------------------------------------
# 4. first_satisfying (questions)
# ---------------------------------------------------------------------------


def first_satisfying(iterable, predicate):
    """
    Returns `(item, index)` for the first item where `predicate(item)` is
    true, or `(None, -1)` if there is no such item.

    A `return` inside a loop leaves the function at once, so the loop stops
    at the first match and never looks at the rest of the items.
    """
    for i, x in enumerate(iterable):
        if predicate(x):
            return (x, i)
    return (None, -1)


# ⭐ CORE
# Q4a. What does `first_satisfying([4, 7, 2, 9], lambda x: x > 6)` return?
FIRST_MATCH = None

# Q4b. What does `first_satisfying([1, 2, 3], lambda x: x > 10)` return?
NO_MATCH = None


# ---------------------------------------------------------------------------
# 5. Samplers (inheritance)
# ---------------------------------------------------------------------------


class Sampler(ABC):
    """
    Base class for samplers. A sampler gives out batches of indices, and
    drops the last batch if it is not full.

    `Sampler` is abstract: `indices` is marked with `@abstractmethod`, so a
    subclass must define it, and `Sampler` itself cannot be created. The
    subclass only decides the order. `__iter__` is shared by all subclasses.
    """

    def __init__(self, n_samples, batch_size):
        self.n_samples = n_samples
        self.batch_size = batch_size

    def __iter__(self):
        batches = chunks(self.indices(), self.batch_size)
        # A generator expression: a comprehension with ( ) instead of [ ].
        # It builds no list. Each batch is checked only when the loop asks
        # for it.
        full = (b for b in batches if len(b) == self.batch_size)
        # `yield from` hands out every item of another iterable, one by one.
        yield from full

    @abstractmethod
    def indices(self):
        """Returns a list of all sample indices, in the order to use."""


class SequentialSampler(Sampler):
    """Batches in the original order: 0, 1, 2, ..."""

    def indices(self):
        return list(range(self.n_samples))


class OneShotSampler:
    """
    A sampler that is an iterator itself, written by hand. It gives out the
    same batches as `SequentialSampler`.

    An object is an iterator if it has two methods. `__iter__` returns the
    iterator, here `self`. `__next__` returns the next value. Here it builds
    the next batch from the position it keeps in `self.pos`. When no full
    batch is left, `__next__` raises `StopIteration`: that is how an
    iterator tells a `for` loop, `list` or `next` that it is finished.
    """

    def __init__(self, n_samples, batch_size):
        self.n_samples = n_samples
        self.batch_size = batch_size
        self.pos = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.pos + self.batch_size > self.n_samples:
            raise StopIteration
        batch = list(range(self.pos, self.pos + self.batch_size))
        self.pos += self.batch_size
        return batch


def abstract_demo():
    try:
        Sampler(10, 2)
    except Exception as e:
        return type(e).__name__
    return "no error"


def one_shot_demo():
    sampler = OneShotSampler(6, 3)
    first = len(list(sampler))
    second = len(list(sampler))
    return first, second


def sequential_demo():
    sampler = SequentialSampler(6, 3)
    first = len(list(sampler))
    second = len(list(sampler))
    return first, second


# ⭐ CORE
class ShuffledSampler(Sampler):
    """
    Batches in a random order. You write `__init__` and `indices`.

    - `__init__(self, *args, seed=None, **kwargs)` passes everything except
      `seed` on with `super().__init__(*args, **kwargs)`, then stores
      `seed`. This way `ShuffledSampler` does not repeat the arguments of
      `Sampler`: `*args` packs the positional arguments into a tuple,
      `**kwargs` packs the keyword arguments into a dict, and the call
      unpacks them again. Because `seed` comes after `*args`, it can only
      be given by name, as in `seed=1`.
    - `indices` makes the list `list(range(n_samples))`, shuffles it in
      place with `random.Random(self.seed).shuffle`, and returns it. (Use
      `.shuffle`: `.sample` gives a different order, and the checks expect
      the order of `.shuffle`.) Create `random.Random(self.seed)` inside
      `indices`, not in `__init__`. Then a fixed seed gives the same order
      on every pass, and `seed=None` gives a new order on every pass.
    """

    # Write your solution here, in place of the placeholder below, which only keeps
    # the file running.
    def __init__(self, *args, seed=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.seed = seed

    def indices(self):
        ret = list(range(self.n_samples))
        rng = random.Random(self.seed)
        rng.shuffle(ret)
        return ret


def positional_seed_demo():
    try:
        sampler = ShuffledSampler(10, 2, 1)
    except Exception as e:
        return type(e).__name__
    return sampler.seed


# Q5a. What does `abstract_demo()` return? Give the name of the exception
#      as a string, or "no error".
ABSTRACT_RESULT = None

# ⭐ CORE
# Q5b. What does `one_shot_demo()` return? Give a tuple of two ints.
ONE_SHOT_PASSES = None

# Q5c. What does `sequential_demo()` return? Give a tuple of two ints.
SEQUENTIAL_PASSES = None

# Q5d. Suppose `OneShotSampler.__next__` had `return None` where it now has
#      `raise StopIteration`. What would `take(OneShotSampler(6, 3), 4)`
#      return then? (Don't try `list(...)` on that sampler: it would never
#      stop.)
TAKE_WITHOUT_STOP = None

# ⭐ CORE
# Q5e. What does `positional_seed_demo()` return? Assume your
#      `ShuffledSampler` works as its docstring says (the placeholder
#      doesn't). If it raises, give the name of the exception as a string.
POSITIONAL_SEED_RESULT = None


if __name__ == "__main__":

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

    def asks_for_at_most(n):
        """Whether `take(it, n)` leaves the rest of `it` untouched."""
        it = iter(range(10))
        take(it, n)
        return next(it) == n

    def shuffled_batches(n_samples, batch_size, seed):
        """The batches the docstring of `ShuffledSampler` describes."""
        order = list(range(n_samples))
        random.Random(seed).shuffle(order)
        return [b for b in chunks(order, batch_size) if len(b) == batch_size]

    def same_order_on_two_passes(sampler, expected):
        """Whether two passes over `sampler` both give `expected`."""
        return list(sampler) == expected and list(sampler) == expected

    def new_order_on_every_pass():
        """Whether two passes with `seed=None` give different orders."""
        sampler = ShuffledSampler(100, 10)
        first = list(sampler)
        return len(first) == 10 and first != list(sampler)

    def every_index_once(sampler):
        """Whether the batches hold every index exactly once."""
        return sorted(i for batch in sampler for i in batch) == list(range(sampler.n_samples))

    # Smoke test: checks `take` and `ShuffledSampler` against their docstrings.
    check("take(range(10), 4) gives [0, 1, 2, 3]", lambda: take(range(10), 4), [0, 1, 2, 3])
    check("take(range(3), 5) gives [0, 1, 2]", lambda: take(range(3), 5), [0, 1, 2])
    check("take(it, 2) does not ask `it` for more than 2 items", lambda: asks_for_at_most(2))
    check("ShuffledSampler(20, 4, seed=1) gives every index exactly once", lambda: every_index_once(ShuffledSampler(20, 4, seed=1)))
    check(
        "ShuffledSampler(20, 4, seed=1) uses the order of random.Random(1).shuffle, on every pass",
        lambda: same_order_on_two_passes(ShuffledSampler(20, 4, seed=1), shuffled_batches(20, 4, 1)),
    )
    check(
        "ShuffledSampler(n_samples=20, batch_size=4, seed=2) works with keyword arguments",
        lambda: list(ShuffledSampler(n_samples=20, batch_size=4, seed=2)),
        shuffled_batches(20, 4, 2),
    )
    check("ShuffledSampler(100, 10) (seed=None) gives a new order on every pass", new_order_on_every_pass)

    # Synthetic dataset: 20 samples with a "feature" that decreases with the
    # index, so batches with high indices have a lower loss.
    random.seed(0)
    dataset = [1.0 - (i / 20) + random.uniform(-0.05, 0.05) for i in range(20)]

    N_EPOCHS = 2
    BATCH_SIZE = 4
    LOG_INTERVAL = 2  # summarise this many batches at a time
    LOSS_TARGET = 0.55  # threshold we want to cross

    for epoch in range(N_EPOCHS):
        print(f"\n{'=' * 42}")
        print(f"Epoch {epoch + 1}")

        # A new seed for every epoch gives a new order every epoch, and the
        # same orders on every run. Within an epoch, the seed stays fixed, so
        # the preview and the training loop see the same order.
        sampler = ShuffledSampler(len(dataset), BATCH_SIZE, seed=epoch)

        # take: preview the first two batches
        print(f"  Preview: {take(sampler, 2)}")

        # A "loss" for every batch (you will learn about loss soon).
        batches = list(sampler)
        losses = [sum(dataset[i] for i in b) / len(b) for b in batches]

        # chunks: log the average loss every LOG_INTERVAL batches
        print(f"  Training: {len(batches)} batches")
        for group in chunks(list(enumerate(losses)), LOG_INTERVAL):
            avg = sum(loss for _, loss in group) / len(group)
            print(f"    batches {group[0][0]}-{group[-1][0]}  loss: {avg:.4f}")

        # first_satisfying: when does the loss first drop below the target?
        value, pos = first_satisfying(losses, lambda loss: loss < LOSS_TARGET)
        if value is None:
            print(f"  Loss never dropped below {LOSS_TARGET}")
        else:
            print(f"  Loss below {LOSS_TARGET} at batch {pos} ({value:.4f})")
