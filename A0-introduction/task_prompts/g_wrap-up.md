# Task G — Wrap-up

You made it! You've been through a whole machine learning experiment: data, fitting, evaluation and development. This last task looks back over the whole assignment, with a short quiz that includes Git.


## Check yourself

By now, you should be able to:

- explain the pipeline: fitting a model to data to improve a metric, and why we split the data into training, validation and test sets (Tasks B and C),
- set up the environment with `uv`, run commands with `make`, and say what the pre-commit checks do (Task A),
- find the data, the model, the fitting, the evaluation, the logging, the experiment scripts and the plotting scripts in this repository, and say what each one is for (Tasks B to E),
- say what `pyproject.toml`, `uv.lock`, `README.md`, `.gitignore` and `AGENTS.md` are for (Task A),
- use `git init`, `git add` and `git commit` (all tasks).

If one of these still feels shaky, go back to the task that covers it. There's no rush.


## A short quiz

> ❓ **Question G1.** Which file makes sure everyone installs exactly the same version of every package?

> ❓ **Question G2.** Which part of the data do you use to compare versions of a model, for example trees of different depths?

> ❓ **Question G3.** Why are `data/` and `results/` listed in `.gitignore`?

> ❓ **Question G4.** What does `git add` do?

> ❓ **Question G5.** What happens when a pre-commit check fails?


## Your Git history

Finally, let's look back at everything you've saved:

> ▶️ **Run.**
>
> ```bash
> git log --oneline
> ```

Each line is one commit: a short ID and its message. You should see your first commit, "Start assignment 0", and at least one commit for each task. Read only the messages. Could someone else tell from them what you did in each commit?


## Submitting

> ▶️ **Run.** Create `submission.json`, then upload it on the course website:
>
> ```bash
> make submit
> ```

> 💾 **Commit.** Save your answers to Task G:
>
> ```bash
> git add worksheet.py
> git commit -m "Answer task G"
> ```

And that's Assignment 0 done. Well done, and see you in Assignment 1!
