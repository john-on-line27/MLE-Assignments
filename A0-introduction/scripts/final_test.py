"""
Fit one decision tree on the train and validation splits of a dataset, then
score it once on the test split. Run this only after you have picked your
settings (see scripts/cv_gridsearch.py). Prints the test accuracy and the
confusion matrix.

Usage:
    python scripts/final_test.py moons --criterion gini --max-depth 4
"""

import argparse

from data import load_dataset, load_train_val
from evaluation import accuracy, confusion_matrix
from tree import DecisionTree


def final_test(name, max_depth, min_samples_split, criterion):
    """Fit on train + val, then predict the test split once."""
    X, y = load_train_val(name)
    tree = DecisionTree(criterion).fit(X, y)
    X_test, y_test = load_dataset(name, "test")
    return y_test, tree.predict(X_test, max_depth, min_samples_split)


def print_details(y_true, y_pred):
    """Print the accuracy and the confusion matrix."""
    print(f"test accuracy: {accuracy(y_true, y_pred):.3f}")
    print("confusion matrix (row: true class, column: predicted class):")
    for row in confusion_matrix(y_true, y_pred)[1]:
        print("  " + "  ".join(f"{count:5d}" for count in row))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", help="name in data/")
    parser.add_argument("--max-depth", default="None")
    parser.add_argument("--min-samples-split", type=int, default=2)
    parser.add_argument(
        "--criterion", choices=["gini", "entropy"], default="gini"
    )
    args = parser.parse_args()

    max_depth = None if args.max_depth == "None" else int(args.max_depth)
    y_test, y_pred = final_test(
        args.dataset, max_depth, args.min_samples_split, args.criterion
    )
    print_details(y_test, y_pred)


if __name__ == "__main__":
    main()
