"""
Indexing

Indexing is how you pick parts out of an array. NumPy has two kinds, and
they behave differently.

*Basic indexing* uses integers, slices (`1:4`, `::2`), `None` and `...`:

- An integer picks one position and *removes* that axis: if `X` has shape
  (8, 3), then `X[0]` has shape (3,).
- A slice keeps the axis, even if it only selects one position: `X[0:1]`
  has shape (1, 3).
- `None` inserts a new axis of size 1, and `...` stands for "all the axes
  I didn't mention".

*Advanced indexing* uses an array of integers or an array of booleans:

- An integer array picks the positions it lists, in that order, repeats
  allowed. The result has the shape of the index array: `E[tokens]` with
  `tokens` of shape (2, 5) picks 10 rows of `E` and arranges them as
  (2, 5, ...). This is exactly how an embedding layer looks up tokens: it
  holds a table `E` with one vector of numbers per token (word or word
  piece), and picks the rows for the tokens in the input.
- Integer arrays in two axes are paired up position by position:
  `P[[0, 1], [2, 0]]` gives `[P[0, 2], P[1, 0]]`, not a 2 x 2 block.
- A boolean array (a *mask*) of the same shape picks the positions where it
  is True. The result is always 1-D, because the selected elements don't
  form a grid any more. A mask over the first axis only, with one bool per
  row, picks whole rows instead. `np.where(mask, a, b)` keeps the shape: it
  takes `a` where the mask is True and `b` elsewhere.

Combine masks with `&`, `|` and `~`, and put each comparison in
parentheses `( )`:
`(x > 0) & (x < 5)`. Python's `and`, `or` and `not` don't work on arrays.

This file has four parts. Work through them in order:

1. Shapes (questions).
2. Picking with integer arrays (questions).
3. Masks and `np.where` (questions).
4. Fix the bugs in `cross_entropy` and `prune_weights`.

Answer the questions by setting the answer variables (they start out as
`None`). You may run code to check your answers. Give a shape as a tuple,
such as (3, 4), and an array as a list, such as [1, 2, 3]. If a line raises
an error, answer with the string "error".

Docs: https://numpy.org/doc/stable/user/basics.indexing.html

⭐ CORE: Q1 and the bugs in `cross_entropy` and `prune_weights`.

DO NOT MODIFY THE FUNCTION SIGNATURES.
"""

import numpy as np


# ---------------------------------------------------------------------------
# 1. Shapes (questions)
# ---------------------------------------------------------------------------

# A batch of 8 RGB images of 32 x 32 pixels, laid out as
# (batch, channel, height, width).
X = np.zeros((8, 3, 32, 32))

# ⭐ CORE
# Q1. Fill in the shape of each expression.
SHAPES: dict[str, object] = {
    "X[0]": (3, 32, 32),
    "X[0:1]": (1, 3, 32, 32),
    "X[:, 0]": (8, 32, 32),
    "X[..., 0]": (8, 3, 32),
    "X[:, :, ::2, ::2]": (8, 3, 16, 16),
    "X[:, None]": (8, 1, 3, 32, 32),
    "X[[0, 2, 2]]": (3, 3, 32, 32),
    "X[:, [0]]": (8, 1, 32, 32),
    "X[-1, -1, -1]": (32,),
}


# ---------------------------------------------------------------------------
# 2. Picking with integer arrays (questions)
# ---------------------------------------------------------------------------

# A classifier's predicted probabilities for 4 samples and 3 classes (one row
# per sample), and the true class of each sample.
probs = np.array(
    [
        [0.1, 0.7, 0.2],
        [0.5, 0.3, 0.2],
        [0.2, 0.2, 0.6],
        [0.3, 0.4, 0.3],
    ]
)
labels = np.array([1, 0, 2, 1])

# Q2a. What is `probs[np.arange(4), labels]`? Give a list.
PICKED = [0.7, 0.5, 0.6, 0.4]

# An embedding table with one 16-dimensional vector for each of 100 tokens,
# and a batch of 2 token sequences of length 3.
embeddings = np.zeros((100, 16))
tokens = np.array([[5, 7, 7], [1, 0, 99]])

# Q2b. What is the shape of `embeddings[tokens]`?
EMBEDDED_SHAPE = (2, 3, 16)


# ---------------------------------------------------------------------------
# 3. Masks and np.where (questions)
# ---------------------------------------------------------------------------

x = np.array([3, -1, 4, -1, 5, -9])

# Q3a. What is `x[(x > 0) & (x < 5)]`? Give a list.
BETWEEN = [3, 4]

# Q3b. What is `x[(x > 0) and (x < 5)]`? Give a list, or "error".
WITH_AND = "error"

# Q3c. What is `np.where(x > 0, x, 0)`? Give a list.
WHERE_RESULT = [3, 0, 4, 0, 5, 0]

# Q3d. `data` has shape (6, 4), one row per sample, and `y` holds the label
#      of each sample. What is the shape of `data[y == 1]`?
data = np.arange(24).reshape(6, 4)
y = np.array([0, 1, 1, 0, 1, 0])
MASKED_ROWS_SHAPE = (3, 4)


# ---------------------------------------------------------------------------
# 4. cross_entropy and prune_weights (fix the bugs)
# ---------------------------------------------------------------------------

# Each function has exactly one bug. Fix each one with the smallest change
# you can.


# ⭐ CORE
def cross_entropy(probs: np.ndarray, labels: np.ndarray) -> float:
    """
    Returns the cross-entropy loss of a classifier: for each sample, take
    the probability the model gave to the *true* class, then return the
    mean of -log(probability) over all samples.

    `probs` has shape (N, C), one row of class probabilities per sample.
    `labels` has shape (N,) and holds the true class of each sample.

    Example:
        >>> cross_entropy(np.array([[0.5, 0.5], [0.1, 0.9]]), np.array([0, 1]))
        0.39925...   # the mean of -log(0.5) and -log(0.9)
    """

    true_class_probs = probs[np.arange(len(labels)), labels]
    return float(-np.log(true_class_probs).mean())


# ⭐ CORE
def prune_weights(W: np.ndarray, threshold: float) -> np.ndarray:
    """
    Returns a copy of the weight matrix `W` in which every weight whose
    absolute value is below `threshold` is set to 0. The result has the
    same shape as `W`, and `W` itself is not changed.

    Example:
        >>> prune_weights(np.array([[0.5, -0.01], [0.02, -2.0]]), 0.1)
        array([[ 0.5,  0. ],
               [ 0. , -2. ]])
    """

    return np.where(np.abs(W) >= threshold, W, 0)


if __name__ == "__main__":
    print("cross_entropy:", cross_entropy(np.array([[0.5, 0.5], [0.1, 0.9]]), np.array([0, 1])))
    print("  expected:    0.3992...")
    print("prune_weights:")
    W = np.array([[0.5, -0.01], [0.02, -2.0]])
    print(prune_weights(W, 0.1))
    print("  expected a 2 x 2 array: [[0.5, 0.0], [0.0, -2.0]]")
    print("W after prune_weights:", W.tolist())
    print("  expected W unchanged:  [[0.5, -0.01], [0.02, -2.0]]")
