"""
Memory Layout

Under every array there is one flat block of memory. So how does
`x[1, 2, 3]` find its element? Through the *strides*: one number per axis,
saying how many bytes to jump to move one step along that axis. The byte
offset of an element is

    offset of x[i, j, k] = i * strides[0] + j * strides[1] + k * strides[2]

A fresh array is stored in *row-major* order (also called C order): the
last axis changes fastest, like reading a book line by line. For a float32
array of shape (2, 3) the six elements sit in memory as

    x[0,0] x[0,1] x[0,2] x[1,0] x[1,1] x[1,2]

so one step along axis 1 is 4 bytes (one float32), one step along axis 0 is
12 bytes (a whole row), and `x.strides` is (12, 4).

Now the trick: a view doesn't move any data, it only gets new shape and
stride numbers. `x.T` just swaps the strides to (4, 12). Slicing with a step
multiplies a stride. That is why these operations are free.

An array is *contiguous* (C-contiguous, to be exact) when reading it in
row-major order walks through memory one element after the other with no
jumps and no gaps. `x.T` is not contiguous: reading its first row jumps 12
bytes at a time. This matters for two reasons:

- Speed. The CPU loads memory in chunks of 64 bytes (cache lines). Walking
  through contiguous memory uses every byte it loads; jumping around wastes
  most of them.
- Reshaping. `reshape` regroups elements in row-major order. If the array
  is not contiguous, there is no way to describe the new shape with strides
  alone, so `reshape` makes a copy, without an error or a warning.
  (PyTorch's `view` refuses and raises an error instead, and
  `.contiguous()` makes the copy explicitly.)

`x.strides` shows the strides, `x.flags["C_CONTIGUOUS"]` says whether `x` is
contiguous, and `np.ascontiguousarray(x)` returns a contiguous copy (or `x`
itself if it already is).

This file has four parts. Work through them in order:

1. Strides and offsets (questions).
2. Contiguity (questions).
3. Strides that repeat (questions).
4. 🎙️ Transcription: `byte_offset` is a worked example; you dictate
   `c_order_strides` and `is_c_contiguous`.

Answer the questions by setting the answer variables (they start out as
`None`). You may run code to check your answers. Give shapes and strides as
tuples, such as (12, 4).

Docs: https://numpy.org/doc/stable/reference/arrays.ndarray.html#internal-memory-layout-of-an-ndarray

⭐ CORE: Q1d, Q2a, Q2b and `c_order_strides`.

DO NOT MODIFY THE FUNCTION SIGNATURES.
"""

import numpy as np


# ---------------------------------------------------------------------------
# 1. Strides and offsets (questions)
# ---------------------------------------------------------------------------

x = np.zeros((2, 3, 4), dtype=np.float32)

# Q1a. What is `x.strides`?
X_STRIDES = None

# Q1b. At which byte offset from the start of the memory block is
#      `x[1, 2, 3]`?
OFFSET_OF_1_2_3 = None

# Q1c. What is `x[:, ::2].strides`?
X_STEP_STRIDES = None

# ⭐ CORE
# Q1d. What are the shape and the strides of `x.transpose(0, 2, 1)`? Give a
#      tuple (shape, strides).
X_TRANSPOSED_SHAPE_AND_STRIDES = None

# Q1e. Let `a = np.arange(24).reshape(2, 3, 4)`. What is `a.T[3, 1, 0]`?
A_T_ELEMENT = None


# ---------------------------------------------------------------------------
# 2. Contiguity (questions)
# ---------------------------------------------------------------------------

# ⭐ CORE
# Q2a. Let `m = np.zeros((4, 6))`. Which of these are C-contiguous? Give a
#      list of letters in alphabetical order.
#
#      A  m.T
#      B  m[1:3]
#      C  m[:, 1:3]
#      D  m[::2]
#      E  m[:, 0]
#      F  m.reshape(6, 4)
#      G  np.ascontiguousarray(m.T)
CONTIGUOUS = None

# ⭐ CORE
# Q2b. Does `m.T.reshape(-1)` share memory with `m`? Give True or False.
TRANSPOSE_RESHAPE_SHARES_MEMORY = None


# ---------------------------------------------------------------------------
# 3. Strides that repeat (questions)
# ---------------------------------------------------------------------------

# Nothing forces strides to be "row-major" or even positive. A stride of 0
# means "stepping along this axis doesn't move at all", so every position
# along it shows the same memory. A stride smaller than a row means rows
# overlap.

signal = np.arange(6)  # int64, 8 bytes per element
windows = np.lib.stride_tricks.sliding_window_view(signal, 3)
tiled = np.broadcast_to(np.arange(3), (1000, 3))

# Q3a. What is `windows.tolist()`?
WINDOWS = None

# Q3b. What is `windows.strides`?
WINDOWS_STRIDES = None

# Q3c. What is `tiled.strides`? (Puzzle f comes back to this: it is how
#      broadcasting "stretches" an array without copying it.)
TILED_STRIDES = None


# ---------------------------------------------------------------------------
# 4. 🎙️ Transcription: byte_offset, c_order_strides and is_c_contiguous
# ---------------------------------------------------------------------------

# In this part you don't type the code yourself. You tell your AI agent what
# the code should do, in precise English, and the agent writes down exactly
# what you said. It won't fill in a missing step or fix a mistake in your
# logic. No agent? Write your dictation as comments first, then the code
# under each comment.
#
# Say one sentence per step about what the step does to the shapes or
# strides. Not "result plus-equals i times s" (that's just code read out
# loud), but not "compute the offset" either (that skips all the thinking).
# The dictation of `byte_offset` below shows the right level.


def byte_offset(index: tuple[int, ...], strides: tuple[int, ...]) -> int:
    """
    Returns the byte offset of the element at `index` in an array with the
    given `strides`.

    This is the dictation that produced the code below:

        Multiply each index by the stride of its axis, and return the sum
        of these products.

    Example:
        >>> byte_offset((2, 1, 3), (80, 40, 8))
        224
    """

    # Multiply each index by the stride of its axis...
    products = [i * s for i, s in zip(index, strides)]
    # ...and return the sum of these products.
    return sum(products)


# ⭐ CORE
def c_order_strides(shape: tuple[int, ...], itemsize: int) -> tuple[int, ...]:
    """
    Returns the strides of a fresh, C-contiguous array with this `shape`
    whose elements take `itemsize` bytes each. For every shape without a 0
    in it, this must match what NumPy reports in
    `np.zeros(shape, dtype).strides`.

    Example:
        >>> c_order_strides((3, 2, 5), 8)
        (80, 40, 8)
        >>> c_order_strides((5,), 8)
        (8,)
    """

    # Your solution here.
    pass


def is_c_contiguous(shape: tuple[int, ...], strides: tuple[int, ...], itemsize: int) -> bool:
    """
    Says whether an array with this `shape`, `strides` and `itemsize` is
    C-contiguous, the same way `x.flags["C_CONTIGUOUS"]` does.

    The array is C-contiguous if its strides are the ones a fresh array of
    that shape would have, except that axes of size 1 don't count: you
    never step along them, so their stride can be anything. An array with
    no elements at all (some size is 0) also counts as C-contiguous.

    Example:
        >>> is_c_contiguous((2, 3), (24, 8), 8)
        True
        >>> is_c_contiguous((3, 2), (8, 24), 8)      # a transposed (2, 3)
        False
        >>> is_c_contiguous((4, 1, 6), (48, 999, 8), 8)
        True
    """

    # Your solution here.
    pass


if __name__ == "__main__":
    print("byte_offset:    ", byte_offset((2, 1, 3), (80, 40, 8)), " expected 224")
    print("c_order_strides:", c_order_strides((3, 2, 5), 8), " expected (80, 40, 8)")
    print("is_c_contiguous:", is_c_contiguous((3, 2), (8, 24), 8), " expected False")
