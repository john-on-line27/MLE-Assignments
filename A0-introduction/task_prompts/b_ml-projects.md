# Task B — Machine Learning Projects

In this task, you'll find out what a machine learning project is made of, and where each part lives in this repository.


## What is machine learning?

In normal programming, you write the rules yourself. In machine learning, you give the computer examples, and it works out the rules on its own. The result is called a **model**: a program that takes an input and returns a prediction.

Most machine learning projects have the same goal: **fit** a model to some data so that it scores well on some **metric**. A metric is just a number that measures how good the model is.

In this assignment:

- the **data** is synthetic 2D data: points in a plane, made by our own code,
- the **model** is a decision tree,
- the **metric** is accuracy: the fraction of points that the model labels correctly.


## Classification

Each point in our data belongs to one of two classes, `0` or `1`. The model gets the two coordinates of a point and has to predict its class. Predicting a class like this is called **classification**, and it's one of the most common tasks in machine learning.

The inputs of the model are called **features**. Each of our points has two features, `x1` and `x2`. The correct class of a point is called its **label**.

Our data has a label for every point, and the model uses these labels while it's being fitted. This is called **supervised learning**: the labels guide the model, a bit like a teacher who knows the answers.


## The pipeline

Most projects go through the same steps, over and over. Together, these steps are called the **pipeline**:

```text
┌──────┐     ┌─────┐     ┌──────────┐     ┌──────────────┐  yes  ┌──────┐
│ data │ ──► │ fit │ ──► │ evaluate │ ──► │ good enough? │ ────► │ done │
└──────┘     └─────┘     └──────────┘     └──────────────┘       └──────┘
                ▲                                 │
                │                                 │ no
                │                                 ▼
                │                       ┌──────────────────┐
                └───────────────────────┤ change the model │
                                        └──────────────────┘
```

1. **Data.** Get the data and prepare it.
2. **Fit.** Fit the model to the data. This is where the model learns from the examples.
3. **Evaluate.** Measure the metric. How good is the model on points it hasn't seen before?
4. **Repeat.** If it's not good enough yet, change something, fit again, and evaluate again.

In step 4, you usually change how the model is fitted, for example how deep the tree is allowed to grow. Sometimes you also change what you measure, for example when one kind of mistake is worse than another.

The next tasks follow the pipeline: data in Task C, fitting in Task D, and evaluation in Task E. Task E also shows you how changing the depth of a tree changes its results, which is the first round of the loop. Task F (Extra) turns this into a proper search.


## Where the pipeline lives

The repository is organized like a small research project:

| Folder | What it holds |
| --- | --- |
| `src/` | The code of the project, as functions and classes that other files import. |
| `scripts/` | Experiment scripts. Each one runs one step of the pipeline from the command line. |
| `scripts/plotting/` | Plotting scripts. Each one draws a figure from saved data and models. |
| `data/` | The datasets. A script creates them. |
| `results/` | Everything the experiments create: saved models in `results/models/` and figures in `results/figures/`. |
| `task_prompts/` | The task prompts, including this one. |

Don't worry if you can't find `data/` and `results/` yet. They appear when you run the first scripts in Task C.

Each step of the pipeline has its code in `src/` and a script that runs it:

| Step | Code | Script |
| --- | --- | --- |
| Data | `src/data.py` | `scripts/create_datasets.py` |
| Model and fit | `src/tree.py` | `scripts/fit_tree.py` |
| Evaluate | `src/evaluation.py` | `scripts/plotting/` |
| Repeat (Extra) | `src/evaluation.py` | `scripts/cv_gridsearch.py` |

On top of that, `src/config.py` holds the settings that the whole project shares: where files are saved, and the default random seed.

Have a quick look around. Open the folders in your editor, or list them in the terminal:

> ▶️ **Run.**
>
> ```bash
> ls src scripts scripts/plotting
> ```


## Supporting parts

Around the pipeline are a few parts that don't fit or evaluate anything themselves. They make the work easier, and they make the results easier to trust.

**Experiment scripts.** The files in `scripts/` are experiment scripts. Each one does one step, takes its settings as command-line options, and saves its output to a file. Since all the settings are in the command, you can run the same experiment again later and get the same result. The `Makefile` stores these commands under short names, so you don't have to type them out.

**Logging.** Over a project, you fit and evaluate a lot of models. Later on, you need to know which model came from which data and which settings. Keeping this record is called **logging**. In this project, `src/config.py` decides where each model is saved, and `save_tree` in `src/tree.py` writes the model and its settings to `results/models/`. Task D looks at this in more detail.

**Plotting scripts.** The files in `scripts/plotting/` turn saved data and models into figures. Figures help people see what a model actually does. You'll use them in Task E.


On to Task C!

```text
  "Away we go!"
         \       \o/
                  |
                 / \
              _____________        _____________        _____________
             |_____________|      |_____________|      |_____________|
               |  DATA   |          |   FIT   |          |EVALUATE |
               |         |          |         |          |         |
  #############|         |##########|         |##########|         |#######
  #############|         |__________|         |__________|         |#######
  #############|___________________________________________________|#######
  ##########################################################################
```
