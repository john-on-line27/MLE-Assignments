"""
Measuring how good a tree is.

A tree can memorize its training rows, so we always score it on rows it did
not see while growing. To pick settings such as the depth, we use k-fold
cross-validation: cut the rows into k folds, then k times grow a
tree on k - 1 folds and score it on the fold that was left out. Averaging
the k scores gives a steadier estimate than a single split would.
"""

import random
import statistics
from itertools import product

from tree import DecisionTree

# -----------------------------------------------------------------------------
# scores


def accuracy(y_true: list[int], y_pred: list[int]) -> float:
    """Fraction of predictions that match the true label."""
    assert len(y_true) == len(y_pred) > 0
    return sum(t == p for t, p in zip(y_true, y_pred)) / len(y_true)


def confusion_matrix(
    y_true: list[int], y_pred: list[int]
) -> tuple[list[int], list[list[int]]]:
    """Count how often each true class (row) gets each prediction (column).

    Returns the sorted classes and the matrix of counts.
    """
    classes = sorted(set(y_true) | set(y_pred))
    matrix = [[0] * len(classes) for _ in classes]
    for t, p in zip(y_true, y_pred):
        matrix[classes.index(t)][classes.index(p)] += 1
    return classes, matrix


def evaluate(
    tree: DecisionTree,
    X: list[list[float]],
    y: list[int],
    max_depth: int | None = None,
    min_samples_split: int = 2,
) -> dict:
    """Score a fitted tree on the rows X, y."""
    walks = [tree.predict_one(x, max_depth, min_samples_split) for x in X]
    y_pred = [label for label, depth in walks]
    return {
        "accuracy": accuracy(y, y_pred),
        "confusion_matrix": confusion_matrix(y, y_pred)[1],
        "avg_pred_depth": statistics.mean(depth for label, depth in walks),
    }


# -----------------------------------------------------------------------------
# picking settings


def k_fold(
    n: int, k: int, seed: int | None = None
) -> list[tuple[list[int], list[int]]]:
    """Shuffle the row numbers 0..n-1 and deal them out into k folds.

    Returns k (train, val) pairs: each fold is the validation set once, and
    the rows of the other folds are its training set.
    """
    assert 2 <= k <= n
    order = list(range(n))
    random.Random(seed).shuffle(order)
    folds = [order[i::k] for i in range(k)]  # deal like a deck of cards
    return [([i for i in order if i not in val], val) for val in folds]


def grid_search(
    X_train: list[list[float]],
    y_train: list[int],
    X_val: list[list[float]],
    y_val: list[int],
    grid: dict[str, list],
) -> list[dict]:
    """Score every combination of the settings in grid on the validation rows.

    grid maps "criterion", "max_depth" and "min_samples_split" to lists of
    values.
    We grow one full tree per criterion and get the smaller trees by stopping
    early (see DecisionTree.predict_one), so nothing is grown twice.
    """
    results = []
    for criterion in grid["criterion"]:
        tree = DecisionTree(criterion=criterion).fit(X_train, y_train)
        for max_depth, min_samples_split in product(
            grid["max_depth"], grid["min_samples_split"]
        ):
            score = evaluate(tree, X_val, y_val, max_depth, min_samples_split)
            setting = {
                "criterion": criterion,
                "max_depth": max_depth,
                "min_samples_split": min_samples_split,
            }
            results.append(setting | score)
    return results


def cross_validate(
    X: list[list[float]],
    y: list[int],
    grid: dict[str, list],
    k: int = 5,
    seed: int | None = None,
) -> list[dict]:
    """Run grid_search on each of k folds, then summarize each setting."""
    results = []
    for train, val in k_fold(len(X), k, seed):
        X_train, y_train = [X[i] for i in train], [y[i] for i in train]
        X_val, y_val = [X[i] for i in val], [y[i] for i in val]
        results += grid_search(X_train, y_train, X_val, y_val, grid)
    return summarize(results)


def summarize(results: list[dict]) -> list[dict]:
    """Merge the results that share a setting into one row per setting.

    The accuracies get a mean and a (population) standard deviation, the
    confusion matrices are added up, and the prediction depths averaged.
    """
    groups: dict[tuple, list[dict]] = {}
    for r in results:
        setting = (r["criterion"], r["max_depth"], r["min_samples_split"])
        groups.setdefault(setting, []).append(r)

    summary = []
    for (criterion, max_depth, min_samples_split), rows in groups.items():
        accuracies = [r["accuracy"] for r in rows]
        summary.append(
            {
                "criterion": criterion,
                "max_depth": max_depth,
                "min_samples_split": min_samples_split,
                "fold_accuracies": accuracies,
                "mean_accuracy": statistics.mean(accuracies),
                "std_accuracy": statistics.pstdev(accuracies),
                "confusion_matrix": add_up(
                    [r["confusion_matrix"] for r in rows]
                ),
                "avg_pred_depth": statistics.mean(
                    r["avg_pred_depth"] for r in rows
                ),
            }
        )
    return summary


def add_up(matrices: list[list[list[int]]]) -> list[list[int]]:
    """Add matrices of the same shape together, cell by cell."""
    total = [[0] * len(row) for row in matrices[0]]
    for matrix in matrices:
        for i, row in enumerate(matrix):
            for j, count in enumerate(row):
                total[i][j] += count
    return total
