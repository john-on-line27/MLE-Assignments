"""
Plot 2D datasets side by side, one panel each. Train points are circles,
validation points are squares, test points are triangles, and the color
shows the class.

Usage: python scripts/plotting/plot_datasets.py moons circles --save out.png
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt

from data import load_dataset


def plot_datasets(datasets):
    """Draw each dataset; datasets maps a name to (train, val, test) splits."""
    n = len(datasets)
    fig, axes = plt.subplots(1, n, figsize=(5 * n, 4.5), squeeze=False)
    for ax, (name, splits) in zip(axes[0], datasets.items()):
        for (X, y), split, marker in zip(
            splits, ["train", "val", "test"], "os^"
        ):
            for label in sorted(set(y)):
                points = [x for x, c in zip(X, y) if c == label]
                ax.scatter(
                    [p[0] for p in points],
                    [p[1] for p in points],
                    color=f"C{label}",
                    marker=marker,
                    s=18,
                    edgecolors="white",
                    linewidths=0.4,
                    label=f"class {label} ({split})",
                )
        ax.set_title(name)
        ax.set_xlabel("x1")
        ax.set_ylabel("x2")
    axes[0][0].legend(fontsize=7)
    fig.tight_layout()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("datasets", nargs="+", help="names in data/")
    parser.add_argument("--save", help="save to this file instead of showing")
    args = parser.parse_args()

    datasets = {}
    for name in args.datasets:
        train = load_dataset(name, "train")
        val = load_dataset(name, "val")
        test = load_dataset(name, "test")
        datasets[name] = (train, val, test)

    plot_datasets(datasets)
    if args.save:
        Path(args.save).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(args.save, dpi=150)
    else:
        plt.show()


if __name__ == "__main__":
    main()
