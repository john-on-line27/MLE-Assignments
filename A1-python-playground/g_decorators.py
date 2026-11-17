"""
Decorators

A decorator is a function that takes a function and returns a new function,
usually one that does something extra before or after calling the original.
Writing

    @log_calls
    def train_step(batch): ...

is the same as writing

    def train_step(batch): ...
    train_step = log_calls(train_step)

ML code uses decorators everywhere: `@torch.no_grad()`, `@property`,
`@dataclass`, and the registries that let you pick a model or an activation
function by its name in a config file.

This file has six parts. Work through them in order:

1. `log_calls` is a finished example. Read it carefully, since the parts you
   write follow the same pattern.
2. You write `count_calls`.
3. `register` is a finished example of a function that returns a
   decorator, used on functions and on a class. Read it, then answer the
   questions below it.
4. You write `retry`, another function that returns a decorator.
5. Read the stacked decorators on `train_step` and answer the questions
   below them.
6. Read `load_split`, which uses a decorator from the standard library,
   and answer the question below it.

Answer the questions by setting the answer variables (they start out as
`None`). You may run code to check your answers.

When you are done, run this file with `python g_decorators.py`. It should
print exactly:

    -> train_step([1.0, 2.0])
    <- train_step returned 1.5
    -> train_step([3.0, 5.0])
    <- train_step returned 4.0
    sigmoid(0.0) = 0.5

    OK: count_calls: square.calls, square(3), square(4), square.calls, name, docstring
    attempt 1/3 failed: ConnectionError
    attempt 2/3 failed: ConnectionError
    OK: retry: download_shard(7) and its name
    attempt 1/3 failed: ConnectionError
    attempt 2/3 failed: ConnectionError
    attempt 3/3 failed: ConnectionError
    OK: retry: (exception, calls) when every call raises ConnectionError
    OK: retry: (exception, calls) when the call raises ValueError

A line that starts with NOT YET tells you which function still needs work.

⭐ CORE: `count_calls`, Q3a, Q3b, Q5a and Q6.

DO NOT MODIFY THE FUNCTION SIGNATURES.
"""

import functools
import math


# ---------------------------------------------------------------------------
# 1. log_calls (finished example)
# ---------------------------------------------------------------------------


def log_calls(fn):
    """
    Prints a line before and after every call to `fn`.

    Example:
        >>> @log_calls
        ... def add(a, b):
        ...     return a + b
        >>> add(1, 2)
        -> add(1, 2)
        <- add returned 3
        3
    """

    def wrapper(*args, **kwargs):
        # `*args` and `**kwargs` collect whatever arguments the caller passes,
        # so this one wrapper works for functions of any signature.
        arg_text = ", ".join([repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()])
        print(f"-> {fn.__name__}({arg_text})")
        result = fn(*args, **kwargs)  # call the original function
        print(f"<- {fn.__name__} returned {result!r}")
        return result  # hand the original result back to the caller

    # Copy the name and docstring of `fn` onto `wrapper`. Without this,
    # `add.__name__` would be "wrapper", which makes error messages and logs
    # confusing. Functions are objects, so this is plain attribute assignment.
    wrapper.__name__ = fn.__name__
    wrapper.__doc__ = fn.__doc__

    # The decorator returns the new function. It does not call it.
    return wrapper


# ---------------------------------------------------------------------------
# 2. count_calls (you write this)
# ---------------------------------------------------------------------------


# ⭐ CORE
def count_calls(fn):
    """
    Counts how many times `fn` has been called.

    The returned function has an attribute `calls` that starts at 0 and goes
    up by one on every call, before `fn` runs. Everything else behaves exactly
    like `fn`: the same arguments, the same return value, the same name and
    docstring.

    Example:
        >>> @count_calls
        ... def square(x):
        ...     return x * x
        >>> square.calls
        0
        >>> square(3)
        9
        >>> square(4)
        16
        >>> square.calls
        2
        >>> square.__name__
        'square'

    (_Hint: functions are objects, so you can set attributes on them, like
    `wrapper.calls = 0`. Copy the name and docstring the way `log_calls`
    does._)

    Keep the count in `wrapper.calls` itself, and copy the name and docstring
    by hand. Don't use `nonlocal` or `functools.wraps`: this puzzle doesn't
    need them.
    """

    # Write your solution here, in place of the placeholder below, which only keeps
    # the file running.
    def wrapper(*args, **kwargs):
        wrapper.calls = wrapper.calls + 1
        result = fn(*args, **kwargs)
        return result

    wrapper.calls = 0
    wrapper.__name__ = fn.__name__
    wrapper.__doc__ = fn.__doc__
    return wrapper


# ---------------------------------------------------------------------------
# 3. register (finished example, with questions)
# ---------------------------------------------------------------------------

ACTIVATIONS = {}


def register(name):
    """
    Stores the decorated function or class in `ACTIVATIONS` under `name`.

    `register` is not a decorator itself. It is a function that *returns* a
    decorator. That is why it is used with parentheses, `@register("relu")`:
    Python first calls `register("relu")`, and then uses the function that
    call returns as the decorator.

    Example:
        >>> @register("relu")
        ... def relu(x):
        ...     return max(0.0, x)
        >>> ACTIVATIONS["relu"](-2.0)
        0.0
    """

    def decorator(fn):
        # `decorator` can still see `name`, even after `register` has
        # returned. A function that remembers the variables around it like
        # this is called a closure.
        ACTIVATIONS[name] = fn
        return fn  # the original function, not a wrapper

    return decorator


@register("relu")
def relu(x):
    return max(0.0, x)


@register("sigmoid")
def sigmoid(x):
    return 1 / (1 + math.exp(-x))


@register("identity")
def identity(x):
    return x


# A decorator can go on a class, too. `register` does not care what it
# gets: here it stores the class `LeakyReLU` itself. Code that reads a
# config often looks a model up this way and creates it with
# `MODELS[config["model"]]()`.
#
# `__call__` makes an instance callable like a function: `act(x)` runs
# `act.__call__(x)`.


@register("leaky_relu")
class LeakyReLU:
    def __init__(self, slope=0.01):
        self.slope = slope

    def __call__(self, x):
        return x if x > 0 else self.slope * x


# ⭐ CORE
# Q3a. Suppose you import this file and call none of its functions. What is
#      `sorted(ACTIVATIONS)` then? Give a list of strings.
REGISTERED_AT_IMPORT = ["identity", "leaky_relu", "relu", "sigmoid"]

# ⭐ CORE
# Q3b. Is `relu is ACTIVATIONS["relu"]` True or False?
RELU_IS_STORED_FUNCTION = True

# Q3c. What is `type(ACTIVATIONS["leaky_relu"](-2.0)).__name__`?
LEAKY_CALL_TYPE = "LeakyReLU"

# Q3d. What is `ACTIVATIONS["leaky_relu"]()(-2.0)`?
LEAKY_VALUE = -0.02


# ---------------------------------------------------------------------------
# 4. retry (you write this)
# ---------------------------------------------------------------------------


def retry(times, exceptions=(Exception,)):
    """
    Returns a decorator that calls the decorated function up to `times` times
    until one call succeeds.

    Use this for operations that sometimes fail for no fault of your own, like
    downloading a shard of a dataset over a slow network.

    - If a call raises one of the exception types in `exceptions`, print
      `attempt <k>/<times> failed: <ExceptionName>` and try again. `k` counts
      from 1.
    - If the last attempt fails too, print its line as well and then let its
      exception propagate to the caller.
    - Any other exception propagates right away, without a retry.
    - The first call that succeeds returns its result.
    - The decorated function keeps the name and docstring of the original.
      Copy them by hand, the way `log_calls` does, not with `functools.wraps`.

    Example:
        >>> @retry(times=3, exceptions=(ConnectionError,))
        ... def download_shard(i):
        ...     ...  # fails twice with ConnectionError, then succeeds
        >>> download_shard(7)
        attempt 1/3 failed: ConnectionError
        attempt 2/3 failed: ConnectionError
        'shard-7'

    (_Hints: `register` above has the same shape: an outer function that
    takes the arguments and returns the actual decorator. You need three
    nested functions here: `retry`, the decorator, and the wrapper.
    `except exceptions as e:` works when `exceptions` is a variable that
    holds a tuple of exception classes: it catches an exception of any class
    in the tuple. `type(e).__name__` is the name of the class of `e`, like
    "ConnectionError"._)
    """

    # Write your solution here, in place of the placeholder below, which only keeps
    # the file running.
    def decorator(fn):
        def wrapper(*args, **kwargs):
            for i in range(times):
                try:
                    ret = fn(*args, **kwargs)
                    return ret
                except exceptions as e:
                    print(f"attempt {i + 1}/{times} failed: {type(e).__name__}")
                    if i + 1 == times:
                        raise e

        wrapper.__name__ = fn.__name__
        wrapper.__doc__ = fn.__doc__
        return wrapper

    return decorator


# ---------------------------------------------------------------------------
# 5. Stacked decorators (questions)
# ---------------------------------------------------------------------------


@log_calls
@count_calls
def train_step(batch):
    """Returns the mean of a batch, standing in for the loss."""
    return sum(batch) / len(batch)


# Decorators are applied from the bottom up: `count_calls` wraps
# `train_step` first, and then `log_calls` wraps the result.

# ⭐ CORE
# Q5a. When you call `train_step([1.0, 2.0])`, which wrapper starts running
#      first? Answer "log_calls" or "count_calls".
RUNS_FIRST = "log_calls"

# Q5b. What is `train_step.__name__`?
STACKED_NAME = "train_step"

# Q5c. Suppose `count_calls` did NOT copy `__name__` onto its inner
#      function, which is named `wrapper`, but `log_calls` still did. What
#      would `train_step.__name__` be then?
STACKED_NAME_WITHOUT_WRAPS = "wrapper"


# ---------------------------------------------------------------------------
# 6. functools.cache (question)
# ---------------------------------------------------------------------------

# `@functools.cache` is a decorator from the standard library. Its wrapper
# keeps a dict that maps arguments to results. When the wrapper is called
# with arguments it has seen before, it returns the stored result instead
# of calling the function again.
# https://docs.python.org/3/library/functools.html#functools.cache


@functools.cache
def load_split(name):
    """Stands in for reading one split of a dataset from disk, which is
    slow."""
    print(f"loading {name}")
    return f"<{name} data>"


def cache_demo():
    load_split.cache_clear()  # empty the stored results first
    for name in ["train", "val", "train", "train", "val"]:
        load_split(name)


# ⭐ CORE
# Q6. How many lines does `cache_demo()` print?
CACHE_LINES = 2


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


def _count_calls_example():
    """The values from the docstring example of `count_calls`."""

    @count_calls
    def square(x):
        """Returns x * x."""
        return x * x

    before = square.calls
    first, second = square(3), square(4)
    after = square.calls
    return before, first, second, after, square.__name__, square.__doc__


def _retry_example():
    """`download_shard(7)` from the docstring of `retry`, and its name."""
    failures = {"left": 2}

    @retry(times=3, exceptions=(ConnectionError,))
    def download_shard(i):
        if failures["left"] > 0:
            failures["left"] -= 1
            raise ConnectionError("network hiccup")
        return f"shard-{i}"

    return download_shard(7), download_shard.__name__


def _retry_raises(error_class):
    """The exception that reaches the caller, and how many calls ran."""
    calls = []

    @retry(times=3, exceptions=(ConnectionError,))
    def always_fails():
        calls.append(1)
        raise error_class("it broke")

    try:
        always_fails()
    except Exception as e:
        return type(e).__name__, len(calls)
    return None, len(calls)


if __name__ == "__main__":
    train_step([1.0, 2.0])
    train_step([3.0, 5.0])

    # Look an activation function up by its registered name.
    activation = ACTIVATIONS["sigmoid"]
    print("sigmoid(0.0) =", activation(0.0))
    print()

    _check(
        "count_calls: square.calls, square(3), square(4), square.calls, name, docstring",
        _count_calls_example,
        (0, 9, 16, 2, "square", "Returns x * x."),
    )
    _check("retry: download_shard(7) and its name", _retry_example, ("shard-7", "download_shard"))
    _check(
        "retry: (exception, calls) when every call raises ConnectionError",
        lambda: _retry_raises(ConnectionError),
        ("ConnectionError", 3),
    )
    _check(
        "retry: (exception, calls) when the call raises ValueError",
        lambda: _retry_raises(ValueError),
        ("ValueError", 1),
    )
