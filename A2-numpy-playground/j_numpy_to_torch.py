"""
From NumPy to PyTorch

PyTorch tensors are NumPy arrays with GPU support and gradients added. Almost
everything you learned in this playground carries over: shapes, strides,
views, broadcasting, axes and `@` all work the same way. What changes are
some names and a handful of defaults, and those are exactly where code
breaks when you port it.

Names that differ:

| NumPy                         | PyTorch                                 |
|-------------------------------|-----------------------------------------|
| `axis=`, `keepdims=`          | `dim=`, `keepdim=` (the NumPy names are accepted too) |
| `np.concatenate`              | `torch.cat`                             |
| `np.expand_dims(x, 0)`        | `x.unsqueeze(0)`                        |
| `x.transpose(0, 2, 1)`        | `x.permute(0, 2, 1)`; `x.transpose(1, 2)` swaps exactly two dims |
| `np.clip`                     | `x.clamp` (`torch.clip` also exists)    |
| `x[::-1]`                     | `x.flip(0)`, which copies (negative steps in slices are not allowed) |

Defaults and behaviours that differ:

- `torch.tensor([1.0])` is `float32`, while `np.array([1.0])` is `float64`.
  But `torch.from_numpy` keeps the array's dtype, so a NumPy array becomes a
  `float64` tensor, and `@` refuses to mix `float64` with `float32`.
- `torch.from_numpy(a)` and `t.numpy()` share memory with their source.
  `torch.tensor(a)` always copies.
- Strides count *elements* in PyTorch (`t.stride()`) and *bytes* in NumPy
  (`a.strides`).
- `t.view(...)` refuses to work on a non-contiguous tensor, where NumPy's
  `reshape` would copy without an error or a warning. `t.reshape(...)` behaves like NumPy, and
  `t.contiguous()` makes the copy explicit.
- `t.max(dim=1)` returns two things, the values and their indices. Use
  `.values` to get the values. Without `dim`, `t.max()` is just a number.
- `torch.maximum(x, y)` wants two tensors, not a tensor and a Python number.

In-place operations on views behave as in NumPy, and their names end in an
underscore: `t.add_(1)` changes `t`, `t.add(1)` returns a new tensor.

This file has four parts. Work through them in order:

1. Same idea, different spelling (questions).
2. Who shares memory (questions).
3. view, reshape and contiguous (questions).
4. Naive ports: fix the bugs in `relu`, `softmax`, `reverse_time`,
   `flatten_channels_last`, `linear_from_numpy` and `center_columns`.

Answer the questions by setting the answer variables (they start out as
`None`). You may run code to check your answers. Give a shape as a tuple,
such as (3, 4), a dtype as a string without the module, such as "float32",
and an array as a list. If a line raises an error, answer with the string
"error".

Docs: https://pytorch.org/docs/stable/tensors.html

⭐ CORE: Q2, Q3a and the bug in `linear_from_numpy`.

DO NOT MODIFY THE FUNCTION SIGNATURES.
"""

import numpy as np
import torch


# ---------------------------------------------------------------------------
# 1. Same idea, different spelling (questions)
# ---------------------------------------------------------------------------

t = torch.arange(12.0).reshape(3, 4)
x3 = torch.zeros(2, 3, 4)

# Q1a. Fill in the shape of each expression, or "error".
SHAPES: dict[str, object] = {
    "t.sum(dim=0)": (4,),
    "t.unsqueeze(0)": (1, 3, 4),
    "t.permute(1, 0)": (4, 3),
    "torch.cat([t, t], dim=1)": (3, 8),
    "t.max(dim=1).values": (3,),
    "t.max()": (),
    "t[:, ::-1]": "error",
    "t.flip(1)": (3, 4),
    "x3.transpose(1, 2)": (2, 4, 3),
    "x3.transpose(0, 2, 1)": "error",
}

# Q1b. Fill in the dtype of each expression as a string (e.g. "float32").
DTYPES: dict[str, object] = {
    "np.array([1.0, 2.0])": "float64",
    "torch.tensor([1.0, 2.0])": "float32",
    "torch.tensor([1, 2])": "int64",
    "torch.from_numpy(np.array([1.0, 2.0]))": "float64",
    "np.exp(np.arange(3))": "float64",
    "torch.exp(torch.arange(3))": "float32",
}

a32 = np.zeros((3, 4), dtype=np.float32)

# Q1c. What is `a32.strides`?
NUMPY_STRIDES = (16, 4)

# Q1d. What is `torch.from_numpy(a32).stride()`?
TORCH_STRIDES = (4, 1)


# ---------------------------------------------------------------------------
# 2. Who shares memory (questions)
# ---------------------------------------------------------------------------


def sharing_demo() -> dict[str, float]:
    a = np.array([1.0, 2.0, 3.0])
    shared = torch.from_numpy(a)
    copied = torch.tensor(a)
    back = shared.numpy()

    a[0] = 10.0
    shared.add_(1)
    copied = copied + 1

    return {
        "a[0]": float(a[0]),
        "shared[0]": float(shared[0]),
        "copied[0]": float(copied[0]),
        "back[0]": float(back[0]),
    }


# ⭐ CORE
# Q2. Without running it first, fill in the values `sharing_demo` returns.
#     Then run it to check.
SHARING: dict[str, object] = {
    "a[0]": 11.0,
    "shared[0]": 11.0,
    "copied[0]": 2.0,
    "back[0]": 11.0,
}


# ---------------------------------------------------------------------------
# 3. view, reshape and contiguous (questions)
# ---------------------------------------------------------------------------

t = torch.arange(12.0).reshape(3, 4)

# ⭐ CORE
# Q3a. For each expression, give the resulting shape, or "error".
VIEWS: dict[str, object] = {
    "t.view(12)": (12,),
    "t.T.view(12)": "error",
    "t.T.reshape(12)": (12,),
    "t.T.contiguous().view(12)": (12,),
    "t[:, :2].view(6)": "error",
    "t[:2].view(8)": (8,),
}

# Q3b. Does `t.T.reshape(12)` share memory with `t`? True or False.
RESHAPE_OF_T_SHARES_MEMORY = False


# ---------------------------------------------------------------------------
# 4. Naive ports (fix the bugs)
# ---------------------------------------------------------------------------

# Someone took working NumPy functions and ported them to PyTorch line by
# line. The NumPy original is in each docstring. Each port has exactly one
# bug, caused by a difference between the two libraries. Run this file to see
# what goes wrong, then fix each one with the smallest change you can.


def relu(x: torch.Tensor) -> torch.Tensor:
    """
    Returns max(x, 0) element by element.

    NumPy original:
        return np.maximum(x, 0)
    """

    return torch.maximum(x, torch.zeros_like(x))


def softmax(logits: torch.Tensor) -> torch.Tensor:
    """
    Returns the softmax of each row of `logits`, shape (N, C).

    NumPy original:
        shifted = logits - logits.max(axis=1, keepdims=True)
        e = np.exp(shifted)
        return e / e.sum(axis=1, keepdims=True)
    """

    shifted = logits - logits.max(dim=1, keepdim=True).values
    e = torch.exp(shifted)
    return e / e.sum(dim=1, keepdim=True)


def reverse_time(x: torch.Tensor) -> torch.Tensor:
    """
    Reverses a batch of sequences of shape (B, T, D) along the time axis.

    NumPy original:
        return x[:, ::-1]
    """

    return x.flip(1)


def flatten_channels_last(images: torch.Tensor) -> torch.Tensor:
    """
    Turns a batch of images of shape (B, C, H, W) into one row per image, in
    channels-last order: the result has shape (B, H * W * C), and each row
    lists the C channel values of the first pixel, then of the second, and
    so on.

    NumPy original:
        B = images.shape[0]
        return images.transpose(0, 2, 3, 1).reshape(B, -1)
    """

    B = images.shape[0]
    return images.permute(0, 2, 3, 1).reshape(B, -1)


# ⭐ CORE
def linear_from_numpy(X: np.ndarray, W: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    """
    Applies a linear layer to a batch of features that arrives as a NumPy
    array of shape (N, in), with float32 weights `W` of shape (in, out) and
    bias `b` of shape (out,). Returns a float32 tensor of shape (N, out).

    NumPy original:
        return X @ W + b
    """

    X_t = torch.as_tensor(X, dtype=W.dtype, device=W.device)
    return X_t @ W + b


def center_columns(x: np.ndarray) -> torch.Tensor:
    """
    Returns a tensor holding `x` with each column's mean subtracted, so every
    column of the result has mean 0. `x` itself is not changed.

    NumPy original:
        x = np.array(x)
        x -= x.mean(axis=0)
        return x
    """

    t = torch.from_numpy(x).clone()
    t -= t.mean(dim=0)
    return t


if __name__ == "__main__":
    from _demo import run

    run("relu:", lambda: relu(torch.tensor([-1.0, 0.5, -0.3, 2.0])))
    print("  expected: tensor([0.0000, 0.5000, 0.0000, 2.0000])")
    run("softmax rows sum to:", lambda: softmax(torch.tensor([[1.0, 2.0, 3.0], [1000.0, 1000.0, 1000.0]])).sum(dim=1))
    print("  expected: tensor([1., 1.])")
    run("reverse_time:", lambda: reverse_time(torch.arange(3.0).reshape(1, 3, 1)).flatten())
    print("  expected: tensor([2., 1., 0.])")
    run("flatten_channels_last:", lambda: flatten_channels_last(torch.arange(8.0).reshape(1, 2, 2, 2)))
    print("  expected: tensor([[0., 4., 1., 5., 2., 6., 3., 7.]])")
    run("linear_from_numpy dtype:", lambda: linear_from_numpy(np.ones((2, 3)), torch.ones(3, 4), torch.zeros(4)).dtype)
    print("  expected: torch.float32")
    data = np.array([[1.0, 10.0], [3.0, 30.0]])
    run("center_columns:", lambda: center_columns(data).tolist())
    print("  expected: [[-1.0, -10.0], [1.0, 10.0]]")
    print("center_columns input after:", data.tolist())
    print("  expected: [[1.0, 10.0], [3.0, 30.0]]")
