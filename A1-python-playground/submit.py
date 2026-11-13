#!/usr/bin/env python3
"""Grade your puzzles and write submission.json, which you upload to the course website."""

import importlib.util
import argparse
import sys
from pathlib import Path

_PYC = Path(__file__).parent / "grader" / "grader.pyc"

if not _PYC.exists():
    print(f"Error: grader file not found at {_PYC}")
    print("Ask your instructor for the grader file.")
    sys.exit(1)

_spec = importlib.util.spec_from_file_location("_grader", _PYC)
_grader = importlib.util.module_from_spec(_spec)
try:
    _spec.loader.exec_module(_grader)
except ImportError:
    print(f"Error: the grader needs Python 3.14, but this is Python {sys.version.split()[0]}.")
    print("Run `make submit-a` (or another letter), or `uv run python submit.py`.")
    sys.exit(1)

_ALL = list("abcdefghij")


def main():
    parser = argparse.ArgumentParser(
        description="Grade your puzzle solutions and write submission.json for the course website.",
        epilog="Examples:\n"
        "  uv run python submit.py           # grade all puzzles (or: make submit-all)\n"
        "  uv run python submit.py a b c     # grade specific puzzles (or: make submit-a)\n"
        "  uv run python submit.py --all     # grade all puzzles",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "puzzles",
        nargs="*",
        metavar="PUZZLE",
        help=f"Puzzle letter(s) to grade. Choose from: {', '.join(_ALL)}. Omit to grade all.",
    )
    parser.add_argument(
        "--all",
        dest="run_all",
        action="store_true",
        help="Grade all puzzles (default when no puzzles are specified).",
    )
    args = parser.parse_args()

    keys = _ALL if (args.run_all or not args.puzzles) else args.puzzles
    invalid = [k for k in keys if k not in _ALL]
    if invalid:
        parser.error(f"Unknown puzzle(s): {invalid}. Choose from: {_ALL}")

    keys = sorted(set(keys), key=_ALL.index)
    Path("submission.json").unlink(missing_ok=True)  # never leave an old one behind
    data = _grader.run_puzzles(keys)
    _grader.write_json(data, "submission.json")
    print(f"submission.json written  ({len(keys)} puzzle(s): {', '.join(keys)})")


if __name__ == "__main__":
    main()
