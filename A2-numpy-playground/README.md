# Assignment 2: _NumPy Playground_

Almost every piece of ML code you'll read in this course pushes arrays around: batches of images, rows of features, tables of probabilities. This playground is about understanding what that code does. You'll mostly *read* NumPy code: predict the shape or the values it produces, work out whether two arrays share memory, and find the one line that's quietly wrong. You'll only write a few short functions yourself.

Each file is one puzzle, and each puzzle starts with a short explanation of the idea it's about. Read that first. The puzzles build on each other, so solve them in order, from `a_arrays_and_dtypes.py` to `j_numpy_to_torch.py`. Puzzle i puts everything together in a small neural network, which is a good warm-up for next week, and j shows how it all carries over to PyTorch.

Puzzles ask you to do four kinds of things:

- **Questions:** set an answer variable, like `SHAPES = {"A[0]": (5, 7), ...}`. You're allowed to run code to check yourself, and you should: the Python shell is the best way to build intuition for arrays.
- **Find the bug:** a function looks finished but has exactly one bug. Fix it with the smallest change you can.
- **Write a function:** in puzzle e, a few functions of a line or two are yours to write. You can type the code, or spell it out to your AI agent, which writes down exactly the code you described.
- **🎙️ Transcription:** in puzzles d and h, you dictate a function to your AI agent in plain English and it writes down exactly what you said. The puzzle explains how this works.

Many problems in puzzle e come with a picture. Run `uv run python e_reshape_and_transpose.py rotate_clockwise` (or another problem's name) to open a window with the input, what your code makes, and the target.

Be sure to run `make install` to set up the virtual environment. Running `make` alone shows all the commands. The ones you'll use most:

```
make submit-a     # grade puzzle a and write submission.json (any letter works)
make submit-all   # grade every puzzle
```

Upload `submission.json` to the course website. It tells you which answers and bugs are still wrong, without giving the answers away. Running a puzzle file (`uv run python a_arrays_and_dtypes.py`) also prints what its functions return next to what they should return.

Be sure to use `git`, and to submit your results **EARLY** and **OFTEN**! :D

If a commit fails because a hook changed some files ("files were modified by this hook"), nothing is broken: the hook only reformatted them. Run `git add -A` and commit again.

## Core parts

Parts marked ⭐ CORE are the bare minimum. Do every question if you can, but if you can't, do the core parts. Together they cover the NumPy and PyTorch concepts from the third lecture, and you can work through them in order without solving anything else first. On the course website, their checks are marked ⭐ too.

| Puzzle | ⭐ CORE |
| --- | --- |
| `a_arrays_and_dtypes.py` | Q1c, Q1e, Q2a, Q2f, Q2j, the bug in `brighten` |
| `b_indexing.py` | Q1, the bugs in `cross_entropy` and `prune_weights` |
| `c_views_and_copies.py` | Q1b, the bugs in `iterate_minibatches` and `sgd_step` |
| `d_memory_layout.py` | Q1d, Q2a, Q2b, `c_order_strides` |
| `e_reshape_and_transpose.py` | Q1f, `rotate_clockwise`, Q2a |
| `f_broadcasting.py` | Q1a, the bug in `mse` |
| `g_reductions.py` | Q2a, Q2b, the bug in `softmax` |
| `h_matmul.py` | Q1a, `matmul_by_broadcasting`, the bug in `attention_scores` |
| `i_forward_pass.py` | the bugs in `shuffle`, `standardize` and `hidden_layer` |
| `j_numpy_to_torch.py` | Q2, Q3a, the bug in `linear_from_numpy` |

## AI assistants

The repository comes with instructions for AI assistants, so they tutor you instead of solving the puzzles for you. Until you run `make install`, `AGENTS.md` is only a placeholder that tells your assistant to send you here. Pick the version that fits how you use AI:

- **KISSKI, the university AI service:** `make install` sets up the KISSKI version of `AGENTS.md`. It keeps the number of requests low, and tells you how to make yours last.
- **Your own coding agent** (Claude Code, Cursor, Copilot, …): after `make install`, run `make agent-coding` for the coding agent version.
- **A chat in the browser:** after `make install`, run `make chat-bundle` and upload `chat-bundle.md` at the start of the chat. It holds the instructions and every puzzle file. Run it again before a new chat, so it includes your latest work: the chat only sees the files as they were when you built the bundle.

To switch back to the KISSKI version, run `make agent-kisski`. After switching, start a new chat.
