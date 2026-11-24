"""
Arrays and dtypes

A Python list stores pointers to objects scattered around memory. A NumPy
array is the opposite: one flat block of memory where every element has the
same type and the same size, sitting right next to the previous one. On top
of that block, the array keeps a little metadata:

- the *shape*, which says how to read the flat block as rows, columns,
  images, batches and so on, e.g. `(64, 28, 28)`;
- the *dtype*, which says what each element is (`float64`, `float32`,
  `int64`, `uint8`, `bool`, ...) and so how many bytes it takes.

The dtype matters more than it looks. It decides how much memory your data
needs, and NumPy gives no error or warning when an operation loses
information: an integer array drops the decimals you write into it, and a
`uint8` image wraps around when a pixel goes past 255.

This file has three parts. Work through them in order:

1. Creating arrays (questions).
2. Dtypes: memory and mixing (questions).
3. Fix the bugs in `brighten` and `scale_to_max`.

Answer the questions by setting the answer variables (they start out as
`None`). You may run code to check your answers. Give a dtype as a string,
such as "float64", and an array as a list, such as [1, 2, 3].

Docs:
- Array creation: https://numpy.org/doc/stable/user/basics.creation.html
- Dtypes: https://numpy.org/doc/stable/user/basics.types.html
- Random numbers: https://numpy.org/doc/stable/reference/random/generator.html

⭐ CORE: Q1c, Q1e, Q2a, Q2f, Q2j and the bug in `brighten`.

DO NOT MODIFY THE FUNCTION SIGNATURES.
"""

import numpy as np


# ---------------------------------------------------------------------------
# 1. Creating arrays (questions)
# ---------------------------------------------------------------------------


def creation_demo():
    a = np.zeros((2, 3))
    b = np.arange(2, 10, 3)
    c = np.linspace(0, 1, 5)
    d = np.full((2, 2), 7)
    e = np.eye(3)
    f = np.zeros_like(b)
    return a, b, c, d, e, f


# Q1a. What values does `b` hold? Give a list.
ARANGE_VALUES = [2, 5, 8]

# Q1b. What values does `c` hold? Give a list.
LINSPACE_VALUES = [0.0, 0.25, 0.5, 0.75, 1.0]

# ⭐ CORE
# Q1c. Which of the arrays `a` to `f` have an integer dtype? Give a list of
#      names as strings, in alphabetical order, e.g. ["a", "c"].
INTEGER_ARRAYS = ["b", "d", "f"]


def random_demo():
    rng = np.random.default_rng(seed=0)
    first = rng.random(3)
    rng = np.random.default_rng(seed=0)
    second = rng.random(3)
    third = rng.random(3)
    return first, second, third


# A generator (`rng`) produces a fixed sequence of numbers that depends only
# on its seed. That is how ML code makes "random" experiments repeatable.

# Q1d. Do `first` and `second` hold exactly the same numbers? Give True or
#      False.
FIRST_EQUALS_SECOND = True

# ⭐ CORE
# Q1e. Do `second` and `third` hold exactly the same numbers? Give True or
#      False.
SECOND_EQUALS_THIRD = False

# Q1f. `rng.integers(0, 10, size=1000)` draws 1000 random integers. What is
#      the largest value it can ever return?
INTEGERS_MAX = 9

# `np.empty((2, 3))` is the fastest constructor: it reserves the memory for
# the array and stops there. Use it only when you overwrite every element
# right away.

# Q1g. Is every element of `np.empty((2, 3))` guaranteed to be 0? Give True
#      or False.
EMPTY_IS_ZEROS = False


# ---------------------------------------------------------------------------
# 2. Dtypes: memory and mixing (questions)
# ---------------------------------------------------------------------------

# Every element of an array takes `arr.itemsize` bytes, so the whole array
# takes `arr.size * arr.itemsize` bytes (also available as `arr.nbytes`).
# A float64 takes 8 bytes, a float32 takes 4 and a uint8 takes 1. You can
# ask a dtype directly, without making an array: `np.dtype(np.float32)` is
# the dtype object, and `np.dtype(np.float32).itemsize` is 4.
#
# The MNIST training set has 60,000 grayscale images of 28 x 28 pixels.

# ⭐ CORE
# Q2a. How many bytes does MNIST take as a float64 array of shape
#      (60000, 28, 28)? Give an int.
MNIST_FLOAT64_BYTES = 376320000

# Q2b. What is `np.dtype(np.float16).itemsize`?
FLOAT16_ITEMSIZE = 2


# When an operation combines two arrays of different dtypes, NumPy picks a
# result dtype that can hold both, or comes as close to that as it can,
# which usually means the "bigger" one.
# A plain Python number (like `2.0`) is weaker: it adapts to the array's
# dtype where it can, instead of making the result bigger.

ints = np.array([1, 2, 3])  # int64
floats32 = np.array([1.0, 2.0, 3.0], dtype=np.float32)

# Q2c. What is the dtype of `ints / 2`?
DTYPE_INT_DIVIDE = "float64"

# Q2d. What is the dtype of `ints // 2`?
DTYPE_INT_FLOOR_DIVIDE = "int64"

# Q2e. What is the dtype of `floats32 * 2.0`?
DTYPE_FLOAT32_TIMES_PYTHON_FLOAT = "float32"

# ⭐ CORE
# Q2f. What is the dtype of `ints + floats32`?
DTYPE_INT64_PLUS_FLOAT32 = "float64"

# Math functions like `np.exp`, `np.log` and `np.sqrt` work element by
# element, and so do the operators `**` and `%`. A math function needs
# floats, so it turns int32 and int64 arrays into float64, but it leaves a
# float32 array float32.

# Q2g. What is `(ints ** 2 % 3).tolist()`? Work it out before you run it.
POWER_MOD_VALUES = [1, 1, 0]


def truncation_demo():
    x = np.array([1, 2, 3])
    x[0] = 2.9
    return x


def wraparound_demo():
    img = np.array([200, 100, 50], dtype=np.uint8)
    return img + img, img - 100


# Q2h. What does `truncation_demo()` return? Give a list.
TRUNCATION_RESULT = [2, 2, 3]

# Q2i. What does `wraparound_demo()` return? Give a tuple of two lists.
#      (A uint8 holds the values 0 to 255, and arithmetic on it wraps
#      around, like a clock: 255 + 1 gives 0.)
WRAPAROUND_RESULT = ([144, 200, 100], [100, 0, 206])

# ⭐ CORE
# Q2j. Floats are stored in binary, so most decimals are slightly off. What
#      are `0.1 + 0.2 == 0.3` and `np.allclose(0.1 + 0.2, 0.3)`? Give a
#      tuple of two bools. (This is why tests compare floats with
#      `np.allclose` instead of `==`.)
FLOAT_COMPARISON = (False, True)


# ---------------------------------------------------------------------------
# 3. brighten and scale_to_max (fix the bugs)
# ---------------------------------------------------------------------------

# Each of these two functions has exactly one bug, and each bug is a dtype
# problem from part 2. Fix each one with the smallest change you can. To
# check your fixes, run this file (`uv run python a_arrays_and_dtypes.py`),
# which prints each function's output next to the expected one, or submit
# (`make submit-a`) and look at the results on the course website.


# ⭐ CORE
def brighten(img: np.ndarray, amount: int) -> np.ndarray:
    """
    Makes a uint8 image brighter by adding `amount` (between 0 and 255) to
    every pixel. Pixels that would go above 255 are set to 255. Returns a
    new uint8 array of the same shape.

    Example:
        >>> brighten(np.array([10, 200, 250], dtype=np.uint8), 50)
        array([ 60, 250, 255], dtype=uint8)
    """

    brighter = img.astype(np.uint16) + amount
    return np.clip(brighter, 0, 255).astype(np.uint8)


def scale_to_max(x: np.ndarray) -> np.ndarray:
    """
    Divides every value of a non-negative array by the largest value, so
    that the largest value becomes 1. Works for integer and float input, and
    always returns a float64 array of the same shape. The input is not
    changed.

    Example:
        >>> scale_to_max(np.array([1, 2, 4]))
        array([0.25, 0.5 , 1.  ])
    """

    out = np.zeros_like(x, dtype=float)

    out[...] = x / x.max()
    return out


if __name__ == "__main__":
    print("brighten:    ", brighten(np.array([10, 200, 250], dtype=np.uint8), 50))
    print("  expected:   [ 60 250 255]")
    print("scale_to_max:", scale_to_max(np.array([1, 2, 4])))
    print("  expected:   [0.25 0.5  1.  ]")
