"""
Reshape and Transpose

`reshape` and `transpose` both change an array's shape, and they are easy
to mix up, because often both of them give you the shape you asked for. But
they do very different things:

- `reshape` keeps the elements in their reading order (row-major) and only
  regroups them. Think of pouring the elements out in a line and refilling
  them into a box of the new shape. `np.arange(6).reshape(2, 3)` is
  [[0, 1, 2], [3, 4, 5]], and reshaping that to (3, 2) gives
  [[0, 1], [2, 3], [4, 5]]. One size can be -1, meaning "whatever is left".
- `transpose` reorders the *axes*. `x.transpose(0, 2, 1)` means "the new
  axis 0 is the old axis 0, the new axis 1 is the old axis 2, the new axis 2
  is the old axis 1". Elements keep their neighbours along each axis; only
  the axes change places. `x.T` reverses all axes.

Using `reshape` where you needed `transpose` is one of the most common bugs
in ML code. Nothing crashes: the shape is right, but the numbers are
scrambled, and the model just trains badly.

A few more tools that only change the shape:

- `np.squeeze(x)` removes axes of size 1; `np.squeeze(x, axis=k)` removes
  only axis `k`. `np.expand_dims(x, k)` and `x[:, None]` insert one.
- `np.concatenate([a, b], axis=k)` joins arrays along an *existing* axis.
  `np.stack([a, b], axis=k)` creates a *new* axis `k` and joins along it.
- `np.split(x, n, axis=k)` cuts `x` into `n` equal pieces along axis `k`
  (axis 0 if you leave out `axis=`).

Scrambled numbers are hard to spot; a scrambled picture isn't. A colour
picture is just an array of shape (H, W, 3): H rows, W columns, and three
numbers per pixel (red, green, blue). PyTorch stores the same picture as
(3, H, W), with the colour axis first. Many problems below come with a
picture. Run this file with the problem's name:

    uv run python e_reshape_and_transpose.py rotate_clockwise

and a window opens with the input, what your code makes, and the target.
The title over your result tells you whether it matches. You don't need to
read or write any plotting code: the drawing all happens in `_viz.py`.

This file has four parts. Work through them in order:

1. Reshape or transpose (questions, then `rotate_clockwise`). Q1e and Q1f
   come with pictures.
2. Shape tools (questions, then `merge_channels` and `swap_halves`).
3. Patches: read `cut_into_patches`, a finished example (and look at its
   picture, step by step), then write `contact_sheet` and `unscramble`.
4. Fix the bugs in `channels_last`, `merge_heads` and `scores_to_vector`.

Answer the questions by setting the answer variables (they start out as
`None`). You may run code to check your answers. Give a shape as a tuple,
such as (3, 4), and an array as a (nested) list. If a line raises an error,
answer with the string "error". Fill in the functions so that their
pictures match the targets.

Docs: https://numpy.org/doc/stable/reference/routines.array-manipulation.html

⭐ CORE: Q1f, `rotate_clockwise` and Q2a.

DO NOT MODIFY THE FUNCTION SIGNATURES.
"""

import argparse

import numpy as np

import _viz

# ---------------------------------------------------------------------------
# 1. Reshape or transpose (questions)
# ---------------------------------------------------------------------------

g = np.arange(12).reshape(3, 4)  # [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]]
a = np.arange(6).reshape(2, 3)  # [[0, 1, 2], [3, 4, 5]]

# Q1a. What is `g.reshape(4, -1).tolist()`?
RESHAPED = None

# Q1b. What is `a.T.tolist()`?
TRANSPOSED = None

# Q1c. What is `a.T.reshape(-1).tolist()`?
TRANSPOSED_FLAT = None

# Q1d. What is `a.reshape(3, 2).T.tolist()`? It has the same shape as `a`.
RESHAPED_THEN_TRANSPOSED = None


s = np.arange(24).reshape(2, 3, 4)

# Q1e. Look at the picture (`uv run python e_reshape_and_transpose.py Q1e`).
#      Every element is a tile with its number in it, darker the bigger the
#      number, and each slice along axis 0 gets its own grid, so `s` shows
#      up as s[0] and s[1]. Each panel 1-4 was made from `s` by one of:
#
#      A  s.transpose(1, 0, 2)
#      B  s.transpose(0, 2, 1)
#      C  s.swapaxes(0, 2)
#      D  s.reshape(3, 2, 4)
#
#      Fill in which letter made which panel.
STACKS: dict[int, str | None] = {1: None, 2: None, 3: None, 4: None}

# ⭐ CORE
# Q1f. Now with a picture (`... Q1f`). `img` has shape (H, W, 3) =
#      (64, 96, 3). Each panel 1-4 was made by one of:
#
#      A  img.transpose(1, 0, 2)
#      B  img.reshape(W, H, 3)
#      C  img.transpose(2, 0, 1).reshape(H, W, 3)
#      D  img[::-1]
#
#      Two of these are bugs you will meet in real code. Learn what they look
#      like: when a picture from your model looks like one of them, you know
#      which line to look for.
PICTURES: dict[int, str | None] = {1: None, 2: None, 3: None, 4: None}


# Rotate the picture a quarter turn clockwise (`... rotate_clockwise`).
# Don't use `np.rot90`: a transpose and a flip are enough. Careful: `img.T`
# reverses *all* axes, including the colour axis.


# ⭐ CORE
def rotate_clockwise(img: np.ndarray) -> np.ndarray:
    """Rotates an (H, W, 3) picture a quarter turn clockwise, giving (W, H, 3)."""

    # Your solution here.
    pass


# ---------------------------------------------------------------------------
# 2. Shape tools (questions)
# ---------------------------------------------------------------------------

x = np.zeros((4, 1, 3))

# ⭐ CORE
# Q2a. Fill in the shape of each expression, or "error".
SHAPES: dict[str, object] = {
    "np.squeeze(x)": None,
    "np.expand_dims(x, 0)": None,
    "np.concatenate([x, x], axis=0)": None,
    "np.stack([x, x], axis=0)": None,
    "np.concatenate([x, x], axis=-1)": None,
    "np.stack([x, x], axis=-1)": None,
    "x.reshape(2, -1)": None,
    "x.reshape(5, -1)": None,
    "np.split(np.arange(12), 3)[1]": None,
}


# Q2b. `A` and `B` both have shape (2, 2). You want the rows of both,
#      taking one from each in turn, as a (4, 2) array: A[0], B[0], A[1],
#      B[1]. Which of these lines give exactly that? Give a list of letters
#      in alphabetical order.
#
#      A  np.stack([A, B], axis=0).reshape(4, 2)
#      B  np.stack([A, B], axis=1).reshape(4, 2)
#      C  np.concatenate([A, B], axis=1).reshape(4, 2)
#      D  np.concatenate([A, B], axis=0)
INTERLEAVES = None


# You get the red, green and blue parts of a picture as three separate
# (H, W) arrays. Put them together into one (H, W, 3) colour picture
# (`... merge_channels`).


def merge_channels(r: np.ndarray, g: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Combines three (H, W) channels into one (H, W, 3) picture."""

    # Your solution here.
    pass


# Cut the picture into a left and a right half and put them back the other
# way round (`... swap_halves`). Use `np.split` and `np.concatenate`.


def swap_halves(img: np.ndarray) -> np.ndarray:
    """Swaps the left and right halves of an (H, W, 3) picture."""

    # Your solution here.
    pass


# ---------------------------------------------------------------------------
# 3. Patches (finished example, then two functions to write)
# ---------------------------------------------------------------------------


def cut_into_patches(img: np.ndarray, p: int) -> np.ndarray:
    """
    Cuts a colour picture of shape (H, W, 3) into non-overlapping p x p
    patches and returns them as a stack of shape
    ((H // p) * (W // p), p, p, 3), in reading order (left to right, then
    top to bottom). H and W must be multiples of p.

    Vision transformers start like this: each patch becomes one "token".
    To see every step drawn, run
    `uv run python e_reshape_and_transpose.py cut_into_patches`.

    Example:
        >>> cut_into_patches(np.zeros((64, 96, 3)), 16).shape
        (24, 16, 16, 3)
    """

    H, W, _ = img.shape
    nh, nw = H // p, W // p

    # Step 1. Split each axis in two: row = (which patch row, row inside the
    # patch), column = (which patch column, column inside the patch). This is
    # a reshape, because it doesn't change the reading order: rows of the
    # picture still come one after the other.
    grid = img.reshape(nh, p, nw, p, 3)  # (patch row, row in patch, patch col, col in patch, colour)

    # Step 2. Bring the two "which patch" axes to the front. This must be a
    # transpose: a patch's pixels come from p different picture rows, which
    # are not next to each other in reading order.
    grid = grid.transpose(0, 2, 1, 3, 4)  # (patch row, patch col, row in patch, col in patch, colour)

    # Step 3. The two "which patch" axes are now next to each other, so a
    # reshape can merge them into one. (The transpose made `grid`
    # non-contiguous, so this reshape makes a copy.)
    return grid.reshape(nh * nw, p, p, 3)


# Training notebooks show a batch of pictures as one big picture, laid out
# in a grid. A batch of six (h, w) robots, shape (6, h, w, 3), becomes one
# (2 * h, 3 * w, 3) picture: robots 0, 1, 2 in the top row, 3, 4, 5 below
# (`... contact_sheet`). This is `cut_into_patches` backwards.


def contact_sheet(batch: np.ndarray, rows: int, cols: int) -> np.ndarray:
    """Lays out a batch (rows * cols, h, w, 3) as one (rows * h, cols * w, 3) picture."""

    _, h, w, _ = batch.shape
    # Your solution here.
    pass


# Someone scrambled the (64, 96, 3) robot with this line:
#
#   scrambled = img.reshape(4, 16, 6, 16, 3).transpose(2, 1, 0, 3, 4).reshape(96, 64, 3)
#
# Undo it (`... unscramble`). Hint: work out what each axis of the 5-D array
# means first. The transpose is easy to undo; the sizes in the first reshape
# are where it goes wrong.


def unscramble(scrambled: np.ndarray) -> np.ndarray:
    """Turns the (96, 64, 3) scrambled picture back into the (64, 96, 3) robot."""

    # Your solution here.
    pass


# ---------------------------------------------------------------------------
# 4. channels_last, merge_heads and scores_to_vector (fix the bugs)
# ---------------------------------------------------------------------------

# Each of these three functions has exactly one bug. Fix each with the
# smallest change you can.


def channels_last(images: np.ndarray) -> np.ndarray:
    """
    Converts a batch of images from channels-first layout (B, C, H, W), the
    one PyTorch uses, to channels-last layout (B, H, W, C), the one
    matplotlib and most image files use. Pixel `[b, c, h, w]` of the input
    must end up at `[b, h, w, c]` of the output.

    To see what the bug does to a picture, run
    `uv run python e_reshape_and_transpose.py channels_last`.
    """

    B, C, H, W = images.shape
    return images.reshape(B, H, W, C)


def split_heads(x: np.ndarray, n_heads: int) -> np.ndarray:
    """
    Splits the feature axis of `x`, shape (B, T, D), into `n_heads` heads of
    D // n_heads features each, and moves the head axis in front of the time
    axis. Returns shape (B, n_heads, T, D // n_heads). Multi-head attention
    does this so that every head can work on its own slice of the features.

    This function is correct.
    """

    B, T, D = x.shape
    x = x.reshape(B, T, n_heads, D // n_heads)  # split D into (heads, features per head)
    return x.transpose(0, 2, 1, 3)  # (B, heads, T, features per head)


def merge_heads(x: np.ndarray) -> np.ndarray:
    """
    The inverse of `split_heads`: turns shape (B, n_heads, T, Dh) back into
    (B, T, n_heads * Dh), so that `merge_heads(split_heads(x, h))` gives
    back exactly `x`.
    """

    B, H, T, Dh = x.shape
    return x.reshape(B, T, H * Dh)


def scores_to_vector(scores: np.ndarray) -> np.ndarray:
    """
    A model returns one score per sample as an array of shape (B, 1).
    Returns the scores as a 1-D array of shape (B,), for any batch size B,
    including B = 1.
    """

    return np.squeeze(scores)


FUNCTIONS = {
    "rotate_clockwise": rotate_clockwise,
    "merge_channels": merge_channels,
    "swap_halves": swap_halves,
    "contact_sheet": contact_sheet,
    "unscramble": unscramble,
    "channels_last": channels_last,
}


def print_checks() -> None:
    """Prints a quick check of the functions that have no picture."""

    print("cut_into_patches of a (64, 96, 3) picture:", cut_into_patches(np.zeros((64, 96, 3)), 16).shape)
    print("  expected: (24, 16, 16, 3)")

    images = np.arange(2 * 3 * 2 * 2).reshape(2, 3, 2, 2)
    print("\nchannels_last: pixel [0, :, 1, 0] should be [2, 6, 10]")
    print("  got:", channels_last(images)[0, 1, 0])

    seq = np.arange(2 * 3 * 4).reshape(2, 3, 4)
    print("\nmerge_heads(split_heads(seq, 2)) == seq:", np.array_equal(merge_heads(split_heads(seq, 2)), seq))
    print("  expected: True")

    print("\nscores_to_vector of shape (1, 1):", scores_to_vector(np.array([[0.7]])).shape)
    print("  expected: (1,)")

    print(f"\nTo see a picture, run this file with one of: {', '.join(_viz.NAMES)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Check the functions, or show the picture for one problem.")
    parser.add_argument("picture", nargs="?", choices=_viz.NAMES, help="which picture to show")
    args = parser.parse_args()

    if args.picture is None:
        print_checks()
        return
    fn = FUNCTIONS.get(args.picture)
    _viz.check(args.picture, fn)


if __name__ == "__main__":
    main()
