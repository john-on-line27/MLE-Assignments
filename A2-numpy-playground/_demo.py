"""
Runs the examples at the bottom of a puzzle file. You don't need to read this file.

`run(label, example)` calls `example()` and prints its result after `label`.
If the example raises an error, it prints the error in one line instead, and
the examples after it still run.
"""

from collections.abc import Callable
from typing import Any


def run(label: str, example: Callable[[], Any]) -> None:
    """Prints `label` and what `example()` returns, or the error it raises."""

    try:
        result = example()
    except Exception as e:  # noqa: BLE001 - any error becomes one line of output
        print(f"{label} crashed ({type(e).__name__}: {e})")
        return
    text = str(result)
    # Arrays with several rows start on their own line, so the rows line up.
    print(f"{label}\n{text}" if "\n" in text else f"{label} {text}")
