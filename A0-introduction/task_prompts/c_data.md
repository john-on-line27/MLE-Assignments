# Task C — Data

The first step of the pipeline is the data. In this task, you'll create the datasets, split them into parts for fitting and evaluating, and plot them.


## Synthetic data

**Synthetic** data is made by a program instead of being measured in the real world. It's small, quick to make, and we know exactly what shape it has, which makes it great for learning.

Our datasets come from the `make_*` functions in `src/data.py`. Each function returns `X` and `y`:

- `X` is a list of points. Each point is a list of two numbers, its features `x1` and `x2`.
- `y` is a list of labels, `0` or `1`, one for each point.

There are five datasets:

| Name | Function | Shape |
| --- | --- | --- |
| `moons` | `make_moons` | Two half circles that hook into each other. |
| `circles` | `make_circles` | A small ring inside a large ring. |
| `xor` | `make_xor` | Four squares. Opposite squares have the same class. |
| `checkerboard` | `make_checkerboard` | A 4 × 4 checkerboard. |
| `linear` | `make_linear` | Two halves, divided by a diagonal line. |

Each function also adds **noise**: it moves every point by a small random amount. That way the classes aren't perfectly clean, just like in real data.


## Training, validation and test sets

A model can **memorize** the points it was fitted on. It then looks perfect on those points, but falls apart on new ones. What we really want is a model that works on new points, so we always measure it on points it hasn't seen.

That's why we split the data into three parts before we fit anything, and save each part to its own file:

```text
├─────────────── train.csv ────────────────┼── val.csv ───┼── test.csv ──┤
                    60%                          20%            20%
```

- **Training set.** We fit the model on these points.
- **Validation set.** We measure the model on these points while we develop it, for example to compare a shallow tree with a deep one.
- **Test set.** We use these points only once, at the very end, after we've chosen the final model. Its score tells us how good the model really is.

Why not just compare models on the test set? Every time we pick a model because it scores well on some points, our choices fit those points a little more closely. After many such choices, a good score on those points doesn't mean much anymore. This is called **overfitting** to those points. If we only touch the test set once, at the end, its score stays honest. Think of it like studying for an exam: practicing with old exam questions (the validation set) is useful, but the real exam (the test set) only tells you what you know if you haven't seen it before.

In this repository:

- `scripts/create_datasets.py` makes each dataset, shuffles the points, and splits them: 60% go to `data/<name>/train.csv`, 20% to `val.csv`, and 20% to `test.csv`.
- `scripts/fit_tree.py` (Task D) fits the model on `train.csv`, and the plots in Task E measure it on `val.csv`.


## Why we save the datasets

We could make new points every time we need them. Instead, we make them once and save them, so that everyone uses the same points every time:

- Two models can only be compared fairly if they're measured on the same points.
- The test set has to stay the same, and it must never be used for fitting.
- You, or someone else, can repeat an experiment later and get the same result.

The random parts of the code use a **seed**. A seed is a number that fixes the random choices: the same seed always gives the same "random" numbers. The default seed is `SEED` in `src/config.py`.

Since the code and the seed can create the datasets again at any time, `data/` is listed in `.gitignore`, and you don't commit it. The same goes for `results/`.


## Take a look around

Time to open some code. You don't need to understand every line, just keep your eyes open.

Start with `src/config.py`. This is where the project keeps the settings that every other file shares, including the default seed.

> ❓ **Question C1.** What is the default seed?
>
> Answer in `worksheet.py` as `c1_default_seed` (an `int`).

> ❓ **Question C2.** Look through the rest of `src/config.py`. Is there another seed in there?
>
> Pick one of the options in `worksheet.py` and answer as `c2_other_seed`.

Next, open `src/data.py`. The functions that make our datasets, `make_moons`, `make_circles` and so on, are called **data generators**. At the end of them, the dictionary `GENERATORS` lists them all by name. That's how `scripts/create_datasets.py` finds the right one when you type `moons`.

> ❓ **Question C3.** Read through `src/data.py`. Besides the data generators, what other kind of generator can you find in it?
>
> Pick one of the options in `worksheet.py` and answer as `c3_other_generator`.

`src/data.py` is divided into **sections** to keep things organized. Each section starts with a line of dashes and a short title, like this:

```python
# -----------------------------------------------------------------------------
# toy datasets
```

> ❓ **Question C4.** Find the last section of `src/data.py`. What is the name of the function just above it?
>
> Answer in `worksheet.py` as `c4_function_name` (a `str`).


## Making the data

Now let's actually make the datasets. This creates all five of them, and splits and saves each one:

> ▶️ **Run.**
>
> ```bash
> make data
> ```

Have a look in `data/`. There's one folder per dataset, each with a `train.csv`, a `val.csv` and a `test.csv`. Open `data/moons/train.csv` in your editor: each row is one point, with `x1`, `x2`, and then the label `y`.

Rows of numbers are hard to picture, so let's draw them:

> 📊 **Plot.** Draw all datasets, then open `results/figures/datasets.png`:
>
> ```bash
> make plot-data
> ```

Each panel shows one dataset. The shape of each marker shows its split (the legend tells you which is which), and the color shows its class. Can you spot the shapes from the table at the top of this task?


## Submitting

> ▶️ **Run.** Create `submission.json`, then upload it on the course website, just like in Task A:
>
> ```bash
> make submit
> ```

> 💾 **Commit.** Save your answers to Task C:
>
> ```bash
> git add worksheet.py
> git commit -m "Answer task C"
> ```

On to Task D!
