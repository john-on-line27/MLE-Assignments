"""
Reductions and Axes

A reduction walks along one axis and collapses it into a single number:
`sum`, `mean`, `max`, `min`, `std`, and `argmax`/`argmin` (which return the
*position* of the largest or smallest value instead of the value itself).

The rule to remember: the axis you name is the axis that disappears. For
`X` of shape (N, D), one row per sample and one column per feature:

- `X.mean(axis=0)` averages over the samples and has shape (D,): one mean
  per feature.
- `X.mean(axis=1)` averages over the features and has shape (N,): one mean
  per sample.
- `X.mean()` averages over everything and gives a single number.

You can name several axes at once with a tuple, like `axis=(0, 2, 3)`.

With `keepdims=True` the collapsed axis stays, with size 1: `X.mean(axis=1,
keepdims=True)` has shape (N, 1). That is exactly the shape that
broadcasts back against `X` (puzzle f), so `X - X.mean(axis=1,
keepdims=True)` subtracts each row's own mean from that row.

`cumsum` is related but doesn't collapse anything: it replaces each value
by the running total along the axis.

Watch out for two functions with almost the same name. `np.max(x, axis)`
is a reduction: the largest value *along an axis*. `np.maximum(a, b)` is
elementwise: the larger of two values at every position, so
`np.maximum(x, 0)` is ReLU, the function that sets every negative value to
0. Because `np.max(x, 0)` means "max along axis 0", mixing them up gives no
error, just an array of the wrong shape.

Many ML operations differ *only* in the axes they reduce over, like batch
normalization and layer normalization in part 2.

This file has three parts. Work through them in order:

1. Which axis disappears (questions).
2. Batch norm and layer norm (questions).
3. Fix the bugs in `softmax` and `accuracy`.

Answer the questions by setting the answer variables (they start out as
`None`). You may run code to check your answers. Give a shape as a tuple,
such as (3, 4), and an array as a (nested) list.

Docs: https://numpy.org/doc/stable/reference/routines.statistics.html

⭐ CORE: Q2a, Q2b and the bug in `softmax`.

DO NOT MODIFY THE FUNCTION SIGNATURES.
"""

import numpy as np


# ---------------------------------------------------------------------------
# 1. Which axis disappears (questions)
# ---------------------------------------------------------------------------

# A batch of 8 RGB images of 32 x 32 pixels: (batch, channel, height, width).
X = np.zeros((8, 3, 32, 32))

# Q1a. Fill in the shape of each expression.
SHAPES: dict[str, object] = {
    "X.sum()": None,
    "X.mean(axis=0)": None,
    "X.mean(axis=1)": None,
    "X.max(axis=-1)": None,
    "X.reshape(8, -1).argmax(axis=1)": None,
    "np.cumsum(X, axis=2)": None,
}

M = np.array([[1, 5, 3], [4, 2, 6]])

# Q1b. What is `M.sum(axis=0)`? Give a list.
M_SUM_AXIS_0 = None

# Q1c. What is `M.max(axis=1)`? Give a list.
M_MAX_AXIS_1 = None

# Q1d. What is `M.argmax(axis=0)`? Give a list.
M_ARGMAX_AXIS_0 = None

# Q1e. What is `M.argmax()`, with no axis? Give an int.
M_ARGMAX = None

# Q1f. What is `M.cumsum(axis=1).tolist()`?
M_CUMSUM_AXIS_1 = None

# The next questions combine an elementwise step with a reduction. Work each
# one out in your head first: write down the array after the elementwise
# step, then reduce it. Then run the line to check.

# Q1g. What are `np.max(M, 0).tolist()` and `np.maximum(M, 0).tolist()`?
#      Give a tuple of two lists.
MAX_VS_MAXIMUM = None

# Q1h. What is `np.maximum(M - 3, 0).sum()`? Give an int.
M_SHIFTED_RELU_SUM = None

# Q1i. What is `np.clip(M, 2, 5).sum(axis=1).tolist()`?
M_CLIPPED_ROW_SUMS = None

# Q1j. What is `(M % 2 == 1).sum(axis=1).tolist()`?
M_ODD_COUNTS = None


# ---------------------------------------------------------------------------
# 2. Batch norm and layer norm (questions)
# ---------------------------------------------------------------------------

# Batch normalization and layer normalization both subtract a mean and
# divide by a standard deviation. They differ only in what they average
# over. For a batch of images of shape (N, C, H, W):
#
# - Batch normalization computes one mean per *channel*, over all images in
#   the batch and all pixel positions.
# - Layer normalization computes one mean per *image*, over all of that
#   image's channels and pixel positions.

# ⭐ CORE
# Q2a. Which `axis` tuple gives the batch norm means, `X.mean(axis=...)`?
BATCH_NORM_AXES = None

# ⭐ CORE
# Q2b. Which `axis` tuple gives the layer norm means?
LAYER_NORM_AXES = None

# Q2c. To subtract the batch norm means from X, you need them with
#      `keepdims=True`. What is their shape then, for X of shape
#      (N, C, H, W) = (8, 3, 32, 32)?
BATCH_NORM_KEEPDIMS_SHAPE = None


# ---------------------------------------------------------------------------
# 3. softmax and accuracy (fix the bugs)
# ---------------------------------------------------------------------------

# Each of these two functions has exactly one bug, and each bug is about
# axes. Both bugs hide for some inputs, so don't trust a single example.
# Fix each with the smallest change you can.


# ⭐ CORE
def softmax(logits: np.ndarray) -> np.ndarray:
    """
    Applies softmax to every row of `logits` (the raw class scores a model
    outputs, one row per sample), shape (n, C): row i of the result is
    exp(logits[i]) divided by the sum of exp(logits[i]), so every row is a
    probability distribution over the C classes.

    Subtracting the same number from every entry of a row doesn't change
    that row's softmax, so the code subtracts the largest value first. That
    keeps exp() from overflowing.

    Example:
        >>> softmax(np.array([[1000.0, 1000.0], [0.0, np.log(3.0)]]))
        array([[0.5 , 0.5 ],
               [0.25, 0.75]])
    """

    shifted = logits - logits.max()
    e = np.exp(shifted)
    return e / e.sum(axis=1, keepdims=True)


def accuracy(logits: np.ndarray, labels: np.ndarray) -> float:
    """
    Returns the fraction of samples whose predicted class is the true class.
    `logits` has shape (n, C), one row of class scores per sample, and the
    predicted class is the one with the highest score. `labels` has shape
    (n,) and holds the true classes.

    Example:
        >>> accuracy(np.array([[0.1, 2.0, 0.3], [5.0, 1.0, 0.0]]), np.array([1, 2]))
        0.5
    """

    predictions = logits.argmax(axis=0)
    return float((predictions == labels).mean())


if __name__ == "__main__":
    from _demo import run

    run("softmax:", lambda: softmax(np.array([[1000.0, 1000.0], [0.0, np.log(3.0)]])))
    print("  expected [[0.5, 0.5], [0.25, 0.75]]")

    print()
    run("accuracy:", lambda: accuracy(np.array([[0.1, 2.0, 0.3], [5.0, 1.0, 0.0]]), np.array([1, 2])))
    print("  expected 0.5")
