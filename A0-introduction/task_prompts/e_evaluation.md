# Task E — Evaluation

The third step of the pipeline is evaluation: finding out how good the model actually is. In this task, you'll draw what the trees do, look at the kinds of mistakes a classifier can make, and see how the depth of a tree changes its results. At the end, you'll use all of that to pick a depth.

Everything in this task measures the trees on the validation set, `val.csv`. The test set stays locked away until the very end, which in this assignment is Task F (Extra).


## Plotting scripts

The scripts in `scripts/plotting/` draw figures. Each one loads saved data and saved trees, draws a figure, and saves it to `results/figures/`. If you leave out the `--save` option, a script opens the figure in a window instead.

We keep the plotting code apart from the code in `src/` and the experiment scripts in `scripts/`, for a few reasons:

- Figures are for people. They don't change any result, so the rest of the pipeline doesn't need them.
- You can change a figure (its colors, size or labels) and draw it again without fitting anything again.
- Each script does one thing, so it stays short and easy to read.


## Running steps together

A Makefile target can list other targets after its colon, and `make` runs those first, in order. That way, one target can run a whole stretch of the pipeline:

```make
boundaries: data fit plot-boundaries
```

`make boundaries` creates the datasets, fits the trees, and then draws their decision boundaries, all in one go. If you're curious, open the `Makefile` and find the three targets it runs.


## Decision boundaries

A **decision boundary** is the border between the area where a model predicts one class and the area where it predicts the other. Each question in a tree compares one feature with a number, so it cuts the plane with a straight vertical or horizontal line. That's why the decision boundary of a tree is always made of vertical and horizontal pieces, a bit like stairs.

Let's see what that looks like:

> 📊 **Plot.** Make the data, fit the trees, and draw their boundaries, then open `results/figures/boundaries.png`:
>
> ```bash
> make boundaries
> ```

You get a grid of panels: one column per dataset, and one row per depth. Each panel colors the plane by the tree's prediction, draws the validation points on top, and shows the accuracy in its title. Take a moment to compare the columns. Some datasets are already in good shape after a question or two, while others need many more. And at the largest depths, keep an eye out for spots where the boundary bends around a single point.

> ❓ **Question E1.** Which dataset needs the deepest tree to reach about 90% accuracy?

> ❓ **Question E2.** The `linear` dataset is split by a single straight line, yet a tree needs quite a few questions to get it right. Why?


## Kinds of mistakes

With two classes, we often call class `1` **positive** and class `0` **negative**. Think of a medical test, where positive means "has the disease". A classifier can be right in two ways and wrong in two ways:

|                  | Predicted 0         | Predicted 1         |
| ---------------- | ------------------- | ------------------- |
| **True class 0** | true negative (TN)  | false positive (FP) |
| **True class 1** | false negative (FN) | true positive (TP)  |

This table of counts is called the **confusion matrix**. The two kinds of mistakes have names of their own:

- A **Type I error** is a false positive. The model says positive, but the true class is negative: a healthy person is told they're sick.
- A **Type II error** is a false negative. The model says negative, but the true class is positive: a sick person is told they're healthy.

Accuracy counts both kinds of mistakes the same:

```
accuracy = (TP + TN) / (TP + TN + FP + FN)
```

In many real problems, though, one kind of mistake is worse than the other. For a disease test, a Type II error is usually worse, since a sick person goes home without treatment. For a spam filter, it's the other way around: a Type I error moves a real email to the spam folder, which is worse than letting one spam email through.

In this repository, `confusion_matrix` in `src/evaluation.py` counts the matrix, and `scripts/plotting/plot_confusion_matrix.py` draws it.

> 📊 **Plot.** Draw the confusion matrix of the full `moons` tree, then open `results/figures/confusion_moons.png`:
>
> ```bash
> make plot-confusion-moons
> ```

> ❓ **Question E3.** How many false positives does the `moons` tree make on the validation set?

> ❓ **Question E4.** A smoke alarm goes off because you burned your toast. Which kind of error is that?


## Underfitting and overfitting

A tree that's too shallow can't follow the shape of the data. It makes lots of mistakes, on the training points and on new points alike. This is called **underfitting**. We say the model has high **bias**: it's too simple, so it keeps making the same mistakes.

A tree that's too deep follows every training point, noise included. It's perfect on the training points but worse on new ones. This is called **overfitting**. You met this word in Task C, and it's the same idea: fitting too closely to one particular set of points. We say the model has high **variance**: change the training points a little, and you'd get a very different tree.

Somewhere between the two is the depth that works best on new points. Finding it means trading bias against variance, which is why this is called the **bias-variance trade-off**.

`scripts/plotting/plot_depth_accuracy.py` lets you see this trade-off. It draws the training accuracy and the validation accuracy of one tree at each depth.

> 📊 **Plot.** Draw accuracy against depth for the `moons` tree, then open `results/figures/depth_accuracy_moons.png`:
>
> ```bash
> make plot-depth-moons
> ```

The training accuracy keeps climbing until it hits 1.0. The validation accuracy is more interesting: follow it and see where it stops rising.

> ❓ **Question E5.** At the largest depths, the training accuracy is perfect, but the validation accuracy is lower than its best. What is happening there?


## Picking a depth

Now you have everything you need to choose a depth. The recipe is simple: take the depth with the highest validation accuracy. That's exactly what the validation set is for. We use it to compare versions of the model, so that the test set stays untouched for the final, honest score.

> ❓ **Question E6.** Look at your plot of accuracy against depth again. At which depth is the validation accuracy of the `moons` tree highest?

One validation set of 200 points can be lucky or unlucky, though. If you'd like to see how to pick a depth more carefully, and how to test the tree you pick, that's what Task F is about.


## Submitting

> ▶️ **Run.** Create `submission.json`, then upload it on the course website:
>
> ```bash
> make submit
> ```

> 💾 **Commit.** Save your answers to Task E:
>
> ```bash
> git add worksheet.py
> git commit -m "Answer task E"
> ```

On to Task F!
