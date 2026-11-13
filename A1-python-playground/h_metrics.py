"""
Classification Metrics

After training a classifier you need to measure how well it performs. This
file computes the standard metrics for that: precision, recall and f1 for one
class, a report with one set of counts per class, and summary values of
precision, recall and f1 over all classes.

The code is finished, but it has three bugs: exactly one in each of the three
functions after `ConfusionCounts` (`binary_confusion`, `multiclass_report`
and `aggregate_metrics`). Your job is to find each bug and fix it with the
smallest change you can. Submit (`make submit-h`) and look at the results on
the course website to see which bugs are still there, then read the code
and the docstring to work out why.

There are also four questions: two about dataclasses, marked `Q1.` and
`Q2.`, and two about comparisons written by hand, marked `Q3.` and `Q4.`.
Read the demo function each one names, then fill in the answer variable.

The `@dataclass` decorator writes methods like `__init__`, `__repr__` and
`__eq__` for you, based on the fields. With `frozen=True`, the fields cannot
be changed after the object is created.
https://docs.python.org/3/library/dataclasses.html

The `@property` decorator lets you read a method like an attribute, without
the brackets.
https://docs.python.org/3/library/functions.html#property

`==` calls the method `__eq__` and `<` calls `__lt__`. A class can define
them itself to decide what "equal" and "smaller" mean for its objects.
https://docs.python.org/3/reference/datamodel.html#object.__lt__

Precision, recall and f1 are explained here:
https://en.wikipedia.org/wiki/Precision_and_recall

⭐ CORE: Q3 and Q4.

DO NOT MODIFY THE FUNCTION SIGNATURES OR THE DATACLASS FIELD DEFINITIONS.
"""

import sys
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# 1. ConfusionCounts  (dataclass, questions)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ConfusionCounts:
    """
    The four outcomes of binary classification for one class.

        tp -- true positives (predicted positive, actually positive)
        fp -- false positives (predicted positive, actually negative)
        fn -- false negatives (predicted negative, actually positive)
        tn -- true negatives (predicted negative, actually negative)

    The properties return 0.0 when their denominator would be zero:

        precision -- tp / (tp + fp)
        recall    -- tp / (tp + fn)
        f1        -- 2 * precision * recall / (precision + recall)
    """

    tp: int
    fp: int
    fn: int
    tn: int

    @property
    def precision(self) -> float:
        denom = self.tp + self.fp
        return self.tp / denom if denom else 0.0

    @property
    def recall(self) -> float:
        denom = self.tp + self.fn
        return self.tp / denom if denom else 0.0

    @property
    def f1(self) -> float:
        denom = self.precision + self.recall
        return 2 * self.precision * self.recall / denom if denom else 0.0


def equality_demo():
    return ConfusionCounts(1, 0, 0, 0) == ConfusionCounts(1, 0, 0, 0)


def frozen_demo():
    c = ConfusionCounts(1, 0, 0, 0)
    try:
        c.tp = 5  # type: ignore[misc]
    except Exception as e:
        return type(e).__name__
    return c.tp


###############################################################################
#  QUESTIONS Q1-Q2: fill in the answer variables below                        #
###############################################################################

# Q1. What does `equality_demo()` return? Give True or False.
EQUAL_COUNTS = None

# Q2. What does `frozen_demo()` return? If an exception is raised, give its
#     name as a string. Otherwise, give the new value of `c.tp`.
FROZEN_RESULT = None

###############################################################################


# ---------------------------------------------------------------------------
# 2. binary_confusion
# ---------------------------------------------------------------------------


def binary_confusion(y_true: list, y_pred: list, pos_label) -> ConfusionCounts:
    """
    Counts TP, FP, FN and TN by comparing two lists of labels of the same
    length. Only `pos_label` is the positive class; every other value is
    negative.

    Example:
        >>> binary_confusion([1, 0, 0], [1, 1, 1], pos_label=1)
        ConfusionCounts(tp=1, fp=2, fn=0, tn=0)
    """

    tp = fp = fn = tn = 0
    for true, pred in zip(y_true, y_pred):
        match (true == pos_label, pred == pos_label):
            case (True, True):
                tp += 1
            case (False, True):
                fn += 1
            case (True, False):
                fp += 1
            case (False, False):
                tn += 1

    return ConfusionCounts(tp=tp, fp=fp, fn=fn, tn=tn)


# ---------------------------------------------------------------------------
# 3. multiclass_report
# ---------------------------------------------------------------------------


def multiclass_report(y_true: list, y_pred: list) -> dict[str, ConfusionCounts]:
    """
    Returns the ConfusionCounts of every class that appears in `y_true` or
    in `y_pred`, with the keys in sorted order. Each class is counted
    one-vs-rest: that class is positive and all other classes are negative.

    Example:
        >>> r = multiclass_report(["a", "b", "a"], ["a", "a", "c"])
        >>> list(r)
        ['a', 'b', 'c']
        >>> r["c"]
        ConfusionCounts(tp=0, fp=1, fn=0, tn=2)
    """

    classes = sorted(set(y_true))
    return {cls: binary_confusion(y_true, y_pred, pos_label=cls) for cls in classes}


# ---------------------------------------------------------------------------
# 4. aggregate_metrics
# ---------------------------------------------------------------------------


def aggregate_metrics(
    report: dict[str, ConfusionCounts],
    y_true: list,
    strategy: str,
) -> dict[str, float]:
    """
    Combines a per-class report (from `multiclass_report`) into one set of
    summary numbers, using one of three strategies:

        "macro"    -- the plain mean of each class's precision, recall, f1

        "weighted" -- the mean of each class's precision, recall, f1,
                      weighted by its support. The support of a class is
                      the number of times it appears in `y_true`.

        "micro"    -- add up TP, FP and FN over all classes first, then
                      compute precision, recall and f1 from the totals

    Returns a dict with the keys "precision", "recall" and "f1", each
    rounded to 4 decimal places. Any other strategy raises ValueError.
    """

    match strategy:
        case "macro":
            n = len(report)
            p = sum(c.precision for c in report.values()) / n
            r = sum(c.recall for c in report.values()) / n
            f = sum(c.f1 for c in report.values()) / n

        case "weighted":
            total = len(y_true)
            support = {cls: c.tp + c.fp for cls, c in report.items()}
            p = sum(c.precision * support[cls] for cls, c in report.items()) / total
            r = sum(c.recall * support[cls] for cls, c in report.items()) / total
            f = sum(c.f1 * support[cls] for cls, c in report.items()) / total

        case "micro":
            pooled = ConfusionCounts(
                tp=sum(c.tp for c in report.values()),
                fp=sum(c.fp for c in report.values()),
                fn=sum(c.fn for c in report.values()),
                tn=0,
            )
            p, r, f = pooled.precision, pooled.recall, pooled.f1

        case _:
            raise ValueError(f"Unknown strategy {strategy!r}. Choose 'macro', 'weighted', or 'micro'.")

    return {
        "precision": round(p, 4),
        "recall": round(r, 4),
        "f1": round(f, 4),
    }


# ---------------------------------------------------------------------------
# 5. ClassScore  (questions)
# ---------------------------------------------------------------------------


class ClassScore:
    """
    The f1 score of one class. `__eq__` and `__lt__` are written by hand,
    so that scores can be compared and sorted by their f1.

    Both methods return `NotImplemented` when `other` is not a
    `ClassScore`. That is a special value, not an exception: it tells
    Python that this method does not know how to compare the two objects.
    """

    def __init__(self, name, f1):
        self.name = name
        self.f1 = f1

    def __eq__(self, other):
        if not isinstance(other, ClassScore):
            return NotImplemented
        return self.f1 == other.f1

    def __lt__(self, other):
        if not isinstance(other, ClassScore):
            return NotImplemented
        return self.f1 < other.f1

    def __repr__(self):
        return f"ClassScore({self.name!r}, {self.f1})"


def score_equality_demo():
    return ClassScore("cat", 0.5) == ClassScore("dog", 0.5)


def score_sorting_demo():
    scores = [ClassScore("cat", 0.8), ClassScore("dog", 0.5), ClassScore("bird", 0.9)]
    return [s.name for s in sorted(scores)]


###############################################################################
#  QUESTIONS Q3-Q4: fill in the answer variables below                        #
###############################################################################

# ⭐ CORE
# Q3. What does `score_equality_demo()` return? Give True or False.
EQUAL_SCORES = None

# ⭐ CORE
# Q4. What does `score_sorting_demo()` return? Give a list of strings.
SORTED_NAMES = None

###############################################################################


def _check(label, compute, expected):
    """Prints OK if `compute()` returns `expected`, NOT YET otherwise."""
    try:
        got = compute()
    except Exception as e:
        print(f"NOT YET: {label} raised {type(e).__name__}: {e}")
        return
    if got == expected:
        print(f"OK: {label}")
    else:
        print(f"NOT YET: {label} gave {got!r}, expected {expected!r}")


if __name__ == "__main__":
    # Small 3-class dataset: ground-truth labels vs. model predictions. The
    # model also predicts "fish", a class that is not in `y_true`.
    y_true = ["cat", "dog", "cat", "bird", "dog", "cat", "bird", "dog"]
    y_pred = ["cat", "cat", "cat", "bird", "dog", "cat", "fish", "dog"]

    # Build a per-class confusion matrix using one-vs-rest: each class is
    # treated as "positive" while all the others are "negative"
    report = multiclass_report(y_true, y_pred)

    # Print a table with precision, recall, F1, and raw counts for each class
    print(f"{'Class':<8} {'Prec':>7} {'Rec':>7} {'F1':>7}  Counts")
    print("-" * 50)
    for cls, counts in report.items():
        print(f"{cls:<8} {counts.precision:>7.3f} {counts.recall:>7.3f} {counts.f1:>7.3f}  {counts}")

    # Collapse the per-class metrics into one precision, recall and f1, with
    # each strategy. To see just one, pass it as a CLI argument:
    #   python h_metrics.py macro      (unweighted mean across classes)
    #   python h_metrics.py weighted   (mean weighted by class frequency)
    #   python h_metrics.py micro      (pool all TP/FP/FN, then compute)
    print()
    for strategy in sys.argv[1:] or ["macro", "weighted", "micro"]:
        try:
            print(f"Aggregate ({strategy}): {aggregate_metrics(report, y_true, strategy)}")
        except Exception as e:
            print(f"Aggregate ({strategy}) raised {type(e).__name__}: {e}")
    print()

    # Checks against the correct values. A NOT YET line means a bug is
    # still there, though not necessarily in the function the line names.
    _check(
        "binary_confusion([1, 0, 0], [1, 1, 1], pos_label=1)",
        lambda: binary_confusion([1, 0, 0], [1, 1, 1], pos_label=1),
        ConfusionCounts(tp=1, fp=2, fn=0, tn=0),
    )
    _check(
        'multiclass_report(["a", "b", "a"], ["a", "a", "c"])',
        lambda: multiclass_report(["a", "b", "a"], ["a", "a", "c"]),
        {
            "a": ConfusionCounts(tp=1, fp=1, fn=1, tn=0),
            "b": ConfusionCounts(tp=0, fp=0, fn=1, tn=2),
            "c": ConfusionCounts(tp=0, fp=1, fn=0, tn=2),
        },
    )
    correct_report = {
        "bird": ConfusionCounts(tp=1, fp=0, fn=1, tn=6),
        "cat": ConfusionCounts(tp=3, fp=1, fn=0, tn=4),
        "dog": ConfusionCounts(tp=2, fp=0, fn=1, tn=5),
        "fish": ConfusionCounts(tp=0, fp=1, fn=0, tn=7),
    }
    _check("multiclass_report on the demo data", lambda: multiclass_report(y_true, y_pred), correct_report)
    correct_summaries = {
        "macro": {"precision": 0.6875, "recall": 0.5417, "f1": 0.581},
        "weighted": {"precision": 0.9062, "recall": 0.75, "f1": 0.7881},
        "micro": {"precision": 0.75, "recall": 0.75, "f1": 0.75},
    }
    for name, summary in correct_summaries.items():
        _check(
            f'aggregate_metrics on the correct demo report, "{name}"',
            lambda name=name: aggregate_metrics(correct_report, y_true, name),
            summary,
        )
