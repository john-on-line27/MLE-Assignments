# fmt: off
r"""
                                   * ^ ^
                                  ^^^_ _/
                                ^  `^,|
                            * ^     ^^|    /
                              ^   ^___ *_ ,^^
                             '^,.^_',_|^^'^ / /
                            ^ ^''^_^``|_*_^''   ^
                    ^^^ * ^^ ^  ^'_''_ ''''_ ^^^/
                       \. ...-'^*,' '_ _ ,''^.     ^
                       ^ `' _,_^*^_ _' ^'^^'',`^
                      ^^  ^^'_'' '`''^|_^_^^_    ^- ^
                   ^  .- .*.,^^`''_''` '__''_'^,' ''^   ^^^
                    ^*  ,,^,._^___`_`,|''` '^^'^''^^--  .. -
                   ^ ^- `.-,'''_ ',''_|^_^_^_ _^^  '' ,^`'    *
                 ^.*''^^- ^_''',,_'_`,|'_'__''_*'^ _^._* --^^*   ^^
        * ^^  ^ ^ ^^,-^.^`^,'_`'__''^_|`_''_*^*__''*'^`^'' .  .
       ^^^^  ^* ^ `' -- __.`, '`^_`^`^|,^__''_,^__-^.__'^-''^ '^
       -  .-- ^^^ . ^^'*__`^_'`','_^''|^''`'_^^,'^,`''''---^-^. .^^ ^ ^
       ' ^^^  -^-'`*^.__'_ __,,_^__'^`|__,`'^',`___*'' ',  ''-.' '--..
           - -',    '''''_ _`,'  ','''|_'_'___  _`'.-.  -.` ,   ,'`
"""
# fmt: on
"""
A decision tree classifier, written from scratch.

A decision tree sorts a point into a class by asking it a chain of yes/no
questions such as "is x[0] <= 0.37?". Each answer sends the point left or
right, until it reaches a leaf that holds the prediction.

We grow the tree greedily, from the top down. At each node we pick the
question that best separates the classes, which is the one that lowers the
impurity (how mixed the labels are) the most:

    gini(S)    = 1 - sum_c p_c^2
    entropy(S) = - sum_c p_c * log2(p_c)
    gain       = I(S) - |L| / |S| * I(L) - |R| / |S| * I(R)

Here S is a list of labels, p_c is the fraction of S that has class c, I is
gini or entropy, and L and R are the labels that go left and right.

Throughout, X is a list of rows (the feature values of one point each) and
y holds the class label of each row.
"""

import json
import math
from collections import Counter
from collections.abc import Callable
from dataclasses import asdict, dataclass
from pathlib import Path

# -----------------------------------------------------------------------------
# impurity: how mixed is a list of labels?


def gini(y: list[int]) -> float:
    """Chance that two labels picked at random (with replacement) differ."""
    if not y:
        return 0.0
    n = len(y)
    return 1.0 - sum((count / n) ** 2 for count in Counter(y).values())


def entropy(y: list[int]) -> float:
    """Average number of bits needed to say which class a label is."""
    if not y:
        return 0.0
    n = len(y)
    return -sum(
        count / n * math.log2(count / n) for count in Counter(y).values()
    )


# an impurity function, such as gini or entropy, scores a list of labels
Impurity = Callable[[list[int]], float]


def information_gain(
    y: list[int], left: list[int], right: list[int], impurity: Impurity
) -> float:
    """How much purer the labels get when y is split into left and right."""
    assert len(left) + len(right) == len(y) > 0
    n = len(y)
    return (
        impurity(y)
        - len(left) / n * impurity(left)
        - len(right) / n * impurity(right)
    )


IMPURITIES: dict[str, Impurity] = {"gini": gini, "entropy": entropy}

# -----------------------------------------------------------------------------
# splitting: which question separates the classes best?


@dataclass
class Split:
    feature: int  # which column of X the question looks at
    threshold: float  # rows with x[feature] <= threshold go left
    gain: float  # how much purer the two sides are than the parent


def midpoints(values: list[float]) -> list[float]:
    """Thresholds worth trying: halfway between each pair of neighbors."""
    unique = sorted(set(values))
    return [(a + b) / 2 for a, b in zip(unique, unique[1:])]


def best_split(
    X: list[list[float]], y: list[int], impurity: Impurity
) -> Split | None:
    """Try every feature and every threshold; keep the one with most gain."""
    best = None
    for feature in range(len(X[0])):
        column = [row[feature] for row in X]
        for threshold in midpoints(column):
            left = [label for v, label in zip(column, y) if v <= threshold]
            right = [label for v, label in zip(column, y) if v > threshold]
            gain = information_gain(y, left, right, impurity)
            if gain > 0 and (best is None or gain > best.gain):
                best = Split(feature, threshold, gain)
    return best


# -----------------------------------------------------------------------------
# the tree


@dataclass
class Node:
    prediction: int  # most common label among the rows that reached here
    n_samples: int  # how many training rows reached here
    split: Split | None = None  # the question asked here; None for a leaf
    left: Node | None = None  # where rows go that answer yes
    right: Node | None = None  # where rows go that answer no


def majority(y: list[int]) -> int:
    """The most common label; ties go to the smaller label."""
    return max(sorted(set(y)), key=y.count)


class DecisionTree:
    """A tree of yes/no questions, grown greedily from training data."""

    def __init__(self, criterion: str = "gini"):
        if criterion not in IMPURITIES:
            raise ValueError(
                f"criterion must be 'gini' or 'entropy', not {criterion!r}"
            )
        self.criterion = criterion
        self.impurity = IMPURITIES[criterion]
        self.root: Node | None = None

    def fit(self, X: list[list[float]], y: list[int]) -> DecisionTree:
        """Grow the tree on the training rows X and their labels y."""
        assert len(X) == len(y) > 0
        self.root = self._grow(X, y)
        return self

    def _grow(self, X: list[list[float]], y: list[int]) -> Node:
        """Grow the subtree for the rows X and their labels y."""
        node = Node(prediction=majority(y), n_samples=len(y))

        pure = len(set(y)) == 1
        if pure:
            return node

        node.split = best_split(X, y, self.impurity)
        if node.split is None:  # no question makes the labels any purer
            return node

        # send each row left or right by its answer, then grow both sides
        X_left, y_left, X_right, y_right = [], [], [], []
        for row, label in zip(X, y):
            if row[node.split.feature] <= node.split.threshold:
                X_left.append(row)
                y_left.append(label)
            else:
                X_right.append(row)
                y_right.append(label)
        node.left = self._grow(X_left, y_left)
        node.right = self._grow(X_right, y_right)
        return node

    def predict(
        self,
        X: list[list[float]],
        max_depth: int | None = None,
        min_samples_split: int = 2,
    ) -> list[int]:
        """Predict a label for every row in X; see predict_one."""
        return [
            self.predict_one(x, max_depth, min_samples_split)[0] for x in X
        ]

    def predict_one(
        self,
        x: list[float],
        max_depth: int | None = None,
        min_samples_split: int = 2,
    ) -> tuple[int, int]:
        """Walk one row down the tree; return its label and the depth reached.

        max_depth and min_samples_split end the walk early: at that depth, or
        at a node that fewer than min_samples_split training rows reached.
        This gives exactly the tree that a depth or size limit during fitting
        would have grown, because each split depends only on the rows that
        reach that node. So one full tree serves every setting.
        """
        node, depth = self.root, 0
        while node.split is not None:
            if max_depth is not None and depth >= max_depth:
                break
            if node.n_samples < min_samples_split:
                break
            if x[node.split.feature] <= node.split.threshold:
                node = node.left
            else:
                node = node.right
            depth += 1
        return node.prediction, depth


# -----------------------------------------------------------------------------
# saving and loading


def save_tree(tree: DecisionTree, path: str | Path) -> None:
    """Write a fitted tree, and the settings it was grown with, to JSON."""
    settings = {"criterion": tree.criterion}
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(
            {"settings": settings, "root": asdict(tree.root)}, f, indent=2
        )


def load_tree(path: str | Path) -> DecisionTree:
    """Read a tree written by save_tree, ready to predict."""
    with open(path) as f:
        saved = json.load(f)
    tree = DecisionTree(**saved["settings"])
    tree.root = node_from_dict(saved["root"])
    return tree


def node_from_dict(d: dict | None) -> Node | None:
    """Rebuild a saved node, and every node below it."""
    if d is None:
        return None
    split = Split(**d["split"]) if d["split"] else None
    left, right = node_from_dict(d["left"]), node_from_dict(d["right"])
    return Node(d["prediction"], d["n_samples"], split, left, right)


#       ^  ____   __ __ __ __  |^|  ^ ^` ) |^`(: | _ __ _  _ _ __ _ __ _ _^^^ ^
#      - - ' ,'',        '` `''^ *)*'^||^^  |^^* ^ '' ' ' ''` '   `'    ,   -
#  '  '``             ^   ^  ^ |^ * _ (' ^ *| ** '^   ^ ^ ^   * ^^^        ''
#                ^^ ^  ^^  ^ ^*|*'| | '| |^_^|^*,|^^  ^ ^^^^^^ ^^*^^^^^     ^
#       ^^    ^___   _ ___   __^|^| * |^ |^^^::) |_ ___    __ _  ___ _ ^ ^
#   '..  . .  -  ', ',    ', ',|) | ^ ^' |   |:^'|' ''     ,     ' '  '.-  .
#       ' '   ,    ^ ^   ^   ^^| :  |||  |^^'_|` ^|                     '`    '
#           ^     ^^^*^^^^ ^ ^^| '  |^|  ( '|^^^  |
#              ^ ^ ___  _ _ __| '^  ^|| .|' ^ ||  `
#               -.'  ',',     |*)^^|^*|  ^  ( ||  |^ ^   ^ *^
#           ,,                | ^^^|^^| )^  |^^   |^^^^ ^ ^  ^  ^
#                ^ ^   ^    ^^| |' ' ^^ | ^^)*|^  ^__^___^  __*   ^
#                ^^^^ ^^* ^ ^^| || ^  :^|   | |^^ |'  ^'`*`, ^-.*. .'
#                .  _ ___ ____|^||^)' (^|^  , ^^  |_  ____^_^  `'^
#        ,.       '^   '  ^  '| || ^  ||     ,||  |' ^ `, ^'  - -  .
#         '     ^ ^^   ^ ^^^^ | || _    |^^ |  | '|__  _   _  `'  ^ ^
#         ^^ ^^_      ________| |) ' ^ ||   |  ^ **'  '',`'`'   -  .-,
#    `    --. -      '' '    `^ ,| :   |    ' *   ^^^  ^^   *^,  ,
#     ,'      '               | :| |   ^|     ||  |___ ___  __^^^
#                             |^ |'|^  |`  '| |^  |'` '  '   '-  -. `
#                             || ' |'  | ^ `| *|  |   ^        '
#                             |  | |   ||  `| |:^^^^^ *^^  ^
#                      ^^^  ^^(| *^:   |)' |  |   |_  _    ^^
#                     * _____ ^^ ^|| ^ ||  | ^|(  |,   ' ' --. `
#                       `   ' |   || *)'      ||  )          '
#                    '        ||  |(  |) |    (|| |
#                        ^    |^  |: '|| | | ^|)| |^    *
#                ^  ^^*^*    ^|:  :|  '| | |  ||| |    ^^^^^  ^     ^
#        ^    ^  _     _  _  _|| ^||  | :|^   | | |__^ _     _  ^
#       '....   -   ' ,  ,,  |(^ ||   | (| |  )  ^ | ^`','     ...    `
#          '              ^^ ||  ||   |  |  | |* | | .-
#                      ^   __||  |^   )^||  | |  ' ^,
#                     '   `  (|    '  | ||  | ^  | |
#                       `    |^  ||   | )|    | ( ||
#                            ||  |:   ) ||  | (  ' ^
#                            ||  ||  |  )|  | | ||^|
#                            (  | |     ||  | ) || |
#                            || ||  .|  |)  |^| |^ |^
#                            || :(   |  ||    ' |  |* ^ ^
#                            || |:     ) |  | | || |_ _  _^^*
#                            (| | |  | | (  ' |  | | ,    - - `
#                            || | |  | | |  ^ | || |      '  '
#                            |) | | |  |  | ||  || |
#                            || | | |  |. ( (|  |: |
#                            || | ) :  |  |`|    | |
#                            (| ` | |  |  | ')  |( |
#                            | .|  ||  |  | ||  || |
#                            |  |  ||  |(@) || `|) |
#                            || |  ||  |  | ||  || |
#                            ( |  | )  |  ' |   :| |
#                            | |: | |  |  | ||  || |
#                            | || | |  |    ||  || )^^     ^*
#                            | ||   |  |    |:  :| |_  ___   ^
#                            | |: ' |  )  | |   |  |'       . ,
#                            ( :|  ||     ) |   )| |      `
#                            | ||  ||  |  | |    |`|
#                            | |'  ||     |     || |
#                            | |:  :|  |  | :   |  |
#                            (  |   (  )  ||    |  |
#                            |  |  ||  |  )||   |  |
#                            |  |  ||  (  |||   |  |
#                            | ||   )  |  ||       |
#                            | (|         |:'   (  |
#                            | || , '( |  | |   |  )
#                            ( ||   || :   ||  ||  |
#                      ______| ||   |  |   (|  |(  |
#                   -=(______| | |  || |   |(| |)  |
#                            | | (   | :   ||| |)  |
#                            (  ||  : |    ||) ||  |
#                            |  ||  | ||   ||| |:  |
#                            |   |  | ||   ||| || ,|
#                            (  ||  ) (    |': )   |
#                            |  ||  | )|   |'  :|  |
#                            |  ||  | |    ||   |  |
#                            |  |   | |     |  :|  |
#                            (  :   '||        |   |
#                            |  |   ' |     |  ||  |
#                            |  |   | |        ||  |
#                            |  (     |     |  |:  |
#                            |' '   | |     |  ||  |__
#                            |  |   | :     || ||  |__)
#                            |  (           || '   |
#                            |  (|  | '     :|' |  |
#                            |  ||  |||     |  )|  |
#                            |  |)  ||      ||  )  |
#                            |  |)  || )    |  ||  )
#                            |  ||  || |    |  ||  |
#                            |  ||  ||      (      |
#                            |  ||  || |    || ||  |
#                            |  | | || |    || )   |
#                            |  : | ||     ||:     )
#                     ^ ^ ^^ |  | | )( |   (|| ||  |
#                     ^^ ^   |  | | |'     ||  |:  |
#                  ^^   ____ |  | | ||:    | : ()  |
#                ,    ''  ,  | |  ) || |     | ||  )
#                  `         | )  | |)     ) :  |  |
#                            | |  | || |   : | ||  |
#                            | |  |  | :   | | ||  |
#                            | | .| :  |   ' |  |  |
#                            | |  | )| | , ' | | | |
#                            | |  | || |   | | | | |
#                            | |  | || )   | | |   |
#                            | ' |  || )   | | ( | |
#                            | ||   |(     | |  || )
#                            | |     ' |   | |  |  |
#                            ( ||   )| :   | |  || |
#                            |  |   )| |   | :  || |
#                            ( ||   |) |   |  | |  |
#                            | )(   || |   )|   |: |______
#                            ( |)   |      |(|  || |______)=-
#                            | |(   || |   )|   || |
#                            |,|    |  )   |    (| |
#                            | |'    | |   ||   |) |
#                            (  )   || |   ||   ) ||
#                            | ||   )| )   ||     ||
#                            | ||   '|  ( ) |   )  |
#                            | ||   )|` ) |     || )
#                            | | |  ||  |  |    |: |
#                            | | |  ||  '  ||   || |
#                            ( | | (@)  |  ||   || |
#                            | ) |  )| `|  |    |: |
#                            | :  ) (|  |  ||   || |
#                            | |  ) (|  |  ||  | ' |
#                            | |(@) )|  |  |'  | | |
#                            |    | '|     )|   | .|
#                          __| |  | ||  )   |   || |
#                         (__| |  ' ||  :  :)    | |
#                            | |  ( ||  |  ||   |( |
#                            | '    ||  |  |'   || |
#                            | |   ||   )  |(   |  |
#                            | |   |||     || . || |
#                            | |   ( |   | |    |  )
#                            | |    ||   | ||   || |
#                            | '   :|    | |    || |
#                            | |   |||   | ||   |( |
#                            | |   |)  . | :)   |) |
#                            | |   |((   | |:   |( )
#                            |  |  | |   ) )    || |
#                            |  (  |||   | |    (| |
#                            |  |   `)   | |     | )
#                            |  |   ||  ( ||     | |
#                            | |   '|   | |      | |
#                            ||    |||  | |      | |
#                            ||     (|  | |      ) |
#                            ||     :|  |'|    ` : |
#                            |      |:  |||      | )
#                            ||     ||  ||     (@) )
#                            (| `   ||  |||      | |
#                            ||     )|  (||      | |
#                           /  |  |  (  |  )  |  |  \
#                         _/   |  |  |  |  |  |  |   \_
#                      __/  /  |  )  |  :  |  (  |  \  \__
#   ~~~~~~~~~~~~~~~~__/   _/  /|  |  |  |  |  |  |\  \_   \__~~~~~~~~~~~~~~~~
#               ___/    _/   / |  |  |     |  |  | \   \_    \___
#         _____/    ___/   _/  /  |__|     |__|  \  \_   \___    \_____
#    ____/    _____/    __/  _/  /             \  \_  \__    \_____    \____
#  _/    ____/      ___/   _/   /   _       _   \   \_   \___      \____    \_
# /   _-'      ___-'     _/    /  _/         \_  \    \_     `-___      `-_   \
#   ,'       ,'        ,'    ,'  /             \  `,    `,        `,       `,
