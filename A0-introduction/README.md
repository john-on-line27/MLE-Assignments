# Assignment 0 — Introduction

This assignment takes you through a small machine learning experiment from start to finish: making datasets, fitting decision trees to them, measuring how good the trees are, and picking the best settings. All the code is already written. Your job is to read the task prompts, run the commands, look at the results, and answer questions about what you see. Along the way, you set up the tools you'll use in every assignment of this course: `uv`, `make`, Git and pre-commit checks.


## Getting started

Open a terminal in this folder and run:

```bash
make install
source .venv/bin/activate
```

`make install` sets up the virtual environment in `.venv/`, turns the folder into a Git repository, and installs the pre-commit checks. You only run it once.

`source .venv/bin/activate` activates the environment. **Run it every time you open a new terminal for this assignment, before you run any code.** Without it, Python can't find the packages the assignment needs. While the environment is active, your prompt usually starts with `(.venv)`. `deactivate` leaves it. If you want to be more fine-grained, you can also prefix any command with `uv run` and it will run the command in the virtual environment.

Then open `task_prompts/a_introduction.md` and start reading. Task A explains all of the above in more detail.


## Tasks

Work through the tasks in order, since each one builds on the ones before it.

| Task | Prompt                          | What it's about                                                                 |
| ---- | ------------------------------- | ------------------------------------------------------------------------------- |
| A    | `task_prompts/a_introduction.md` | The tools: the virtual environment, `make`, Git and pre-commit checks           |
| B    | `task_prompts/b_ml-projects.md`  | What machine learning is, the steps of the pipeline, and where each one lives   |
| C    | `task_prompts/c_data.md`         | Making the datasets and splitting them into training, validation and test sets |
| D    | `task_prompts/d_fitting.md`      | How a decision tree works, and fitting and saving trees                         |
| E    | `task_prompts/e_evaluation.md`   | Decision boundaries, kinds of mistakes, and underfitting and overfitting       |
| F    | `task_prompts/f_development.md`  | Extra: cross-validation, a search for the best settings, and the final test    |
| G    | `task_prompts/g_wrap-up.md`      | A look back over the whole assignment, with a short quiz                        |

Sections marked **Extra**, and all of Task F, are optional.


## What's in this folder

| Path                | What it holds                                                          |
| ------------------- | ---------------------------------------------------------------------- |
| `task_prompts/`     | One prompt per task. This is where you spend most of your time.        |
| `src/`              | The code: settings, datasets, the decision tree, and evaluation.       |
| `scripts/`          | Scripts that each run one step of the experiment.                      |
| `scripts/plotting/` | Scripts that draw figures.                                             |
| `worksheet.py`      | Your answers to the questions in the task prompts.                     |
| `submit.py`         | Turns your answers into `submission.json`.                             |
| `Makefile`          | Short names for the commands in the task prompts.                      |
| `AGENTS.md`         | Instructions for AI assistants.                                        |
| `data/`, `results/` | Datasets, saved trees and figures. The scripts create these folders.   |


## Working with an AI assistant

You can do this assignment on your own, with a coding agent, or with a chat assistant:

- **On your own.** Everything you need is in the task prompts.
- **With a coding agent** that runs inside this folder, such as Kilo Code, Claude Code or Codex. Most coding agents read `AGENTS.md` on their own.
- **With a chat assistant** in your browser. Paste `AGENTS.md` into the chat, or attach it, before you start. It holds every file of the assignment, so the assistant knows the whole repository. It can't see your computer, though, so paste any output or error message you want it to look at.

Either way, the assistant explains things and gives hints, but doesn't do the work for you. It also doesn't check on its own whether you've done a step. If you want it to look at something, just ask.


## Answering and submitting

Each ❓ question in a task prompt has a matching variable in `worksheet.py`. Replace its `None` with your answer. To check your answers, run:

```bash
make submit
```

This writes `submission.json` with every answer in the worksheet. Upload it at [py.ml.tu-berlin.de](https://py.ml.tu-berlin.de): click **Homework** at the top of the page, open **A0 — Introduction**, and drop the file there. The website shows you which answers are correct, and you can submit as often as you like. Nothing in this assignment is graded.
