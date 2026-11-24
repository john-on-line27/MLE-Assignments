"""
Matrix Multiplication

`*` multiplies elementwise (with broadcasting). `@` is matrix
multiplication. For two matrices, `(n, k) @ (k, m)` gives `(n, m)`: entry
`[i, j]` is the dot product of row i of the left matrix and column j of the
right one, so the inner sizes (both k) must match.

`@` also works on stacks of matrices, which is how batched ML code uses
it. Only the *last two* axes take part in the matrix product. All axes in
front of them are batch axes, and they broadcast like in puzzle f:

    (8, 4, 3) @ (8, 3, 5)  ->  (8, 4, 5)   8 separate products
    (8, 4, 3) @    (3, 5)  ->  (8, 4, 5)   the same (3, 5) matrix for all 8

1-D arrays are special: on the left, a vector of shape (k,) acts as a row
(1, k); on the right, it acts as a column (k, 1); and that extra axis is
removed from the result again.

Two traps that come up all the time:

- `.T` reverses *all* axes. For a single matrix that is the transpose you
  want, but for a stack of shape (B, n, m) it gives (m, n, B), which mixes
  the batch axis into the matrix. To transpose every matrix in a stack, swap
  only the last two axes: `x.swapaxes(-1, -2)` or `x.transpose(0, 2, 1)`.
- Weight layout. A linear layer computes `X @ W + b` with X of shape
  (N, in) and W of shape (in, out). PyTorch stores the weight the other way
  round, as (out, in), and computes `X @ W.T + b`. If W happens to be
  square, using the wrong one gives no error, just wrong numbers.

The lecture showed that a matrix product is really a combination of the
operations you already know: reshape (or insert axes), broadcast, multiply
elementwise, and sum. In part 2 you dictate exactly that.

This file has three parts. Work through them in order:

1. Shapes (questions).
2. 🎙️ Transcription: `row_dots` is a worked example; you dictate
   `matmul_by_broadcasting`.
3. Fix the bugs in `linear` and `attention_scores`.

Answer the questions by setting the answer variables (they start out as
`None`). You may run code to check your answers. Give a shape as a tuple,
such as (3, 4). If a line raises an error, answer with the string "error".

Docs: https://numpy.org/doc/stable/reference/generated/numpy.matmul.html

⭐ CORE: Q1a, `matmul_by_broadcasting` and the bug in `attention_scores`.

DO NOT MODIFY THE FUNCTION SIGNATURES.
"""

import numpy as np


# ---------------------------------------------------------------------------
# 1. Shapes (questions)
# ---------------------------------------------------------------------------

# ⭐ CORE
# Q1a. For each line, `a` has the first shape and `b` the second. Give the
#      shape of the result, or "error".
MATMUL_SHAPES: dict[str, object] = {
    "(4, 3) @ (3, 5)": None,
    "(4, 3) @ (4, 3)": None,
    "(4, 3) * (4, 3)": None,
    "(3,) @ (3, 5)": None,
    "(4, 3) @ (3,)": None,
    "(3,) @ (3,)": None,
    "(8, 4, 3) @ (2, 3, 5)": None,
    "(2, 1, 4, 3) @ (8, 3, 5)": None,
}

# Q1b. `X` holds n samples as rows, shape (n, d). Which expression gives the
#      (n, n) table of dot products between every pair of samples? Give a
#      letter.
#
#      A  X @ X.T
#      B  X.T @ X
#      C  X * X
#      D  (X * X).sum(axis=1)
SAMPLE_DOTS = None


# ---------------------------------------------------------------------------
# 2. 🎙️ Transcription: row_dots and matmul_by_broadcasting
# ---------------------------------------------------------------------------

# As in puzzle d, you dictate the code to your AI agent in precise English,
# and it writes down exactly what you said (no agent? write your dictation
# as comments, then the code under each one). Dictate in terms of shapes and
# axes, like the dictation of `row_dots` below: say which axes to insert,
# what to multiply, and which axis to sum over.


def row_dots(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """
    Returns the dot product of each row of `X` with the matching row of `Y`.
    Both have shape (n, d); the result has shape (n,).

    This is the dictation that produced the code below:

        Multiply X and Y elementwise; both are n by d. Then sum over the
        last axis, the d features, which leaves one number per row.

    Example:
        >>> row_dots(np.array([[1.0, 2.0], [3.0, 4.0]]), np.array([[1.0, 1.0], [0.0, 2.0]]))
        array([3., 8.])
    """

    # Multiply X and Y elementwise; both are n by d.
    products = X * Y
    # Then sum over the last axis, which leaves one number per row.
    return products.sum(axis=-1)


# ⭐ CORE
def matmul_by_broadcasting(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """
    Returns the matrix product of `A`, shape (n, k), and `B`, shape (k, m),
    as an (n, m) array, using only axis insertion, broadcasting, elementwise
    multiplication and a sum. Don't use `@`, `np.matmul`, `np.dot` or
    `np.einsum`.

    Hint: entry [i, j] is the sum over p of A[i, p] * B[p, j]. Build an
    array with one axis for i, one for p and one for j, holding every
    product A[i, p] * B[p, j], then sum the p axis away.

    Example:
        >>> matmul_by_broadcasting(np.array([[1, 2, 3], [4, 5, 6]]), np.array([[1, 0], [0, 1], [1, 1]]))
        array([[ 4,  5],
               [10, 11]])
    """

    # Your solution here.
    pass


# ---------------------------------------------------------------------------
# 3. linear and attention_scores (fix the bugs)
# ---------------------------------------------------------------------------

# Each function has exactly one bug. Fix each with the smallest change you
# can.


def linear(X: np.ndarray, W: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    A linear layer with weights stored the PyTorch way. `X` has shape
    (N, in), `W` has shape (out, in) and `b` has shape (out,). Output `[n, o]`
    is the dot product of sample n with row o of `W`, plus `b[o]`. Returns
    shape (N, out).

    Example:
        >>> X = np.array([[1.0, 2.0]])
        >>> W = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])  # out=3, in=2
        >>> linear(X, W, np.zeros(3))
        array([[1., 2., 3.]])
    """

    return X @ W + b


# ⭐ CORE
def attention_scores(Q: np.ndarray, K: np.ndarray) -> np.ndarray:
    """
    The first step of attention. `Q` (queries) and `K` (keys) both have
    shape (B, T, D): a batch of B sequences, each with T vectors of D
    features. For every sequence b, returns the (T, T) table of dot products
    between every query and every key, divided by sqrt(D):

        scores[b, i, j] = (Q[b, i] . K[b, j]) / sqrt(D)

    Returns shape (B, T, T).
    """

    D = Q.shape[-1]
    return Q @ K.T / np.sqrt(D)


if __name__ == "__main__":
    from _demo import run

    run("row_dots:", lambda: row_dots(np.array([[1.0, 2.0], [3.0, 4.0]]), np.array([[1.0, 1.0], [0.0, 2.0]])))
    print("  expected [3. 8.]")

    print()
    run("matmul_by_broadcasting:", lambda: matmul_by_broadcasting(np.array([[1, 2, 3], [4, 5, 6]]), np.array([[1, 0], [0, 1], [1, 1]])))
    print("  expected [[4, 5], [10, 11]]")

    X = np.array([[1.0, 2.0]])
    W = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    print()
    run("linear:", lambda: linear(X, W, np.zeros(3)))
    print("  expected [[1. 2. 3.]]")

    rng = np.random.default_rng(0)
    Q = rng.normal(size=(2, 5, 4))
    K = rng.normal(size=(2, 5, 4))
    print()
    run("attention_scores shape:", lambda: attention_scores(Q, K).shape)
    print("  expected (2, 5, 5)")
