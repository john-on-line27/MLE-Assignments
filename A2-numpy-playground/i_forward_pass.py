"""
A Forward Pass

This file puts everything together: a small but complete evaluation of a
neural network classifier in NumPy, from raw data to a loss and an accuracy.
Next week you'll build and train networks like this one yourself.

The pipeline, in the order the code at the bottom runs it:

1. `shuffle` the dataset, then split it into a training and a test set.
2. `standardize` the features with statistics from the training set.
3. `hidden_layer`: a linear layer followed by ReLU.
4. A second linear layer gives the logits (one score per class).
5. `softmax` turns the logits into class probabilities.
6. `cross_entropy` and `accuracy` measure how good the probabilities are.

The model's parameters are given: `make_params` builds them, so there is
no training in this file. Three functions, `shuffle`, `standardize` and `hidden_layer`, have
exactly one bug each, and every bug comes from an idea in puzzles a to h.
One crashes; the others just give wrong numbers. The rest of the pipeline,
at the bottom of the file, is correct.

Read each function and its docstring to work out where its bug is, and fix
it with the smallest change you can. When you are done, run this file with
`uv run python i_forward_pass.py`. It should print exactly:

    train: 150 samples, test: 50 samples
    test loss:     0.2474
    test accuracy: 0.9000

⭐ CORE: the bugs in `shuffle`, `standardize` and `hidden_layer`.

DO NOT MODIFY THE FUNCTION SIGNATURES OR THE CODE BELOW `if __name__`.
"""

import numpy as np


# ⭐ CORE
def shuffle(X: np.ndarray, y: np.ndarray, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """
    Returns the samples `X`, shape (n, d), and their labels `y`, shape (n,),
    in a random order. Sample `X[i]` must keep its label `y[i]`: both are
    put in the same new order.
    """

    perm = rng.permutation(len(X))
    return X[perm], y[rng.permutation(len(y))]


# ⭐ CORE
def standardize(X_train: np.ndarray, X_test: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Standardizes every feature (column) to mean 0 and standard deviation 1,
    using the mean and standard deviation of the *training* set for both
    sets, so that the test set is treated exactly like new data would be.
    Each feature gets its own mean and its own standard deviation (NumPy's
    default, `ddof=0`).

    Returns two new arrays of the same shapes as the inputs.
    """

    mean = X_train.mean(axis=0)
    std = X_train.std()
    train = (X_train - mean) / std
    test = (X_test - mean) / std
    return train, test


# ⭐ CORE
def hidden_layer(X: np.ndarray, W: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    A linear layer followed by ReLU: computes `X @ W + b` and then replaces
    every negative entry by 0. `X` has shape (n, d_in), `W` has shape
    (d_in, d_out) and `b` has shape (d_out,). Returns shape (n, d_out).
    """

    return np.max(X @ W + b, 0)


# ---------------------------------------------------------------------------
# The rest of the pipeline, data and parameters (correct, don't change)
# ---------------------------------------------------------------------------


def softmax(logits: np.ndarray) -> np.ndarray:
    """
    Applies softmax to every row of `logits`, shape (n, C), so that row i is
    a probability distribution over the C classes for sample i.
    """

    e = np.exp(logits - logits.max(axis=1, keepdims=True))
    return e / e.sum(axis=1, keepdims=True)


def cross_entropy(probs: np.ndarray, y: np.ndarray) -> float:
    """
    Returns the mean cross-entropy loss over all n samples. `probs` has
    shape (n, C) and `y` holds the n true labels. The loss of one sample is
    -log of the probability the model gave to its true class; the one-hot
    row picks out that probability.
    """

    # Row c of `np.eye(C)` is all zeros except a 1 at position c, so row i of
    # `onehot` has its 1 at column y[i], the true class of sample i.
    onehot = np.eye(probs.shape[1])[y]  # (n, C)
    per_sample = -(onehot * np.log(probs)).sum(axis=1)
    return float(per_sample.mean())


def accuracy(probs: np.ndarray, y: np.ndarray) -> float:
    """
    Returns the fraction of samples whose most probable class (according to
    `probs`, shape (n, C)) is the true class in `y`, shape (n,).
    """

    predictions = probs.argmax(axis=1)
    return float((predictions == y).mean())


# The centre of each of the three classes, in standardized units.
CENTRES = np.array(
    [
        [1.5, 0.0, -1.0, 0.5],
        [-1.5, 1.0, 0.0, 0.5],
        [0.0, -1.0, 1.0, -1.0],
    ]
)


def make_data(rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """200 samples with 4 features on very different scales, 3 classes."""
    y = rng.integers(0, 3, size=200)
    Z = CENTRES[y] + rng.normal(scale=1.0, size=(200, 4))
    X = Z * np.array([1.0, 10.0, 100.0, 0.1]) + np.array([0.0, 5.0, -50.0, 1.0])
    return X, y


def make_params() -> dict[str, np.ndarray]:
    """The parameters of the trained two-layer network."""
    return {
        "W1": np.hstack([np.eye(4), -np.eye(4)]),  # (4, 8)
        "b1": np.zeros(8),
        "W2": np.vstack([CENTRES.T, -CENTRES.T]),  # (8, 3)
        "b2": -0.5 * (CENTRES**2).sum(axis=1),  # (3,)
    }


if __name__ == "__main__":
    rng = np.random.default_rng(seed=7)
    X, y = make_data(rng)
    X, y = shuffle(X, y, rng)
    X_train, y_train = X[:150], y[:150]
    X_test, y_test = X[150:], y[150:]
    print(f"train: {len(X_train)} samples, test: {len(X_test)} samples")

    X_train, X_test = standardize(X_train, X_test)

    params = make_params()
    hidden = hidden_layer(X_test, params["W1"], params["b1"])
    logits = hidden @ params["W2"] + params["b2"]
    probs = softmax(logits)

    print(f"test loss:     {cross_entropy(probs, y_test):.4f}")
    print(f"test accuracy: {accuracy(probs, y_test):.4f}")
