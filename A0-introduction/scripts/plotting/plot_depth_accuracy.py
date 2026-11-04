"""
Plot the train and validation accuracy of a saved tree as it is allowed to grow
deeper. A widening gap between the two lines is a sign of overfitting.

Needs a saved tree for the dataset (see scripts/fit_tree.py).

Usage:
    python scripts/plotting/plot_depth_accuracy.py moons --max-depth 15
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt

from config import model_path
from data import load_dataset
from evaluation import accuracy
from tree import load_tree


def plot_depth_accuracy(tree, train, val, depths, title):
    """Draw one accuracy line for the train set and one for the val set."""
    plt.figure(figsize=(8, 5))
    for name, (X, y) in [("train", train), ("val", val)]:
        accs = [
            accuracy(y, tree.predict(X, max_depth=depth)) for depth in depths
        ]
        plt.plot(depths, accs, marker="o", label=name)
    plt.xlabel("max depth")
    plt.ylabel("accuracy")
    plt.ylim(0, 1.05)
    plt.title(title)
    plt.legend()
    plt.tight_layout()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", help="name in data/")
    parser.add_argument("--max-depth", type=int, default=15)
    parser.add_argument(
        "--criterion", choices=["gini", "entropy"], default="gini"
    )
    parser.add_argument("--save", help="save to this file instead of showing")
    args = parser.parse_args()

    tree = load_tree(model_path(args.dataset, args.criterion))
    train = load_dataset(args.dataset, "train")
    val = load_dataset(args.dataset, "val")
    depths = list(range(1, args.max_depth + 1))
    title = f"{args.dataset}, {args.criterion}: accuracy vs. depth"

    plot_depth_accuracy(tree, train, val, depths, title)
    if args.save:
        Path(args.save).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(args.save, dpi=150)
    else:
        plt.show()


if __name__ == "__main__":
    main()
