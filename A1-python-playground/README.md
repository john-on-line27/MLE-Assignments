# Assignment 1: _Python Playground_

This assignment provides you all with the opportunity to become familiar with Python and become familiar with some ideas from ML along the way.

Each file, or puzzle, contains functions for you all to fill out. Each puzzle stands on its own, so you can work on them in any order.

The puzzles increase in difficulty as you go higher in the alphabetic index. So `a_foobar.py` is the easiest and `j_context_managers.py` is the most difficult. It should be noted that you don't have to be able to answer _all_ of these questions to do well in the rest of this course, but you should be able to do most of them with a good bit of thought and effort.

Be sure to run `make install` to instantiate the virtual environment and set up the AI tutor. Running `make` alone will display the help message, which lists all of the commands in the Makefile.

Be sure to use `git`, and to submit your results **EARLY** and **OFTEN**! :D To submit, run `make submit-a` (or the letter of another puzzle; `make submit-all` grades every puzzle). It writes `submission.json`, which you upload to the course website.

## Core parts

Parts marked ⭐ CORE are the bare minimum. Do every question if you can, but if you can't, do the core parts. Together they cover the Python concepts from the second lecture, and you can work through them in order without solving anything else first.

| Puzzle | ⭐ CORE |
| --- | --- |
| `a_foobar.py`, `b_word_frequency.py`, `c_basic_math.py` | none |
| `d_running_stats.py` | the bug that makes `text_demo()` crash, Q1 |
| `e_batch_sampler.py` | Q2a, Q2d, Q2e, Q4a, Q5b, `ShuffledSampler`, Q5e |
| `f_sensor_processing.py` | Q1, Q5b, Q5c |
| `g_decorators.py` | `count_calls`, Q3a, Q3b, Q5a, Q6 |
| `h_metrics.py` | Q3, Q4 |
| `i_mutability.py` | Q1a, Q1b, Q1d, Q1e, the bug in `center`, `ListDataset` |
| `j_context_managers.py` | Q1, `seeded`, Q3a, Q3b |

## Using an AI assistant

The repository comes with instructions for AI assistants, so they tutor you instead of solving the puzzles for you. Until you run `make install`, `AGENTS.md` is only a placeholder that tells your assistant to send you here. Pick the version that fits how you use AI:

- **KISSKI, the university AI service:** `make install` sets up the KISSKI version of `AGENTS.md`. It keeps the number of requests low, and tells you how to make yours last.
- **Your own coding agent** (Claude Code, Cursor, Copilot, …): after `make install`, run `make agent-coding` for the coding agent version.
- **A chat in the browser:** after `make install`, run `make chat-bundle` and upload `chat-bundle.md` at the start of the chat. It holds the instructions and every puzzle file. Run it again before a new chat, so it includes your latest code.

To switch back to the KISSKI version, run `make agent-kisski`. After switching, start a new chat.
