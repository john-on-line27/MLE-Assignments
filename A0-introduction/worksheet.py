"""
Your answers to the questions in the task prompts.

Each question is copied here as a comment, followed by the kind of answer
it expects or the options to choose from. Replace `None` with your answer,
then run `make submit` to create submission.json.
"""

# -----------------------------------------------------------------------------
# Task A — Introduction

# Question A1. `AGENTS.md` gives the assistant a name. What is it?
#
# Answer with the name, as a string.
a1_agent_name: str | None = "Bender"

# -----------------------------------------------------------------------------
# Task C — Data

# Question C1. What is the default seed?
#
# Answer with a whole number.
c1_default_seed: int | None = 42

# Question C2. Look through the rest of `src/config.py`. Is there another
# seed in there?
#
# Answer with a string, such as "twine".
c2_other_seed: str | None = "acorns"

# Question C3. Read through `src/data.py`. Besides the data generators, what
# other kind of generator can you find in it?
#
# Answer with one letter, as a string, such as "cord".
c3_other_generator: str | None = "gas"

# Question C4. Find the last section of `src/data.py`. What is the name of
# the function just above it?
#
# Answer with the function name, as a string, without parentheses or arguments.
c4_function_name: str | None = "train_test_split"

# -----------------------------------------------------------------------------
# Task D — Fitting

# Question D1. `DecisionTree` has no maximum depth while it is fitted. The
# maximum depth, together with `min_samples_split`, turns up as an argument
# of two public methods instead. Their names start the same way. Give the
# part they share.
#
# Answer with the shared start of their names, as a string.
d1_method_prefix: str | None = "predict"

# Question D2. While you're in `src/tree.py`: how many lines tall is the
# tree?
#
# Answer with a whole number.
d2_tree_height: int | None = 20

# Question D3. What sort of font can you find in `scripts/fit_tree.py`?
#
# Look in the file and answer with one letter, as a string, such as "a".
d3_font: str | None = "serif"

# Question D4. How many training points reached the root?
#
# Answer with a whole number.
d4_root_samples: int | None = 600

# Question D5. Which feature does the root's question look at? Give the
# number stored under `feature`.
#
# Answer with a whole number.
d5_root_feature: int | None = 1

# -----------------------------------------------------------------------------
# Task E — Evaluation

# Question E1. Which dataset needs the deepest tree to reach about 90%
# accuracy?
#
# Answer with the dataset name, as a string, such as "xor".
e1_deepest_dataset: str | None = "checkerboard"

# Question E2. The `linear` dataset is split by a single straight line, yet
# a tree needs quite a few questions to get it right. Why?
#
#   a) the training set is too small to find the line
#   b) the line is diagonal, but each question can only cut straight across
#      or straight up and down
#   c) the validation points are noisier than the training points
#   d) Gini impurity can't measure straight lines
#
# Answer with one letter, as a string, such as "a".
e2_linear_reason: str | None = "b"

# Question E3. How many false positives does the `moons` tree make on the
# validation set?
#
# Answer with a whole number.
e3_false_positives: int | None = 8

# Question E4. A smoke alarm goes off because you burned your toast. Which
# kind of error is that?
#
#   a) a Type I error (false positive)
#   b) a Type II error (false negative)
#
# Answer with one letter, as a string, such as "a".
e4_smoke_alarm: str | None = "a"

# Question E5. At the largest depths, the training accuracy is perfect, but
# the validation accuracy is lower than its best. What is happening there?
#
#   a) underfitting
#   b) overfitting
#   c) neither
#
# Answer with one letter, as a string, such as "a".
e5_deep_tree: str | None = "b"

# Question E6. At which depth is the validation accuracy of the `moons` tree
# highest?
#
# Answer with a whole number.
e6_best_depth: int | None = 6

# -----------------------------------------------------------------------------
# Task F — Development (Extra)

# Question F1. Which of these is *not* a hyperparameter of our tree?
#
#   a) the criterion
#   b) the maximum depth
#   c) the threshold of the root's question
#   d) min_samples_split
#
# Answer with one letter, as a string, such as "a".
f1_not_hyperparameter: str | None = None

# Question F2. With 5-fold cross-validation, how many trees are fitted to
# score a single combination of hyperparameters?
#
# Answer with a whole number.
f2_trees_per_setting: int | None = None

# Question F3. Thanks to this trick, how many trees does the search with 2
# criteria, 6 depths and 5 folds actually fit?
#
# Answer with a whole number.
f3_trees_fitted: int | None = None

# Question F4. Which criterion does the best combination use?
#
# Answer with "gini" or "entropy".
f4_best_criterion: str | None = None

# Question F5. Which maximum depth does the best combination use?
#
# Answer with a whole number, or -1 for no limit.
f5_best_depth: int | None = None

# Question F6. What is the test accuracy of your final tree? Copy it as it's
# printed.
#
# Answer with a decimal number, such as 0.123.
f6_test_accuracy: float | None = None

# -----------------------------------------------------------------------------
# Task G — Wrap-up

# Question G1. Which file makes sure everyone installs exactly the same
# version of every package?
#
#   a) pyproject.toml
#   b) uv.lock
#   c) Makefile
#   d) .gitignore
#
# Answer with one letter, as a string, such as "a".
g1_versions_file: str | None = None

# Question G2. Which part of the data do you use to compare versions of a
# model, for example trees of different depths?
#
#   a) the training set
#   b) the validation set
#   c) the test set
#
# Answer with one letter, as a string, such as "a".
g2_compare_split: str | None = None

# Question G3. Why are `data/` and `results/` listed in `.gitignore`?
#
#   a) Git can't store CSV or JSON files
#   b) they hold secrets that shouldn't be shared
#   c) everything in them can be created again from the code, the data
#      generators and the seed
#   d) they're only used in Task F
#
# Answer with one letter, as a string, such as "a".
g3_ignored_reason: str | None = None

# Question G4. What does `git add` do?
#
#   a) it saves a new commit
#   b) it stages files, so they're part of the next commit
#   c) it turns the folder into a Git repository
#   d) it uploads your work to the course website
#
# Answer with one letter, as a string, such as "a".
g4_git_add: str | None = None

# Question G5. What happens when a pre-commit check fails?
#
#   a) the commit is made anyway, with a warning
#   b) the commit stops, and you fix the problem and commit again
#   c) Git deletes the files that failed
#   d) nothing, the checks only run on the course website
#
# Answer with one letter, as a string, such as "a".
g5_failed_check: str | None = None
