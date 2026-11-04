"""
Score decision tree settings with k-fold cross-validation on the train and
validation splits of a dataset together, so the folds take the place of
a single validation set. Give a flag several values to try every combination.
Prints one row per setting, from best to worst, then more detail about
the best one.

Usage:
    python scripts/cv_gridsearch.py moons --max-depth 5
    python scripts/cv_gridsearch.py moons --max-depth 3 5 10 None \\
        --criterion gini entropy --folds 10
"""

import argparse

from config import SEED
from data import load_train_val
from evaluation import cross_validate


def print_table(results):
    """Print one row per setting: its mean accuracy and how much it varies."""
    print("criterion  max_depth  min_samples_split  accuracy       depth")
    for r in results:
        print(
            f"{r['criterion']:<9}  {r['max_depth']!s:>9}  "
            f"{r['min_samples_split']!s:>17}  "
            f"{r['mean_accuracy']:.3f} ± {r['std_accuracy']:.3f}  "
            f"{r['avg_pred_depth']:5.2f}"
        )


def print_details(r):
    """Print the accuracy on each fold and the summed confusion matrix."""
    print("accuracy on each fold:")
    print("  " + "  ".join(f"{acc:.3f}" for acc in r["fold_accuracies"]))
    print("confusion matrix (row: true class, column: predicted class):")
    for row in r["confusion_matrix"]:
        print("  " + "  ".join(f"{count:5d}" for count in row))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", help="name in data/")
    parser.add_argument("--max-depth", nargs="+", default=["None"])
    parser.add_argument(
        "--min-samples-split", nargs="+", type=int, default=[2]
    )
    parser.add_argument(
        "--criterion", nargs="+", choices=["gini", "entropy"], default=["gini"]
    )
    parser.add_argument("--folds", type=int, default=5)
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()

    X, y = load_train_val(args.dataset)
    depths = [None if d == "None" else int(d) for d in args.max_depth]
    grid = {
        "criterion": args.criterion,
        "max_depth": depths,
        "min_samples_split": args.min_samples_split,
    }
    results = cross_validate(X, y, grid, k=args.folds, seed=args.seed)
    results.sort(key=lambda r: r["mean_accuracy"], reverse=True)

    print_table(results)
    print()
    print("best setting:")
    print_details(results[0])


if __name__ == "__main__":
    main()
