"""
Plot the confusion matrix of a saved tree on a dataset's validation split: how
often each true class (row) was predicted as each class (column).

Needs a saved tree for the dataset (see scripts/fit_tree.py).

Usage:
    python scripts/plotting/plot_confusion_matrix.py moons --max-depth 5
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt

from config import model_path
from data import load_dataset
from evaluation import confusion_matrix
from tree import load_tree


def plot_confusion_matrix(classes, matrix, title):
    """Draw the matrix as shaded squares with the counts written in them."""
    n = len(classes)
    fig, ax = plt.subplots(figsize=(1.2 * n + 2, 1.2 * n + 2))
    image = ax.imshow(matrix, cmap="Blues")
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)

    biggest = max(max(row) for row in matrix)
    for i in range(n):
        for j in range(n):
            # white text on dark squares, black text on light ones
            color = "white" if matrix[i][j] > biggest / 2 else "black"
            ax.text(j, i, matrix[i][j], ha="center", va="center", color=color)

    ax.set_xticks(range(n), classes)
    ax.set_yticks(range(n), classes)
    ax.set_xlabel("predicted")
    ax.set_ylabel("true")
    ax.set_title(title)
    fig.tight_layout()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", help="name in data/")
    parser.add_argument("--max-depth", type=int, help="default: no limit")
    parser.add_argument(
        "--criterion", choices=["gini", "entropy"], default="gini"
    )
    parser.add_argument("--save", help="save to this file instead of showing")
    args = parser.parse_args()

    tree = load_tree(model_path(args.dataset, args.criterion))
    X, y = load_dataset(args.dataset, "val")
    classes, matrix = confusion_matrix(
        y, tree.predict(X, max_depth=args.max_depth)
    )
    depth = "full" if args.max_depth is None else args.max_depth
    title = f"{args.dataset}, {args.criterion}, depth = {depth}"

    plot_confusion_matrix(classes, matrix, title)
    if args.save:
        Path(args.save).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(args.save, dpi=150)
    else:
        plt.show()


if __name__ == "__main__":
    main()
