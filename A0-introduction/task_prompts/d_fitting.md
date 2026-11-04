# Task D — Fitting

The second step of the pipeline is fitting the model. In this task you learn how a decision tree works, how the project fits one, and how it keeps a record of every tree it fits.

**A very important note on terminology:** "Fitting" is the more general term, and a bit of a holdover from a time when the ML field wasn't overrun with neural networks. After this assignment, we'll use the more specific term for fitting neural network models: "training". You can't train a tree, but you can fit a network. The names "training set" and "training accuracy" stick around for every kind of model, though, which is why you see them in this assignment too.

A quick word on where trees stand in ML today. A single decision tree is rarely the best model on its own. Combine hundreds of them, though, and you get **random forests** and **gradient-boosted trees** (libraries such as XGBoost and LightGBM), which are still among the strongest methods for tabular data, the kind of data that fits in a spreadsheet. There, they often beat neural networks. Unfortunately, trees won't come up again in this course. We chose them here because they're easy to explain and map well onto concepts you already know.


## Decision trees

A decision tree is, well, a tree, like the data structure, and predicts a class by asking yes/no questions about the features. Each question looks at one feature and compares it with a number, for example "is `x1 <= 0.37`?". The answer sends the point left (yes) or right (no) to the next question. At the end, the point reaches a **leaf**, which holds the prediction.

```
               x1 <= 0.37 ?
               /          \
            yes            no
            /                \
      x2 <= 0.5 ?          predict 1
       /       \
     yes        no
     /            \
 predict 0     predict 1
```

Take the point `[0.2, 0.8]`. Its `x1` is 0.2, which is at most 0.37, so it goes left. Its `x2` is 0.8, which is more than 0.5, so it goes right. It reaches a leaf and gets the prediction `1`.

Each question is a **node**. The first one is the **root**. The **depth** of a tree is the largest number of questions a point can be asked on its way from the root to a leaf. The tree above has depth 2.


## Fitting a tree to data

To fit a tree, we choose its questions. We build the tree from the top down:

1. Start with all training points at the root.
2. Try every feature and every useful threshold. Pick the pair that separates the classes best: after the split, each side should be more homogeneous than it was before.
3. Send each point left or right by its answer.
4. Repeat steps 2 and 3 on each side.
5. Stop when a side holds only one class, or when the tree has reached its maximum depth, among other possible conditions. That side becomes a leaf. It predicts the most common class among its points.

The tree needs a way to measure how mixed the classes on a side are. This project has two: **Gini impurity** and **entropy**. Both are 0 when all points on a side have the same class, and larger when the classes are mixed. Which one the tree uses is its **criterion**, `"gini"` or `"entropy"`.

In `src/tree.py`, `DecisionTree.fit` starts the fitting. `DecisionTree._grow` handles one node and its children, and calls `best_split` to find the best question. `DecisionTree.predict` walks points down the fitted tree.

**Note.** Methods whose names start with `_`, like `DecisionTree._grow`, are meant to be used only inside the class: they're **private** methods. Unlike Java, Python has no formal way to make a method public or private, so this is only true by convention.

**Extra.** For a list of labels `S`, let `p_c` be the fraction of labels in `S` with class `c`. Then:

```
gini(S)    = 1 - (sum over all classes c of p_c^2)
entropy(S) = -(sum over all classes c of p_c * log2(p_c))
```

`best_split` picks the question that lowers the impurity the most. The two sides are weighted by their size. This drop in impurity is the **information gain**, computed by `information_gain`.


You can see all of the code for the tree in `src/tree.py`. If you look at it for a bit, you'll notice something that contradicts what we said above about how trees are fitted. Step 5 says the tree stops growing when it reaches its maximum depth, but have a look at `DecisionTree.__init__` and `DecisionTree._grow`: there's no maximum depth anywhere. Our trees always grow until every leaf holds one class. So where did the maximum depth go?

> ❓ **Question D1.** The maximum depth, together with `min_samples_split`, the smallest number of points a node needs before it may be split, turns up as an argument of two public methods of `DecisionTree`. Their names start the same way. Give the part they share.

So our trees stop early when they *predict*, not when they're fitted. That's allowed because each split only depends on the points that reach its node, never on what happens further down. A tree fitted with a maximum depth of 3 is therefore exactly the full tree cut off at depth 3, so one full tree can stand in for trees of every depth. This saves us from fitting the same tree again and again in our experiments in Task F.

**Note.** Most libraries, such as scikit-learn, take settings like `max_depth` and `min_samples_split` when the tree is created, so don't be surprised to find them there later. We moved them to `predict` for the reason above.

> ❓ **Question D2.** While you're in `src/tree.py`: how many lines tall is the tree?


## The fitting script

`scripts/fit_tree.py` fits one tree per dataset:

1. It loads `data/<name>/train.csv`.
2. It fits the tree on these points. The validation and test points stay untouched.
3. It fits the tree in a way so that the tree grows until every leaf holds one class.
4. It saves the tree to `results/models/<name>_<criterion>.json`.

> ❓ **Question D3.** What sort of font can you find in `scripts/fit_tree.py`?

**Extra.** A bit of context on scripts in practice.

A script like this one describes one job, such as fitting or evaluating a model, and its command-line arguments let you adjust that job without touching the code. That makes the command line a handy common interface. On the computer clusters that research labs (like ours, the ML Group) and companies use, you describe a job with exactly such a command, and the cluster runs it for you, usually to train models far bigger than anything in this course.

The layout of `fit_tree.py` is very common, too. The functions near the top do the actual work, and `main` at the bottom does little more than read the command-line arguments. It reads them with `argparse`, which is clunky but easy to read. There are more elegant libraries for this, but `argparse` is built into Python and has been around for a long time, so it's still what you'll find in most research code, although that's slowly changing.


## Logging

**Logging** means keeping a record of what you ran and what came out. In this project, the most important records are the fitted trees:

- `model_path` in `src/config.py` decides where a tree is saved: `results/models/<dataset>_<criterion>.json`.
- `save_tree` in `src/tree.py` writes the tree to that file, together with the settings it was fitted with.
- `load_tree` in `src/tree.py` reads the file back into a tree that can predict.

The reasons for this design:

- **Fit once, use many times.** Fitting is the slow step. Every later script loads the saved tree instead of fitting it again.
- **The file name says what is inside.** The name is built from the dataset and the criterion, so every script can find the right tree. Only `src/config.py` decides where files go, so the paths are the same everywhere.
- **The settings stay with the tree.** The file stores the settings next to the tree, so you always know how a tree was made.
- **Plain text.** JSON is a text format. You can open the file and read the tree.
- **Not in Git.** `results/` is listed in `.gitignore`. Everything in it can be created again from the code, the data, and the seed.


## Fitting the trees

Time to fit some trees. This fits one tree on each dataset, with the Gini criterion:

> ▶️ **Run.**
>
> ```bash
> make fit
> ```

Now open `results/models/moons_gini.json` in your editor. The first node under `"root"` is the root of the tree. Its `split` is its question, and `n_samples` is the number of training points that reached it.

> ❓ **Question D4.** How many training points reached the root?

> ❓ **Question D5.** Which feature does the root's question look at? Give the number stored under `feature`.


## Submitting

> ▶️ **Run.** Create `submission.json`, then upload it on the course website:
>
> ```bash
> make submit
> ```

> 💾 **Commit.** Save your answers to Task D:
>
> ```bash
> git add worksheet.py
> git commit -m "Answer task D"
> ```

On to Task E!

```text
 .---.                                   .---.
 |   |                                   |   |
 |   |                                   |   |
=|   |===================================|   |=
 |   |   \\                         //   |   |
 '---'    \\                       //    '---'
           \\        .---.        //
            \\    ' ( >_< ) '    //
             \\      '---'      //
              \\______| |______//
               |               |
               |               |
               '---.       .---'
                   |=======|
                   |___.___|
                   |   |   |      "Just one more
                   |   |   |       rep..."
                   |   |   |
                 __|   |   |__
                (______|______)
```
