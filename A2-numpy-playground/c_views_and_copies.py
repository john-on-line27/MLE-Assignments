"""
Views and Copies

Remember aliasing from the Python playground: after `b = a`, both names
point to the same list, so changing it through one name changes it for the
other. NumPy takes this one step further. Many operations return a *view*:
a new array object, with its own shape, that points into the *same memory*
as the original. Writing into a view writes into the original.

Views are what make NumPy fast. Slicing a 1 GB dataset into batches, or
reshaping or transposing it, is almost free, because no data is copied. The
price is that you have to know which operations give you a view and which
give you a copy:

- Views: basic indexing (integers, slices, `None`, `...`), `reshape` (when
  it can, more on that in puzzle d), `.T` and `transpose`.
- Copies: advanced indexing (integer arrays and masks), `.copy()`,
  `.flatten()`, `.astype(...)`, and every arithmetic result like `a + 1`.

`np.shares_memory(a, b)` tells you whether two arrays use the same memory.

Turning something into an array also comes in these two kinds. `np.array(x)`
always copies, even when `x` is already an array. `np.asarray(x)` copies
only if it has to: given an array of the right dtype, it returns that very
array. Library functions start with `np.asarray` so they accept lists but
don't waste a copy on arrays.

One more pair to keep apart, the same as with lists:

- `x += 1` (and `-=`, `*=`, `/=`, `x[...] = ...`) changes the array *in
  place*. Every name and view pointing at that memory sees the change.
- `x = x + 1` builds a new array and points the name `x` at it. The old
  array, and anyone else holding it, is untouched.

Assigning *to* an advanced index, like `a[mask] = 0`, does change `a`:
NumPy treats an assignment to an index as one in-place operation. But
reading with an advanced index first, and then assigning into the result,
like `a[[0, 4]][1] = 7`, writes into a temporary copy that is thrown away.

This file has two parts. Work through them in order:

1. Views, copies and in-place writes (questions).
2. Fix the bugs in `iterate_minibatches` and `sgd_step`.

Answer the questions by setting the answer variables (they start out as
`None`). You may run code to check your answers. Give an array as a list,
such as [1, 2, 3].

Docs: https://numpy.org/doc/stable/user/basics.copies.html

⭐ CORE: Q1b and the bugs in `iterate_minibatches` and `sgd_step`.

DO NOT MODIFY THE FUNCTION SIGNATURES.
"""

from collections.abc import Iterator

import numpy as np


# ---------------------------------------------------------------------------
# 1. Views, copies and in-place writes (questions)
# ---------------------------------------------------------------------------


def write_demo():
    a = np.arange(6)
    b = a[1:4]
    b[0] = 100
    c = a[[1, 2]]
    c[1] = 200
    d = a.reshape(2, 3)
    d[1, 2] = 300
    return a


# Q1a. What does `write_demo()` return? Give a list.
WRITE_DEMO_RESULT = None


# ⭐ CORE
# Q1b. Let `a = np.arange(12).reshape(3, 4)`. Which of these share memory
#      with `a`? Give a list of letters in alphabetical order.
#
#      A  a[:, 1]
#      B  a[[1]]
#      C  a.T
#      D  a[a > 5]
#      E  a.reshape(-1)
#      F  a.flatten()
#      G  a[::2, ::-1]
#      H  a.astype(np.int64)
#      I  np.asarray(a)
#      J  np.array(a)
SHARES_MEMORY = None


def assignment_demo():
    a = np.zeros(5)
    a[[0, 1]] = 1
    a[[2, 3]][0] = 2
    a[2:4][0] = 3
    a[a == 0] = 4
    return a


# Q1c. What does `assignment_demo()` return? Give a list.
ASSIGNMENT_DEMO_RESULT = None


# ---------------------------------------------------------------------------
# 2. iterate_minibatches and sgd_step (fix the bugs)
# ---------------------------------------------------------------------------

# Two bugs that show up in real training code, one in each function. One
# function changes data it must leave alone; the other fails to change data
# it must update. Fix each with the smallest change you can.


# ⭐ CORE
def iterate_minibatches(X: np.ndarray, batch_size: int) -> Iterator[np.ndarray]:
    """
    Yields the rows of the float dataset `X` in batches of `batch_size`
    rows, in order, with every value divided by 255 (pixel values become
    values between 0 and 1). The last batch may be smaller.

    `X` itself must not change, so that the next epoch starts from the same
    data.

    Example:
        >>> X = np.array([[255.0], [51.0], [0.0]])
        >>> [b.tolist() for b in iterate_minibatches(X, 2)]
        [[[1.0], [0.2]], [[0.0]]]
        >>> X.tolist()
        [[255.0], [51.0], [0.0]]
    """

    for start in range(0, len(X), batch_size):
        batch = X[start : start + batch_size]
        batch /= 255.0
        yield batch


# ⭐ CORE
def sgd_step(params: list[np.ndarray], grads: list[np.ndarray], lr: float) -> None:
    """
    One step of gradient descent. Updates every parameter array in `params`
    *in place*: p becomes p - lr * g, where g is the matching array in
    `grads`. Returns None.

    The model holds references to these exact arrays, so the update must
    change them; building new arrays would leave the model unchanged.

    Example:
        >>> w = np.array([1.0, 2.0])
        >>> sgd_step([w], [np.array([10.0, 10.0])], lr=0.1)
        >>> w
        array([0., 1.])
    """

    for p, g in zip(params, grads):
        p = p - lr * g


if __name__ == "__main__":
    X = np.array([[255.0], [51.0], [0.0]])
    for epoch in range(2):
        batches = [b.tolist() for b in iterate_minibatches(X, 2)]
        print(f"epoch {epoch}:", batches)
    print("  expected the same batches in both epochs: [[[1.0], [0.2]], [[0.0]]]")

    w = np.array([1.0, 2.0])
    sgd_step([w], [np.array([10.0, 10.0])], lr=0.1)
    print("w after sgd_step:", w)
    print("  expected:        [0. 1.]")
