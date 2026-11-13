"""
Word Frequency

This file is a small pipeline: it cleans up some text (`normalize`), counts
the words (`word_frequencies`), formats one line per word (`format_entry`),
and writes a report to a file (`write_report`).

The code is finished, but it has four bugs: exactly one in each function.
Your job is to find each bug and fix it with the smallest change you can.
Submit (`make submit-b`) and look at the results on the course website to
see which bugs are still there, then read the code and the docstring to
work out why.

The code uses two tools from the standard library:

- `defaultdict` is a dict that creates a missing value for you the first
  time you use a key, so `counts[word] += 1` just works.
  https://docs.python.org/3/library/collections.html#collections.defaultdict
- `pathlib.Path` represents a file path as an object, with methods to check,
  read, and write files.
  https://docs.python.org/3/library/pathlib.html

This file has no ⭐ CORE parts.

DO NOT MODIFY THE FUNCTION SIGNATURES OR THE STOPWORDS SET.
"""

from collections import defaultdict
from pathlib import Path


STOPWORDS = {
    "a",
    "an",
    "the",
    "and",
    "or",
    "but",
    "so",
    "yet",
    "for",
    "nor",
    "to",
    "of",
    "in",
    "on",
    "at",
    "by",
    "up",
    "as",
    "is",
    "it",
    "its",
    "be",
    "was",
    "are",
    "were",
    "been",
    "has",
    "have",
    "had",
    "do",
    "does",
    "did",
    "will",
    "would",
    "could",
    "should",
    "may",
    "might",
    "i",
    "me",
    "my",
    "we",
    "our",
    "you",
    "your",
    "he",
    "she",
    "his",
    "her",
    "they",
    "them",
    "their",
    "this",
    "that",
    "with",
    "from",
    "not",
    "no",
    "if",
    "then",
    "than",
    "also",
    "just",
    "more",
    "into",
}


def normalize(text: str) -> list[str]:
    """
    Turns raw text into a list of lowercase words.

    Split the text on whitespace and lowercase every word. Drop tokens that
    have no letters (like "42" or "!!!") and drop every word in STOPWORDS.
    Stopwords must be removed whatever their capitalization: "The" and "the"
    are both dropped.
    """

    return [
        token.lower()
        for token in text.split()
        if any(c.isalpha() for c in token)
        and token not in STOPWORDS
    ]  # fmt: skip


def word_frequencies(words: list[str]) -> dict[str, int]:
    """
    Counts each word and returns a dict ordered by count, highest first.

    Words with the same count are ordered alphabetically (A to Z).
    """

    counts: defaultdict[str, int] = defaultdict(int)
    for word in words:
        counts[word] += 1
    ordered = sorted(counts.items(), key=lambda p: (p[1], p[0]), reverse=True)
    return dict(ordered)


def format_entry(rank: int, word: str, count: int, total: int) -> str:
    """
    Formats one line of the report: rank, word, count, and percentage.

    The layout, from left to right:

    - rank: right-aligned, width 4, then a period and a space
    - word: left-aligned, width 20
    - count: right-aligned, width 6
    - percentage of `total`: right-aligned, width 8, two decimals, then "%"

    For example, `format_entry(1, "python", 42, 200)` gives
    `'   1. python                  42   21.00%'`.

    Hint: https://docs.python.org/3/library/string.html#format-specification-mini-language
    """

    pct = count // total * 100
    return f"{rank:>4}. {word:<20}{count:>6}{pct:>8.2f}%"


def _is_file(source: str) -> bool:
    # A long text can be an invalid file name, which makes the OS raise an
    # error. That just means "not a file".
    try:
        return Path(source).is_file()
    except OSError:
        return False


def write_report(source: str, output_path: str | Path, top_n: int = 10) -> None:
    """
    Runs the whole pipeline and writes the report to `output_path`.

    `source` is either the path of a text file or the text itself: if a file
    exists at that path, read the text from it, otherwise use `source` as the
    text. Create missing folders for `output_path`. The report is a header
    line, a separator line, and then one `format_entry` line for each of the
    `top_n` most frequent words. Running the function again with the same
    `output_path` replaces the old report.

    Raises an IOError (with a clear message) if reading or writing fails.
    """

    try:
        if _is_file(source):
            text = Path(source).read_text()
        else:
            text = source

        words = normalize(text)
        top_words = list(word_frequencies(words).items())[:top_n]

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        mode = "a"
        with path.open(mode) as f:
            f.write(f"{'Rank':>5} {'Word':<20}{'Count':>6}{'   %':>8}\n")
            f.write("-" * 42 + "\n")
            for rank, (word, count) in enumerate(top_words, start=1):
                line = format_entry(rank, word, count, len(words))
                f.write(line + "\n")

    except OSError as e:
        raise IOError(f"Report generation failed: {e}") from e


if __name__ == "__main__":
    sample_text = """
    To be or not to be that is the question whether tis nobler in the mind
    to suffer the slings and arrows of outrageous fortune or to take arms
    against a sea of troubles and by opposing end them to die to sleep no
    more and by a sleep to say we end the heartache and the thousand natural
    shocks that flesh is heir to tis a consummation devoutly to be wished
    """

    print("Running on raw string...")
    write_report(sample_text, "output/raw_report.txt", top_n=10)
    print("Report written to output/raw_report.txt")

    print("Running on file...")
    sample_path = Path("output/sample.txt")
    sample_path.write_text(sample_text)
    write_report(str(sample_path), "output/file_report.txt", top_n=10)
    print("Report written to output/file_report.txt")

    def check(label, get, expected):
        """Print OK if `get()` returns `expected`, NOT YET otherwise."""
        try:
            got = get()
        except Exception as e:
            print(f"NOT YET: {label} (raised {type(e).__name__}: {e})")
            return
        if got == expected:
            print(f"OK: {label}")
        else:
            print(f"NOT YET: {label}\n    expected {expected!r}\n    got      {got!r}")

    def header_count_after_two_runs():
        """How many header lines the report has after writing it twice."""
        write_report(sample_text, "output/twice_report.txt", top_n=10)
        write_report(sample_text, "output/twice_report.txt", top_n=10)
        lines = Path("output/twice_report.txt").read_text().splitlines()
        return sum(line.startswith(" Rank") for line in lines)

    # Smoke test: compares each function with what its docstring says.
    print()
    check(
        "normalize drops stopwords whatever their capitalization, and tokens without letters",
        lambda: normalize("The the 42 !!! Python"),
        ["python"],
    )
    check(
        "word_frequencies orders by count, highest first, then alphabetically",
        lambda: list(word_frequencies(["b", "a", "b", "c"]).items()),
        [("b", 2), ("a", 1), ("c", 1)],
    )
    check(
        'format_entry(1, "python", 42, 200) matches the docstring',
        lambda: format_entry(1, "python", 42, 200),
        "   1. python                  42   21.00%",
    )
    check("write_report replaces the old report (one header line after two runs)", header_count_after_two_runs, 1)
