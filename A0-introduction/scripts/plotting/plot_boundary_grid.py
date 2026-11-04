"""
Plot a grid of decision boundaries: one column per dataset, one row per
depth. Each panel shades the area by the class the tree predicts there,
shows the validation points on top, and gives the validation accuracy in
its title.

Needs a saved tree for each dataset (see scripts/fit_tree.py).

Usage:
    python scripts/plotting/plot_boundary_grid.py moons circles \\
        --depths 1 2 3 None --save results/figures/boundary_grid.png
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt

from config import model_path
from data import load_dataset
from evaluation import accuracy
from tree import load_tree


def draw_boundary(ax, tree, X, y, depth, resolution=200):
    """Shade the plane by the tree's prediction, then scatter X on top."""
    x1 = [row[0] for row in X]
    x2 = [row[1] for row in X]
    left, right = min(x1) - 0.5, max(x1) + 0.5
    bottom, top = min(x2) - 0.5, max(x2) + 0.5

    # ask the tree about every point of a fine grid that covers the data
    steps = range(resolution + 1)
    grid1 = [left + (right - left) * i / resolution for i in steps]
    grid2 = [bottom + (top - bottom) * i / resolution for i in steps]
    preds = [
        tree.predict([[a, b] for a in grid1], max_depth=depth) for b in grid2
    ]

    classes = sorted(set(y))
    levels = [c - 0.5 for c in classes] + [classes[-1] + 0.5]
    colors = [f"C{c}" for c in classes]
    ax.contourf(grid1, grid2, preds, levels=levels, colors=colors, alpha=0.3)

    for label in classes:
        points = [x for x, c in zip(X, y) if c == label]
        ax.scatter(
            [p[0] for p in points],
            [p[1] for p in points],
            color=f"C{label}",
            s=18,
            edgecolors="white",
            linewidths=0.4,
        )
    ax.set_xticks([])
    ax.set_yticks([])


def plot_boundary_grid(trees, vals, depths, criterion):
    """Draw one panel per depth and dataset; trees, vals are keyed by name."""
    rows, cols = len(depths), len(trees)
    fig, axes = plt.subplots(
        rows, cols, figsize=(5 * cols, 4.5 * rows), squeeze=False
    )
    for i, depth in enumerate(depths):
        for j, name in enumerate(trees):
            ax = axes[i][j]
            X, y = vals[name]
            draw_boundary(ax, trees[name], X, y, depth)
            acc = accuracy(y, trees[name].predict(X, max_depth=depth))
            ax.set_title(f"acc: {acc:.2f}", fontsize=24)
            if i == 0:
                ax.set_title(f"{name}\nacc: {acc:.2f}", fontsize=28)
            if j == 0:
                label = "no limit" if depth is None else depth
                ax.set_ylabel(f"depth = {label}", fontsize=28)
    fig.suptitle(f"Decision boundaries, {criterion} criterion", fontsize=32)
    fig.tight_layout(rect=(0, 0, 1, 0.985))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("datasets", nargs="+", help="names in data/")
    parser.add_argument("--depths", nargs="+", required=True)
    parser.add_argument(
        "--criterion", choices=["gini", "entropy"], default="gini"
    )
    parser.add_argument("--save", help="save to this file instead of showing")
    args = parser.parse_args()

    depths = [None if d == "None" else int(d) for d in args.depths]
    trees, vals = {}, {}
    for name in args.datasets:
        trees[name] = load_tree(model_path(name, args.criterion))
        vals[name] = load_dataset(name, "val")

    plot_boundary_grid(trees, vals, depths, args.criterion)
    if args.save:
        Path(args.save).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(args.save, dpi=150)
    else:
        plt.show()


if __name__ == "__main__":
    main()
