#!/usr/bin/env python3
"""Check your worksheet answers and write submission.json to upload."""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PYC = HERE / "grader" / "grader.pyc"

if not PYC.exists():
    sys.exit(f"Grader not found at {PYC}. Ask your instructor for it.")

spec = importlib.util.spec_from_file_location("_grader", PYC)
grader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grader)

TASKS = list(grader.TASKS)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Write submission.json from your worksheet.py answers."
    )
    parser.add_argument(
        "tasks",
        nargs="*",
        metavar="TASK",
        help=f"task letters to submit ({' '.join(TASKS)}); default: all",
    )
    args = parser.parse_args()

    tasks = args.tasks or TASKS
    unknown = [t for t in tasks if t not in TASKS]
    if unknown:
        hint = " (task b has no questions)" if "b" in unknown else ""
        parser.error(f"unknown task(s) {unknown}{hint}; use {TASKS}")

    tasks = sorted(set(tasks), key=TASKS.index)
    data = grader.run_puzzles(tasks, HERE)
    grader.write_json(data, HERE / "submission.json")
    print(f"Wrote submission.json (tasks: {', '.join(tasks)})")


if __name__ == "__main__":
    main()
