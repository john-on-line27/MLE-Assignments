"""
Generate toy 2D datasets, split each into a train, a validation and a test
set (60% / 20% / 20%), and save them to data/<name>/train.csv, val.csv and
test.csv.

Usage:
    python scripts/create_datasets.py moons circles --n 1000
    python scripts/create_datasets.py all
"""

import argparse

from config import SEED
from data import GENERATORS, save_dataset, train_test_split


def create_dataset(name, n, val_size, test_size, seed):
    """Generate one dataset, split it, and save all three splits.

    val_size and test_size are fractions of all n points.
    """
    X, y = GENERATORS[name](n=n, seed=seed)
    # first cut off the test set, then cut the validation set from the rest
    X_rest, X_test, y_rest, y_test = train_test_split(X, y, test_size, seed)
    X_train, X_val, y_train, y_val = train_test_split(
        X_rest, y_rest, val_size / (1 - test_size), seed
    )
    save_dataset(name, "train", X_train, y_train)
    save_dataset(name, "val", X_val, y_val)
    save_dataset(name, "test", X_test, y_test)
    print(
        f"{name}: {len(y_train)} train, {len(y_val)} val and "
        f"{len(y_test)} test points"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("datasets", nargs="+", choices=[*GENERATORS, "all"])
    parser.add_argument("--n", type=int, default=1000, help="number of points")
    parser.add_argument("--val-size", type=float, default=0.2)
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()

    names = list(GENERATORS) if "all" in args.datasets else args.datasets
    for name in names:
        create_dataset(name, args.n, args.val_size, args.test_size, args.seed)


if __name__ == "__main__":
    main()
