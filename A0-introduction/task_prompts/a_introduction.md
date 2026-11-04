# Task A — Introduction

Welcome to Assignment 0!

In this assignment, we go over the general structure of an ML pipeline in a practical setting: as data and code on your own computer. Most of your time goes into reading task prompts like this one and looking at files in the repository. The main goal is to get you oriented. Along the way, you get a chance to read some code, get comfortable with your text editor or IDE again, and, most importantly, learn how the coming assignments work.

If you don't have a development environment yet, the `README.md` in the folder above this assignment lists what you need and what we recommend. Make sure `git`, `make` and `uv` are installed before you continue.


## How the assignment works

There are seven tasks, `a` to `g`. Each one has a prompt in `task_prompts/`, just like the one you're reading now. They build on each other, so work through them in order.

Most tasks come with questions, and you answer them in `worksheet.py`. Every answer is a Python variable with a fixed value, almost always a whole number, a decimal number, a string, a single letter, or a list or set of strings or numbers. Above each variable, `worksheet.py` repeats the question and says what kind of answer it expects. For multiple-choice questions, it also lists the options, and your answer is a single letter, such as `"b"`. Nothing in this assignment is graded. The questions are there to help you check that you've understood the material, and they're good practice for the exam.

Whenever you need to do something, the prompt puts it in a box. There are four kinds:

| Box             | What you do                                                                         |
| --------------- | ----------------------------------------------------------------------------------- |
| ▶️ **Run.**     | Run the commands in the box, in a terminal in the assignment folder.                |
| 📊 **Plot.**    | Run the commands to draw a figure, then open the figure and have a look at it.      |
| ❓ **Question.** | Answer the question in `worksheet.py`. The box tells you which variable to fill in. |
| 💾 **Commit.**  | Save your work with Git. More on that in [Git](#git).                               |

Everything outside the boxes is there to explain things. You only need to act when you reach a box.

Everything outside the sections marked **Extra** is the core of this assignment: the minimum we expect you to know by the end. Extra sections, and all of Task F, go a bit further. They cover things you'll see often in practice, but that aren't part of the core content of the course. Questions in Extra sections are optional too. Read them if you're curious, and skip them if you're short on time.


## The files in the root folder

Besides the folders, the assignment comes with these files:

| File                      | What it is for                                                                                                                                         |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `README.md`               | A short description of the assignment: its goals, folders and tools. Read this one first.                                                              |
| `pyproject.toml`          | Describes the Python project: its name, the Python version, and the packages it needs. It also holds the settings for tools such as `ruff` and `mypy`. |
| `uv.lock`                 | The exact version of every package, including the packages that other packages need. Thanks to this file, everyone installs exactly the same versions. |
| `Makefile`                | Short names for long commands. See [Make](#make).                                                                                                      |
| `.gitignore`              | Files and folders that Git ignores. See [Git](#git).                                                                                                   |
| `.pre-commit-config.yaml` | The checks that run before each commit. See [Pre-commit checks](#pre-commit-checks).                                                                   |
| `AGENTS.md`               | Instructions for AI assistants that help you. See [Working with AI assistants](#working-with-ai-assistants).                                           |
| `worksheet.py`            | Your answers.                                                                                                                                          |
| `submit.py`               | Turns your answers into `submission.json`.                                                                                                             |

Files whose names start with a dot are hidden. Run `ls -a` to see them too.


## The virtual environment

A Python project needs packages, for example `matplotlib` to draw plots. The problem is that different projects may need different versions of the same package. A **virtual environment** solves this: it's a folder that holds a Python interpreter and the packages for one project, so each project stays separate from the others.

We use `uv` to manage the virtual environment. The command `uv sync` reads `pyproject.toml` and `uv.lock` and installs the packages into a new folder, `.venv/`. The first run can take a few minutes.

Once the environment exists, you **activate** it before you run any code:

```bash
source .venv/bin/activate
```

This one line is very important, so remember it. After it, `python` and tools such as `ruff` and `mypy` in this terminal come from the environment, and your prompt usually starts with `(.venv)`. Activating only lasts until you close the terminal, so run it again every time you open a new terminal for this assignment. `deactivate` leaves the environment.

If you forget, Python usually tells you it can't find a package, for example `ModuleNotFoundError: No module named 'matplotlib'`. That almost always means the environment isn't active.

There's one other way: put `uv run` in front of a command, for example `uv run python submit.py`. It runs the command inside the environment, without activating it. The Makefile does this, so `make` commands work either way.


## Make

A `Makefile` gives short names to commands. Each short name is called a **target**, and below each target are the commands it runs. For example:

```make
submit:
	uv run python submit.py
```

When you run `make submit`, `make` runs `uv run python submit.py` for you.

If you want to see all targets, open `Makefile` in your editor. Each task tells you which targets to run, so you don't need to read the commands behind a target unless the task asks you to.


## Git

Git is a version control system. It saves snapshots of your project, called **commits**. With commits, you can see what changed over time and go back to an older version if something breaks.


### Telling Git who you are

Every commit records who made it, with a name and an email address. Git needs to know these before your first commit. You only set them once per computer: `--global` means they apply to every repository on it.

> ▶️ **Run.** Put in your own name and email address:
>
> ```bash
> git config --global user.name "Ada Lovelace"
> git config --global user.email "ada@example.com"
> ```

Not sure if you've done this before? `git config --global user.name` prints the name Git has, or nothing if there is none.


### The basic commands

You downloaded this assignment as a `.zip` file, so it isn't a Git repository yet. For now, we only need the most basic commands:

| Command                     | What it does                                                                                             |
| --------------------------- | -------------------------------------------------------------------------------------------------------- |
| `git init -b main`          | Turns the current folder into a Git repository, with a first branch called `main`. You only run it once. |
| `git add <file>`            | **Stages** a file: marks it to be part of the next commit. `git add .` stages every changed file.        |
| `git commit -m "<message>"` | Saves the staged files as a new commit. The message says in a few words what changed.                    |
| `git status`                | Shows which files changed and which ones are staged.                                                     |

It's a good habit to run `git status` often. It's easy to keep working, forget to commit, and suddenly find half of the repository changed or staged.

Git ignores the files listed in `.gitignore`. In this project, these are mostly files that the code can create again at any time, such as the datasets in `data/` and the results in `results/`.

If you want to know more, `../docs/git.md` goes into a bit more detail.


### When to commit

A good time to commit is whenever you finish a piece of work that makes sense on its own, for example a fixed mistake or the answers to one task. Small commits are easier to read and easier to undo than one huge commit, so don't wait until everything is finished.

The task prompts show you when to commit with a 💾 **Commit.** box. The box gives you the commands and the message to use.

You never commit the files in `data/` and `results/`. They're in `.gitignore`, so `git add` skips them anyway.


### Writing a commit message

A commit message tells others, and you in a few weeks, what changed. A good message:

- starts with a verb, as if you give an instruction: "Fix", "Add", "Answer",
- is short: about 50 characters at most,
- says what changed, not how long it took or how you feel about it.

| Helpful                        | Not helpful       |
| ------------------------------ | ----------------- |
| `Fix unused import in data.py` | `fix`             |
| `Answer task C`                | `stuff`           |
| `Start assignment 0`           | `final version 2` |


### Your first commit

Time to set everything up. `make install` does three things for you: it installs the virtual environment (`uv sync`), turns the folder into a Git repository (`git init -b main`), and installs the pre-commit checks, which the next section explains.

> ▶️ **Run.**
>
> ```bash
> make install
> ```

The environment exists now, so activate it. From here on, do this every time you open a new terminal for this assignment:

> ▶️ **Run.**
>
> ```bash
> source .venv/bin/activate
> ```

Now stage every file and make your first commit:

> 💾 **Commit.** Save the assignment as it is now:
>
> ```bash
> git add .
> git commit -m "Start assignment 0"
> ```

The commit fails, and that's on purpose. The next section explains why.


## Pre-commit checks

A **pre-commit hook** is a program that Git runs every time you commit. If it finds a problem, the commit stops. You fix the problem and then commit again, which is exactly what you're about to do.

This project uses the `pre-commit` tool to run its checks. You can find the list of checks in `.pre-commit-config.yaml`:

- `ruff` looks for common mistakes in Python code, such as a variable that is never used. A tool like this is called a **linter**.
- `ruff-format` rewrites Python code in one fixed style, so that quotes and line breaks look the same everywhere.
- `mypy` checks the **type hints** in the code. A type hint says what kind of value a variable should hold, for example `n: int`. `mypy` reports places where the values don't match the hints.
- A few smaller checks remove spaces at the end of lines, make sure every file ends with a new line, and check that `.yaml` and `.toml` files are valid.

Some checks fix the problem themselves and change your file. Others only report it. Either way, the commit stops, and you need to `git add` the files again before you commit.

So let's fix the problems. Look at the output of your failed commit: for each problem, it tells you the file, the line, and what is wrong.

Your commit failed with two complaints, both about the function `model_path` in `src/config.py`:

- `ruff` says ``F841 Local variable `path` is assigned to but never used``. The line `path = ...` makes a variable that nothing uses. Delete that line.
- `mypy` says `Incompatible return value type (got "Path", expected "str")`. The function promises to return a `str`, but it returns a `Path`. In the function header, change `-> str` to `-> Path`.

Afterwards, the function should look like this:

```python
def model_path(dataset: str, criterion: str) -> Path:
    """Where the tree grown on a dataset with a given criterion is saved."""
    return MODELS_DIR / f"{dataset}_{criterion}.json"
```

Since the first commit never happened, try again with the same message:

> 💾 **Commit.** Save the assignment, now with the fix:
>
> ```bash
> git add .
> git commit -m "Start assignment 0"
> ```

This time, all checks should pass. To make sure, ask Git for the status. It should say that there's nothing to commit:

> ▶️ **Run.**
>
> ```bash
> git status
> ```


## Working with AI assistants

You can do this assignment in three ways:

- **On your own.** Everything you need is in the task prompts.
- **With a coding agent** that runs inside the assignment folder, such as Kilo Code, Claude Code or Codex. Most coding agents read `AGENTS.md` on their own.
- **With a chat assistant** in your browser. Paste `AGENTS.md` into the chat, or attach it, before you start. It holds every file of the assignment, so the assistant knows the whole repository. It can't see your computer, though, so paste any output or error message you want it to look at.

Either way, `AGENTS.md` tells the assistant how to help you: it explains things and gives hints, but doesn't do the work for you. It also doesn't check on its own whether you've done a step. It takes your word for it and moves on. If you want it to look at something, such as your answers or a file, just ask.

> ❓ **Question A1.** `AGENTS.md` gives the assistant a name. What is it? If an assistant is guiding you through the assignment, it has probably introduced itself already. Otherwise, open `AGENTS.md` and look for the name.
>
> Answer in `worksheet.py` as `a1_agent_name` (a `str`).


## Submitting

`submit.py` reads your answers from `worksheet.py` and writes them to `submission.json`. It always takes every answer in the worksheet, so questions from later tasks show up as not correct until you get to them.

> ▶️ **Run.** Create `submission.json`:
>
> ```bash
> make submit
> ```

Then upload it: go to [py.ml.tu-berlin.de](https://py.ml.tu-berlin.de), click **Homework** at the top of the page, open **A0 — Introduction**, and drop `submission.json` there. The website shows you which answers are correct, and you can submit as often as you like.

Last step: save your answer.

> 💾 **Commit.** Save your answers to Task A:
>
> ```bash
> git add worksheet.py
> git commit -m "Answer task A"
> ```

That's it for Task A. Off to Task B! :D

```text
    _/\_                     .   *   .  .   *   .                     _/\_
   ( o  )                    .-~~~~~~~~~~~~~~~~-.                    (  o )
   (   3)===========<  ) ) ) (     HUZZAH!!     ) ( ( (  >===========(E   )
   _\__/_  |\/\/\/\/\|       '-~~~~~~~~~~~~~~~~-'       |/\/\/\/\/|  _\__/_
  / |##| \ | TASK A  |                                  | TASK A  | / |##| \
 /  |##|  \|  DONE!  |                                  |  DONE!  |/  |##|  \
    |##|    \  / \  /                                    \  / \  /    |##|
    /  \     \/   \/                                      \/   \/     /  \
   /____\                                                            /____\
```
