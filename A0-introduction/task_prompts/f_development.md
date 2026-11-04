# Task F — Development

The last step of the pipeline is to repeat: change the model, evaluate it again, and keep the best version. In this task, you'll search for the best settings for a tree on the `moons` dataset, and then test your final tree, just once, on the test set.

This whole task is **Extra**, questions included. It shows how model development usually works in practice, so it's well worth a read, but feel free to skip to Task G if you're short on time.


## What does "best" mean?

So far, "best" has meant the highest accuracy. In real projects, the goal depends on the situation:

- The model has to run on a small device with little memory. Then the tree may only have a limited number of nodes.
- The model answers billions of requests a day. Then each prediction has to be fast, and a tree that asks fewer questions is better.
- One kind of mistake is much worse than the other (Task E). Then we're happy to give up some accuracy in exchange for fewer of the bad mistakes.

So as a part of developing a model, decide what you want to improve. In this task, we're after the highest accuracy.


## Hyperparameters

The questions inside a tree are learned from the data during fitting. Some settings aren't learned, though: we choose them ourselves, usually before fitting. These settings are called **hyperparameters**. For our tree, the two most important ones are:

- the **criterion**: `gini` or `entropy` (Task D),
- the **maximum depth**: the largest number of questions a point may be asked.

There's a third one, `min_samples_split`, which we'll leave at its default value.

Developing the model means trying different hyperparameters and comparing the results on validation data.

> ❓ **Question F1.** Which of these is *not* a hyperparameter of our tree?


## Cross-validation

In Task E, we used one validation set, `val.csv`. One validation set has a weakness, though: by chance, it might hold lots of easy points or lots of hard ones, and then its score comes out too high or too low.

**k-fold cross-validation** gets around this by giving every point a turn in the validation set. With k = 5:

1. Put the points of `train.csv` and `val.csv` together, shuffle them, and divide them into 5 equal groups, called **folds**.
2. Fit a tree on folds 2 to 5 and measure it on fold 1.
3. Fit a tree on folds 1, 3, 4 and 5 and measure it on fold 2.
4. Keep going until every fold has been the validation set once.
5. Take the average of the 5 scores.

```
             fold 1   fold 2   fold 3   fold 4   fold 5
  round 1:   [val]    train    train    train    train
  round 2:   train    [val]    train    train    train
  round 3:   train    train    [val]    train    train
  round 4:   train    train    train    [val]    train
  round 5:   train    train    train    train    [val]
```

The average is more reliable than the score of a single validation set. The **standard deviation** of the 5 scores shows how much they differ from each other, in other words, how much the score depends on luck. And the test set? It isn't used at all.

In `src/evaluation.py`, `k_fold` makes the folds, and `cross_validate` runs the rounds and combines the scores.

> ❓ **Question F2.** With 5-fold cross-validation, how many trees are fitted to score a single combination of hyperparameters?


## Grid search

To compare hyperparameters, we pick a few values for each one and try every combination. This is called a **grid search**. For example, 2 criteria and 6 depths give 2 × 6 = 12 combinations, and with 5-fold cross-validation, each combination gets 5 scores.

In `src/evaluation.py`, `grid_search` scores every combination on one fold. Here's a trick, though: it doesn't fit a separate tree for every depth. Fitting is the slow part, and we want to compare trees of many depths. So instead, it fits one full tree per criterion and imitates the smaller trees when it predicts. `predict` can stop walking at a given depth (its `max_depth` argument) and return the prediction of the node it stopped at. Every node stores the most common class among its training points, so every node can act as a leaf. This is the stopping rule you found in `src/tree.py` back in Task D.

`scripts/cv_gridsearch.py` runs the whole search and prints the results.

> ❓ **Question F3.** Thanks to this trick, how many trees does the search with 2 criteria, 6 depths and 5 folds actually fit?


## Running the search

Let's run it on `moons`. This tries both criteria and the depths 1, 2, 4, 6, 8 and `None` (no limit), with 5 folds:

> ▶️ **Run.**
>
> ```bash
> make cv-moons
> ```

The output has one row per combination, sorted from best to worst. Each row shows the mean accuracy ± the standard deviation, plus `depth`, the average number of questions asked per prediction. Below the table are the scores on each fold and the confusion matrix of the best combination.

Have a look at the top few rows. Their differences are much smaller than their standard deviations, so they're more or less tied, and with a different seed, the order might well change. That's normal. We still go with the top row, but it's good to know how close the race was.

> ❓ **Question F4.** Which criterion does the best combination use?

> ❓ **Question F5.** Which maximum depth does the best combination use?


## Testing the final tree

After the search, three steps are left:

1. Pick the combination with the highest mean validation accuracy. You just did that.
2. Fit a final tree with these hyperparameters on all of `train.csv` and `val.csv`.
3. Measure this tree on the test set, once.

`scripts/final_test.py` does steps 2 and 3 for you.

> ▶️ **Run.** Replace `<criterion>` and `<depth>` with your answers to F4 and F5:
>
> ```bash
> uv run python scripts/final_test.py moons --criterion <criterion> --max-depth <depth>
> ```

> ❓ **Question F6.** What is the test accuracy of your final tree? Copy it as it's printed.

Compare it with the mean validation accuracy of the best combination. They should be pretty close, which is a good sign: the cross-validation score was an honest estimate.

The test score is your final result. Don't go back and change the hyperparameters because of it. If you did, the test set would turn into a second validation set, and its score would no longer be honest.


## Submitting

> ▶️ **Run.** Create `submission.json`, then upload it on the course website:
>
> ```bash
> make submit
> ```

> 💾 **Commit.** Save your answers to Task F:
>
> ```bash
> git add worksheet.py
> git commit -m "Answer task F"
> ```

One more to go: on to Task G!
