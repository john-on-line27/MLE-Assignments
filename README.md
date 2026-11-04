# MLE Assignments

Welcome to MLE!!! :D

I would hope that you all are excited to learn some practical machine learning. We're certainly excited to teach it.

This folder is the home for your assignments. Each week you download a new assignment as a `.zip` file and unpack it here. Every assignment is a complete repository of its own: it has its own virtual environment, its own `Makefile`, its own Git repository, and its own `README.md`. This README covers what all of them have in common: the tools you need, how to work with AI assistants, and how to check your work. Short guides to the tools live in [`docs/`](docs/).


## The Assignments

| Week | Lecture | Assignment |
|---|---|---|
| 1 | ML Project | A0 — Introduction |
| 2 | Engineering/Python Basics | A1 — Python Playground |
| 3 | Acceleration Frameworks | A2 — NumPy Playground |
| 4 | Deep Learning Basics | A3 — Neural Networks in NumPy |
| 5 | Autograd and Backpropagation | A4 — CNNs in PyTorch |
| 6 | Autoregressive Language Models | A5 — ♪ ¯\\\_(ツ)\_/¯ ♫ |
| 7 | Transformers | A6 — ˖✧ ¯\\\_(◕‿◕)\_/¯ ✧˖ |
| 8 | GPU Computing | A7 — ⋆｡˚ ¯\\\_(ᵔᴥᵔ)\_/¯ ˚｡⋆ |
| 9 | GPU Compilation | A8 — ✦･ﾟ✧ ¯\\\_(☆▽☆)\_/¯ ✧ﾟ･✦ |

The later assignments are still in the works. Stay tuned!

There are two kinds of assignment:

- **Playgrounds** are a series of small Python files, `a_*.py`, `b_*.py`, …, each with a puzzle or two to solve. They get harder as the letter goes up.
- **Experiments** look like the repository of a small ML research experiment. You work through the task prompts in `task_prompts/` in order, and run, read, and fill in parts of the code along the way.

Everything in this course runs on an ordinary laptop. You don't need a GPU.


## Installation and Environment

### General Environment

This course expects that you work in a unix-like environment. If you're running macOS or some version of Linux, you're already there. If you're running Windows, install the most recent Windows Subsystem for Linux (WSL). You can find instructions here:

- https://learn.microsoft.com/en-us/windows/wsl/about

Further, this course assumes basic familiarity with shell commands (`cd`, `ls`, `rm`, etc.). If you're not familiar with these, there are plenty of cheat sheets and simple tutorials online.

### IDE

This course does not assume a particular IDE. Use whatever you're comfortable with. Personally, I like Neovim and VS Code. If you don't have an editor yet, [`docs/setup.md`](docs/setup.md) has our recommendations.

### `git`

We will be using `git` in this course. Make sure it is installed on your computer. For Windows users, it should be installed on WSL. Do this before installing `uv`. Instructions for installing `git` are found here:

- https://git-scm.com/install/

New to Git, or want a refresher? [`docs/git.md`](docs/git.md) walks you through the basics.

### `make`

`make` is a build automation tool that lets you define and run common commands through simple shortcuts. We'll be using it throughout the course, so make sure it's installed. It almost certainly already is on macOS and Linux, and Windows users should have it available on WSL as well.

### `uv`

`uv` is a fast Python package manager that we use to manage each assignment's virtual environment and dependencies. Think of it as a modern, much speedier replacement for `pip` + `venv`. You can find installation instructions here:

- https://docs.astral.sh/uv/getting-started/installation

Windows users should install it on WSL. You'll almost never have to deal with `uv` directly. When you start an assignment, `make install` sets up its virtual environment for you. Assignment 0 explains all of this in more detail.

> **Activate the environment in every new terminal.** To run anything in an assignment's virtual environment, you have two options:
>
> - put `uv run` in front of every command, for example `uv run python submit.py`, or
> - activate the environment with `source .venv/bin/activate` from the assignment's folder. After that, `python`, `pytest` and the other tools in this terminal come from the environment, and you can leave out `uv run`.
>
> Activating only lasts as long as the terminal session. Unless you want to write `uv run` in front of everything, you have to run `source .venv/bin/activate` again every time you open a new terminal, and whenever you switch to a different assignment. `deactivate` leaves the environment. The `make` commands already use `uv run`, so they work either way.


## A Note on AI Assistants

> ### ⚠️ Using an AI agent is not required to complete these assignments.
>
> You can finish every assignment in a reasonable amount of time on your own. An agent just guides you through it.

This course encourages you to use coding agents and AI chatbots while you work on the assignments. At this point, it's no longer possible to deny the impact these tools have had on software engineering, and education has to adapt its methods to match.

Here's the honest situation: there is nothing in this course that a coding agent can't easily solve if you ask it to. That's fine. This is an introductory course, and it's actually kind of nice that these models know so much. But you still need to learn the story and the structure of how models are trained, which is what the code reflects. You need this foundation to understand the systems built on top of it.

So the real question is: at what level do we expect you to be able to describe these systems? With agents, describing a system has become almost the same thing as implementing it. And descriptions can be fuzzier and fuzzier: often a sentence or two is enough for a model to build something quite complex. What we want is for you to be able to describe the concepts and systems in this course in the detail using the terminology of the field.

So please use agents! To make sure you still do the work of recounting and describing these ideas yourself, every assignment comes with an `AGENTS.md` file that limits what an AI assistant will do for you: it guides you through the assignment, explains things, and gives hints, but it doesn't hand you the answers.

You can always work through an assignment with the help of a **coding agent**: an AI assistant that runs inside the assignment folder, such as Claude Code, Codex, Copilot, Cursor, or Kilo Code. It reads `AGENTS.md` on its own. Only some assignments also work with a **chat assistant**, the kind you use on a website. The assignment tells you when it does. In that case, paste `AGENTS.md` into the chat, or attach it, before you start on any problems.

Which coding agent should you use? If you already have a subscription that comes with a coding agent, it's probably best to use that one. If you don't have a coding agent yet, [`docs/setup.md`](docs/setup.md) describes the free setup we recommend: the Zed editor with the Kilo Code agent in the terminal, using KISSKI, the AI service for German universities. It's a bit more limited than a paid subscription, since KISSKI caps how many requests you can make.

Again though, it's important to note that you can finish every assignment in a reasonable amount of time without an agent. The agent just guides you through it.


## Checking Your Work

### Submitting

The primary way for you to check your work is through the course website. Go to [py.ml.tu-berlin.de](https://py.ml.tu-berlin.de), click **Homework** at the top of the page, open the assignment you're working on, and drop your `submission.json` file there. The website shows you what's correct and what isn't.

You create `submission.json` with `submit.py` in the assignment's folder. The `Makefile` has a shortcut for it: `make submit` creates a submission with every answer you've given so far.

Feel free to submit often. There is no limit to the number of times you can submit. The feedback shows you where your code and answers work and where they don't, and will hopefully help you find your mistakes. This system was deliberately designed to help you. So please **SUBMIT EARLY AND OFTEN**.

### Questions

Some things we can't check by running code. For those, the task prompts ask you questions, and you write your answers into `worksheet.py`. They're submitted together with everything else in `submission.json`. The questions are there to help you check that you've understood the material, and they're good practice for the exam.

### Tests

Some assignments come with unit tests in `pytest`. These are deliberately incomplete: they're smoke tests and hints, not the real grading. Look at the test names and comments to get a sense of the cases your code will likely run into. Feel free to fill them out further, particularly if the feedback from submitting isn't helpful. Unit tests are a valuable tool for working through difficult problems.
