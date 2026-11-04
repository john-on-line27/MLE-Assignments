"""
Grow a full decision tree on the training split of each given dataset and
save it to results/models/<name>_<criterion>.json.

The tree is grown without any limit. Smaller trees are imitated later by
stopping early when predicting (see DecisionTree.predict_one in src/tree.py).

Usage:
    python scripts/fit_tree.py moons circles --criterion entropy
"""

import argparse

from config import ROOT, model_path
from data import load_dataset
from tree import DecisionTree, save_tree


def fit_tree(name, criterion):
    """Grow a tree on a dataset's training split and save it."""
    X, y = load_dataset(name, "train")
    tree = DecisionTree(criterion=criterion).fit(X, y)
    path = model_path(name, criterion)
    save_tree(tree, path)
    print(f"{name}: saved to {path.relative_to(ROOT)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("datasets", nargs="+", help="names in data/")
    parser.add_argument(
        "--criterion", choices=["gini", "entropy"], default="gini"
    )
    args = parser.parse_args()

    for name in args.datasets:
        fit_tree(name, args.criterion)


if __name__ == "__main__":
    main()


#                                          .-.
#                                   .-.   /    \
#     .--.      .--.    ___ .-.    ( __)  | .`. ;
#   /  _  \    /    \  (   )   \   (''")  | |(___)
#  . .' `. ;  |  .-. ;  | ' .-. ;   | |   | |_
#  | '   | |  |  | | |  |  / (___)  | |  (   __)
#  _\_`.(___) |  |/  |  | |         | |   | |
# (   ). '.   |  ' _.'  | |         | |   | |
#  | |  `\ |  |  .'.-.  | |         | |   | |
#  ; '._,' '  '  `-' /  | |         | |   | |
#   '.___.'    `.__.'  (___)       (___) (___)
