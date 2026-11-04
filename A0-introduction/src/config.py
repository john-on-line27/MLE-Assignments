"""Where the project keeps its files, and the default random seed."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"  # data/<name>/train.csv, val.csv, test.csv
MODELS_DIR = ROOT / "results" / "models"  # fitted trees, saved as JSON
SEED = 42


def model_path(dataset: str, criterion: str) -> str:
    """Where the tree grown on a dataset with a given criterion is saved."""
    path = MODELS_DIR / f"{dataset}_{criterion}.json"
    return MODELS_DIR / f"{dataset}_{criterion}.json"


r"""
          _
        _/-\_
    .-`-:-:-`-.
    /-:-:-:-:-:-\
    \:-:-:-:-:-:/
     |`       `|
     |         |
     `\       /'
       `-._.-'
          `

    Mighty oaks from little acorns grow.
"""
