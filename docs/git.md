# Git

Git is a version control system: it keeps track of how your files change over time. You'll use it in every assignment of this course, and in pretty much any real software or research job after that.

This guide covers the basics. You don't need to read it in one go. Assignment 0 already walks you through the first few commands, so come back here whenever you want to know more or need to look something up.

Two words you'll see everywhere:

- A **repository** (or **repo**) is a folder whose history Git keeps track of. Each assignment is its own repository.
- A **commit** is a saved snapshot of the files in a repository at one point in time, with a short message that says what changed. The history of a repository is just a chain of commits.


## Before you start

Every commit records who made it. Tell Git your name and email address once per computer:

```bash
git config --global user.name "Ada Lovelace"
git config --global user.email "ada@example.com"
```

Not sure if you've done this already? `git config --global user.name` prints the name Git has, or nothing if there is none.


## A practice repository

The best way to learn Git is to try it somewhere you can't break anything. Make a new folder outside your assignments and turn it into a repository:

```bash
mkdir ~/git-practice
cd ~/git-practice
git init -b main
```

`git init` turns the current folder into a repository. You only run it once per repository. The `-b main` gives the first branch the name `main`. More on branches [below](#branches).

In the assignments, `make install` runs `git init` for you.


## Saving a snapshot: `status`, `add`, `commit`

Saving a snapshot takes two steps. First you **stage** the changes you want to save with `git add`. Then you save everything that's staged as a new commit with `git commit`. The two steps let you decide exactly what goes into each commit.

Make a file, then ask Git what it sees:

```bash
echo "Things I learned today" > notes.txt
git status
```

Git lists `notes.txt` as **untracked**: it's new, and Git isn't keeping track of it yet. Stage it and check again:

```bash
git add notes.txt
git status
```

Now `notes.txt` is listed under "Changes to be committed". Save it:

```bash
git commit -m "Add notes file"
```

That's your first commit. `git add .` stages every changed file in the current folder at once, which is handy, but run `git status` first so you know what you're adding.

Run `git status` often. It's easy to keep working, forget to commit, and suddenly find half the repository changed.


## Writing a good commit message

A commit message tells others, and you in a few weeks, what changed. A good message:

- starts with a verb, as if you're giving an instruction: "Add", "Fix", "Answer",
- is short: about 50 characters at most,
- says what changed, not how long it took or how you feel about it.

| Helpful                        | Not helpful       |
| ------------------------------ | ----------------- |
| `Fix unused import in data.py` | `fix`             |
| `Answer task C`                | `stuff`           |
| `Add gradient descent step`    | `final version 2` |

A good moment to commit is whenever you finish a piece of work that makes sense on its own: a function that works, a fixed bug, the answers to one task. Small commits are easier to read and easier to undo than one huge commit.

If you leave out `-m "..."`, Git opens a text editor for you to write the message in.


## Looking at changes: `diff` and `log`

Change the file:

```bash
echo "Git keeps snapshots" >> notes.txt
git diff
```

`git diff` shows what changed since the last commit. Lines starting with `+` were added, lines starting with `-` were removed. Once you stage the change, `git diff` shows nothing any more, because it only shows changes that aren't staged. Use `git diff --staged` to see what you're about to commit:

```bash
git add notes.txt
git diff --staged
git commit -m "Add a note about snapshots"
```

To see the history, use `git log`. The short version puts each commit on one line:

```bash
git log --oneline
```

The string of letters and numbers at the start of each line is the commit's **hash**, a short name Git uses for that commit. Press `q` to leave `git log` if the output fills the screen.


## Branches

A **branch** is a separate line of commits. You can try something on a new branch without touching your main line of work, then either keep it or throw it away.

Make a new branch and switch to it in one step:

```bash
git switch -c try-something
```

`git branch` lists your branches, with a `*` next to the one you're on. Make a commit on the new branch:

```bash
echo "Branches are cheap" >> notes.txt
git add notes.txt
git commit -m "Add a note about branches"
```

Now switch back to `main` and look at the file:

```bash
git switch main
cat notes.txt
```

The new line is gone. It's not lost, it only exists on `try-something`. Switch back and forth a few times and watch the file change.

You'll also see `git checkout` in older guides and on the internet. `git checkout try-something` does the same as `git switch try-something`, and `git checkout -b try-something` does the same as `git switch -c try-something`.


## Merging

Once you're happy with the work on a branch, you bring it back into `main` with a **merge**. Switch to the branch you want to merge *into*, then name the branch you want to merge:

```bash
git switch main
git merge try-something
```

Now `main` has the new line too. You can delete the branch you're done with:

```bash
git branch -d try-something
```

### Merge conflicts

If both branches changed the same lines, Git can't decide which version to keep. It stops the merge and marks the lines in the file:

```text
<<<<<<< HEAD
the version on the branch you're on
=======
the version on the branch you're merging in
>>>>>>> try-something
```

Open the file, edit these lines into what you want to keep, and delete the three marker lines. Then stage the file and commit to finish the merge:

```bash
git add notes.txt
git commit
```

If you'd rather not deal with it right now, `git merge --abort` puts everything back the way it was before the merge.


## Undoing mistakes

| What you want                                       | Command                            |
| --------------------------------------------------- | ---------------------------------- |
| Throw away the changes in a file since the last commit | `git restore <file>`            |
| Unstage a file, but keep the changes                | `git restore --staged <file>`      |
| Fix the message of your last commit                 | `git commit --amend -m "<message>"` |
| Get a file back as it was in an older commit        | `git restore --source <hash> <file>` |

Be careful with the first one: changes that were never committed are gone for good. That's the whole idea behind committing often. Once something is in a commit, it's very hard to lose.


## Git in the assignments

A few things are set up for you in every assignment:

- **`make install`** runs `git init` (and sets up the virtual environment).
- **`.gitignore`** lists files that Git ignores, such as `data/` and `results/`. These are files the code can create again at any time, so they don't belong in the history.
- **Pre-commit checks** run every time you commit. If one finds a problem, the commit stops. Fix what it reports, `git add` the files again, and commit again. Assignment 0 shows you how this works.
- **💾 Commit boxes** in the task prompts tell you when to commit and which message to use.


## Cheat sheet

| Command                       | What it does                                         |
| ----------------------------- | ---------------------------------------------------- |
| `git init`                    | Turn the current folder into a repository.           |
| `git status`                  | Show what changed and what's staged.                 |
| `git add <file>`              | Stage a file for the next commit.                    |
| `git commit -m "<message>"`   | Save the staged changes as a commit.                 |
| `git diff`                    | Show changes that aren't staged yet.                 |
| `git diff --staged`           | Show changes that are staged.                        |
| `git log --oneline`           | Show the history, one commit per line.               |
| `git branch`                  | List branches.                                       |
| `git switch -c <branch>`      | Make a new branch and switch to it.                  |
| `git switch <branch>`         | Switch to an existing branch.                        |
| `git merge <branch>`          | Merge a branch into the one you're on.               |
| `git restore <file>`          | Throw away uncommitted changes in a file.            |
