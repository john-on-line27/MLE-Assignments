"""
Broadcasting

Elementwise operations like `+` and `*` normally need two arrays of the
same shape. Broadcasting relaxes that. To combine two shapes, NumPy lines
them up from the *right* and compares them axis by axis:

1. If one shape has fewer axes, pretend it has extra axes of size 1 on the
   left: (3,) is treated as (1, 3).
2. Two sizes fit if they are equal, or if one of them is 1.
3. An axis of size 1 is stretched to match the other size. On every axis,
   the result has the size that isn't 1 (or 1, if both are 1).
4. If any pair doesn't fit, you get a ValueError.

    X:        (64, 10)
    b:            (10,)   -> treated as (1, 10), stretched to (64, 10)
    X + b:    (64, 10)    adds the bias b to every row

Stretching is almost free: as you saw in puzzle d, a stretched axis is just
a stride of 0, so no data is copied.

The rules hold for every elementwise operation, not just the operators:
`np.maximum(a, b)`, `np.where(mask, a, b)` and friends broadcast too. To
check shapes without making any arrays, ask NumPy directly:
`np.broadcast_shapes((64, 10), (10,))` returns `(64, 10)`, and raises the
same ValueError if the shapes don't fit.

When the axes don't line up the way you want, insert size-1 axes yourself
with `None` (or `keepdims=True` on a reduction, see puzzle g). To combine
every element of `a` (shape (m,)) with every element of `b` (shape (n,)):

    a[:, None]:   (m, 1)
    b[None, :]:   (1, n)
    result:       (m, n)   result[i, j] combines a[i] and b[j]

The danger: broadcasting also succeeds when you didn't mean it to. If a
model returns predictions of shape (N, 1) and you subtract targets of shape
(N,), you get an (N, N) matrix of every prediction minus every target. No
error, and taking its mean even gives you a number.

This file has three parts. Work through them in order:

1. Which shapes broadcast (questions).
2. Read `pairwise_sq_distances`, a finished example, and answer the
   questions below it.
3. Fix the bugs in `mse` and `scale_rows`.

Answer the questions by setting the answer variables (they start out as
`None`). You may run code to check your answers. Give a shape as a tuple,
such as (3, 4), and an array as a (nested) list. If a line raises an error,
answer with the string "error".

Docs: https://numpy.org/doc/stable/user/basics.broadcasting.html

⭐ CORE: Q1a and the bug in `mse`.

DO NOT MODIFY THE FUNCTION SIGNATURES.
"""

import numpy as np


# ---------------------------------------------------------------------------
# 1. Which shapes broadcast (questions)
# ---------------------------------------------------------------------------

# ⭐ CORE
# Q1a. For each pair of shapes, give the shape of `a + b`, where `a` has the
#      first shape and `b` the second, or "error" if they don't broadcast.
#      (`()` is the shape of a single number.)
BROADCAST_SHAPES: dict[str, object] = {
    "(3, 4) + (4,)": (3, 4),
    "(3, 4) + (3,)": "error",
    "(3, 4) + (3, 1)": (3, 4),
    "(3, 1) + (1, 4)": (3, 4),
    "(5,) + (5, 1)": (5, 5),
    "(2, 3, 4) + (3, 4)": (2, 3, 4),
    "(2, 3, 4) + (2, 4)": "error",
    "(2, 3, 4) + (2, 1, 4)": (2, 3, 4),
    "(8, 1, 6, 1) + (7, 1, 5)": (8, 7, 6, 5),
    "() + (3, 3)": (3, 3),
}

# Q1b. What is `np.broadcast_shapes((8, 1, 3), (5, 1), (3,))`? Work it out
#      by hand first, then run it to check.
THREE_WAY_SHAPE = (8, 5, 3)

rows = np.array([1, 2, 3])
cols = np.array([10, 20])

# Q1c. What is `np.maximum(rows[:, None], cols // 10).tolist()`?
MAXIMUM_TABLE = [[1, 2], [2, 2], [3, 3]]


# ---------------------------------------------------------------------------
# 2. pairwise_sq_distances (finished example and questions)
# ---------------------------------------------------------------------------


def pairwise_sq_distances(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """
    Returns the squared Euclidean distance between every row of `X`, shape
    (m, d), and every row of `Y`, shape (n, d), as an (m, n) array:
    `D[i, j]` is the sum over k of (X[i, k] - Y[j, k]) ** 2.

    k-nearest neighbours, k-means and attention all start from a table of
    pairwise comparisons like this one.

    Example:
        >>> X = np.array([[0.0, 0.0], [1.0, 1.0]])
        >>> Y = np.array([[1.0, 0.0], [3.0, 4.0], [0.0, 0.0]])
        >>> pairwise_sq_distances(X, Y)
        array([[ 1., 25.,  0.],
               [ 1., 13.,  2.]])
    """

    # Give X a new axis for "which row of Y", and Y a new axis for "which
    # row of X", so that the two line up into an (m, n, d) block:
    #
    #   X[:, None, :]   (m, 1, d)
    #   Y[None, :, :]   (1, n, d)
    #   diff            (m, n, d)   diff[i, j] = X[i] - Y[j]
    diff = X[:, None, :] - Y[None, :, :]

    # Square every difference, then add up over the last axis (the d
    # features), which leaves one number per pair: (m, n).
    return (diff**2).sum(axis=-1)


# Q2a. `X` holds 1000 samples with 64 features and `Y` holds 500 samples
#      with 64 features. What is the shape of `diff` inside
#      `pairwise_sq_distances(X, Y)`?
DIFF_SHAPE = (1000, 500, 64)

# Broadcasting doesn't copy its *inputs*, but the *result* of the
# subtraction is a real, new array. With the X and Y from Q2a, `diff` takes
# 256 MB, which is why this approach runs out of memory for large m and n.

# Q2b. What would `pairwise_sq_distances(X, Y)` return if you wrote
#      `X[:, None, :] - Y[:, None, :]` instead, with the same X (1000, 64)
#      and Y (500, 64)? Give its shape, or "error".
WRONG_AXES_SHAPE = "error"


# ---------------------------------------------------------------------------
# 3. mse and scale_rows (fix the bugs)
# ---------------------------------------------------------------------------

# Each function has exactly one bug, and both are broadcasting going wrong
# without an error for some inputs. Fix each with the smallest change you
# can.


# ⭐ CORE
def mse(y_pred: np.ndarray, y_true: np.ndarray) -> float:
    """
    Returns the mean squared error between a model's predictions and the
    targets: the mean over all samples of (prediction - target) ** 2.

    The model returns `y_pred` with shape (N, 1), one column with one
    prediction per sample. The targets `y_true` have shape (N,).

    Example:
        >>> mse(np.array([[1.0], [2.0]]), np.array([1.0, 4.0]))
        2.0
    """

    errors = y_pred - y_true[:, None]
    return float((errors**2).mean())


def scale_rows(X: np.ndarray, s: np.ndarray) -> np.ndarray:
    """
    Multiplies every row `i` of `X`, shape (n, d), by the number `s[i]`,
    where `s` has shape (n,). Returns a new (n, d) array.

    Example:
        >>> scale_rows(np.array([[1.0, 1.0, 1.0], [1.0, 2.0, 3.0]]), np.array([2.0, 10.0]))
        array([[ 2.,  2.,  2.],
               [10., 20., 30.]])
    """

    return X * s[:, None]


if __name__ == "__main__":
    X = np.array([[0.0, 0.0], [1.0, 1.0]])
    Y = np.array([[1.0, 0.0], [3.0, 4.0], [0.0, 0.0]])
    print("pairwise_sq_distances:")
    print(pairwise_sq_distances(X, Y))

    print("\nmse:", mse(np.array([[1.0], [2.0]]), np.array([1.0, 4.0])), " expected 2.0")

    print("\nscale_rows on a square matrix:")
    print(scale_rows(np.array([[1.0, 1.0], [1.0, 1.0]]), np.array([2.0, 10.0])))
    print("  expected [[2, 2], [10, 10]]")
