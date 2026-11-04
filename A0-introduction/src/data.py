"""
Toy datasets, and reading and writing them as CSV files.

Each make_* function returns (X, y): X is a list of 2D points [x1, x2] and
y holds the class label (0, 1, ...) of each point. Every dataset is a small
puzzle with its own shape, so we can see what a tree learns from it.

A saved dataset lives in data/<name>/ as train.csv, val.csv and test.csv, with
one point per row: its features first, then its label in the last column.
"""

import csv
import math
import random
from pathlib import Path

from config import DATA_DIR, SEED

# -----------------------------------------------------------------------------
# toy datasets


def add_noise(
    rng: random.Random, point: list[float], std: float
) -> list[float]:
    """Nudge each coordinate of a point by a small random amount."""
    return [v + rng.gauss(0, std) for v in point]


def make_moons(n: int = 1000, noise: float = 0.2, seed: int = SEED):
    """Two half circles that hook into each other."""
    rng = random.Random(seed)
    X, y = [], []
    upper = n // 2
    for i in range(upper):  # class 0: the upper moon
        angle = math.pi * i / max(1, upper - 1)
        X.append(add_noise(rng, [math.cos(angle), math.sin(angle)], noise))
        y.append(0)
    for i in range(n - upper):  # class 1: the lower moon
        angle = math.pi * i / max(1, n - upper - 1)
        point = [1 - math.cos(angle), 0.5 - math.sin(angle)]
        X.append(add_noise(rng, point, noise))
        y.append(1)
    return X, y


def make_circles(
    n: int = 1000, noise: float = 0.1, factor: float = 0.5, seed: int = SEED
):
    """A ring (class 0) around a ring factor times as big (class 1)."""
    rng = random.Random(seed)
    X, y = [], []
    outer = n // 2
    for label, m, radius in [(0, outer, 1.0), (1, n - outer, factor)]:
        for i in range(m):
            angle = 2 * math.pi * i / max(1, m - 1)
            point = [radius * math.cos(angle), radius * math.sin(angle)]
            X.append(add_noise(rng, point, noise))
            y.append(label)
    return X, y


#                                                                 1
#                        .---------------------.                 0    *putt*
#                       /  .-----------------.  \             0     1
#                      /  /                   \  \              1
#                    .----------------------------------.    0   1  *putt*
#                   /                                  /|  1  0
#                  /    (@)                           / |0 1
#      _[]_       /                                  /##|  *sputter*
#    .---------. .----------------------------------. ##|
#   /         /| |                                  |   |
#  .---------. | |   H  O  N  D  A   [ ::]  [ ::]   |   |
#  | BENZIN  | | |                                  |   '
#  |   \ /   | | |   =============    ( I / O )     |  /
#  |    X    | ' |   =============                  | /
#  |   / \   |/  |                                  |/
#  '---------'   '----------------------------------'


def make_xor(n: int = 1000, noise: float = 0.1, seed: int = SEED):
    """Four squares: class 0 where x1 and x2 have the same sign, else 1."""
    rng = random.Random(seed)
    X, y = [], []
    for _ in range(n):
        x1, x2 = rng.uniform(-1, 1), rng.uniform(-1, 1)
        X.append(add_noise(rng, [x1, x2], noise))
        y.append(0 if (x1 > 0) == (x2 > 0) else 1)
    return X, y


def make_checkerboard(
    n: int = 1000, grid: int = 4, noise: float = 0.05, seed: int = SEED
):
    """A grid x grid checkerboard of the two classes."""
    rng = random.Random(seed)
    X, y = [], []
    for _ in range(n):
        x1, x2 = rng.uniform(0, grid), rng.uniform(0, grid)
        X.append(add_noise(rng, [x1, x2], noise))
        y.append((int(x1) + int(x2)) % 2)
    return X, y


def make_linear(n: int = 1000, noise: float = 0.15, seed: int = SEED):
    """Two classes on either side of the diagonal line x2 = x1."""
    rng = random.Random(seed)
    X, y = [], []
    for _ in range(n):
        x1, x2 = rng.uniform(-2, 2), rng.uniform(-2, 2)
        X.append(add_noise(rng, [x1, x2], noise))
        y.append(0 if x2 > x1 else 1)
    return X, y


GENERATORS = {
    "moons": make_moons,
    "circles": make_circles,
    "xor": make_xor,
    "checkerboard": make_checkerboard,
    "linear": make_linear,
}

# -----------------------------------------------------------------------------
# splitting into train, validation and test


def train_test_split(
    X: list[list[float]],
    y: list[int],
    test_size: float = 0.2,
    seed: int = SEED,
):
    """Shuffle the rows, then keep the last test_size of them for testing.

    Returns X_train, X_test, y_train, y_test.
    """
    assert len(X) == len(y)
    order = list(range(len(X)))
    random.Random(seed).shuffle(order)
    n_train = len(X) - round(len(X) * test_size)
    train, test = order[:n_train], order[n_train:]
    X_train, y_train = [X[i] for i in train], [y[i] for i in train]
    X_test, y_test = [X[i] for i in test], [y[i] for i in test]
    return X_train, X_test, y_train, y_test


# -----------------------------------------------------------------------------
# reading and writing


def save_csv(path: str | Path, X: list[list[float]], y: list[int]) -> None:
    """Write one row per point: its features, then its label."""
    header = [f"x{i + 1}" for i in range(len(X[0]))] + ["y"]
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows([*row, label] for row, label in zip(X, y))


def load_csv(path: str | Path) -> tuple[list[list[float]], list[int]]:
    """Read a file written by save_csv back into X and y."""
    X, y = [], []
    with open(path) as f:
        reader = csv.reader(f)
        next(reader)  # skip the header
        for *features, label in reader:
            X.append([float(v) for v in features])
            y.append(int(label))
    return X, y


def save_dataset(
    name: str, split: str, X: list[list[float]], y: list[int]
) -> None:
    """Save one split ("train", "val" or "test") to data/<name>/."""
    save_csv(DATA_DIR / name / f"{split}.csv", X, y)


def load_dataset(name: str, split: str) -> tuple[list[list[float]], list[int]]:
    """Load one split ("train", "val" or "test") from data/<name>/."""
    return load_csv(DATA_DIR / name / f"{split}.csv")


def load_train_val(name: str) -> tuple[list[list[float]], list[int]]:
    """Load the train and val splits of a dataset as one long list."""
    X_train, y_train = load_dataset(name, "train")
    X_val, y_val = load_dataset(name, "val")
    return X_train + X_val, y_train + y_val
