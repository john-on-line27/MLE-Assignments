"""Build the agent instructions for this repository from `agents/template.md`.

Usage: `uv run python agents/build_agents.py {kisski,coding,chat}`

- `kisski`: write `AGENTS.md` for KISSKI, the university AI service.
- `coding`: write `AGENTS.md` and `CLAUDE.md` for your own coding agent.
- `chat`: write `chat-bundle.md`, one file to upload to a chat in the browser.

Template syntax: lines between `<!-- only: kisski coding -->` and
`<!-- /only -->` are kept only for the listed variants, and the line
`<!-- REPOSITORY FILES -->` marks where `chat` inlines the repository.

Jokes: every slot of the template's "Bender's joke file" section (a bold
line such as `**After part 1** (Shapes)` under a `### `file`` heading)
gets one option, picked at random, from the slot of the same name in
`agents/jokes.md`. There, every `- ` bullet or fenced code block under a
slot line is one option. A slot without options stays empty.
"""

import argparse
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TEMPLATE = Path(__file__).resolve().parent / "template.md"
DEFAULT_JOKES = Path(__file__).resolve().parent / "jokes.md"
JOKE_SECTION = "## Bender's joke file"
JOKE_FILE_RE = re.compile(r"^### `([^`]+)`\s*$")
JOKE_SLOT_RE = re.compile(r"^\*\*(.+?)\*\*")
VARIANTS = ("kisski", "coding", "chat")
# What to tell the student after a build.
NEXT_STEPS = {
    "kisski": "Lehrer Bender is ready (KISSKI version). Start a new chat. Using your own coding agent? Run `make agent-coding`.",
    "coding": "Lehrer Bender is ready (coding agent version). Start a new chat.",
    "chat": "Upload chat-bundle.md at the start of a new chat. Run `make chat-bundle` again before the next chat, so it has your latest work.",
}
MARKER = "<!-- REPOSITORY FILES -->"
CLOSE = "<!-- /only -->"
OPEN_RE = re.compile(r"^<!-- only:((?: [a-z]+)+) -->$")
CLAUDE_MD = "@AGENTS.md\n"
LANGS = {
    ".py": "python",
    ".md": "markdown",
    ".toml": "toml",
    ".yaml": "yaml",
    ".yml": "yaml",
}
LEAK_RE = re.compile(r"^\s*### BEGIN (SOLUTION|INSTRUCTOR REFERENCE|BUGGY|STUB)\b", re.MULTILINE)


def filter_variant(template: str, variant: str) -> str:
    """Keep the lines of `template` that belong to `variant`."""
    kept: list[str] = []
    allowed: list[str] | None = None
    opened_at = 0
    for number, line in enumerate(template.splitlines(), start=1):
        match = OPEN_RE.match(line)
        if match:
            if allowed is not None:
                sys.exit(f"template line {number}: nested only-block (opened at line {opened_at})")
            allowed = match.group(1).split()
            unknown = [name for name in allowed if name not in VARIANTS]
            if unknown:
                sys.exit(f"template line {number}: unknown variant {', '.join(unknown)}")
            opened_at = number
        elif line == CLOSE:
            if allowed is None:
                sys.exit(f"template line {number}: {CLOSE} without an opening marker")
            allowed = None
        elif allowed is None or variant in allowed:
            kept.append(line)
    if allowed is not None:
        sys.exit(f"template line {opened_at}: only-block is never closed")
    return "\n".join(kept) + "\n"


Jokes = dict[tuple[str, str], list[list[str]]]


def parse_jokes(text: str) -> Jokes:
    """Map (puzzle file, slot name) to the options under that slot in jokes.md.
    Each option is a list of lines: one bullet, or a whole fenced block."""
    options: Jokes = {}
    current_file: str | None = None
    slot: tuple[str, str] | None = None
    block: list[str] | None = None
    opened_at = 0
    for number, line in enumerate(text.splitlines(), start=1):
        if block is not None:
            block.append(line)
            if line.strip() == "```" and slot is not None:
                options[slot].append(block)
                block = None
            continue
        if match := JOKE_FILE_RE.match(line):
            current_file, slot = match.group(1), None
        elif (match := JOKE_SLOT_RE.match(line)) and current_file is not None:
            slot = (current_file, match.group(1).strip())
            options[slot] = []
        elif slot is not None and line.startswith("- "):
            options[slot].append([line])
        elif slot is not None and line.startswith("```"):
            block = [line]
            opened_at = number
    if block is not None:
        sys.exit(f"jokes file line {opened_at}: code block is never closed")
    return options


def joke_section(lines: list[str]) -> tuple[int, int] | None:
    """The index range of the joke section's body (after its heading), or None."""
    if JOKE_SECTION not in lines:
        return None
    start = lines.index(JOKE_SECTION) + 1
    end = next((k for k in range(start, len(lines)) if lines[k].startswith("## ") or lines[k].startswith("<!--")), len(lines))
    return start, end


def fill_jokes(text: str, jokes: Jokes, rng: random.Random) -> str:
    """Put one random option from `jokes` under each slot of the joke section.
    Slots of jokes.md that the template doesn't have are reported on stderr."""
    lines = text.splitlines()
    span = joke_section(lines)
    if span is None:
        return text
    start, end = span
    out = lines[:start]
    used: set[tuple[str, str]] = set()
    current_file: str | None = None
    for line in lines[start:end]:
        out.append(line)
        if match := JOKE_FILE_RE.match(line):
            current_file = match.group(1)
        elif (match := JOKE_SLOT_RE.match(line)) and current_file is not None:
            slot = (current_file, match.group(1).strip())
            if jokes.get(slot):
                used.add(slot)
                out += ["", *rng.choice(jokes[slot])]
    for name, slot_name in sorted(set(jokes) - used):
        if jokes[(name, slot_name)]:
            print(f"warning: jokes file has options for {name} / {slot_name}, but the template has no such slot", file=sys.stderr)
    return "\n".join([*out, *lines[end:]]) + "\n"


def without_jokes(text: str) -> str:
    """`text` with everything under the joke section's slot lines removed, so
    that two builds with different random jokes compare equal."""
    lines = text.splitlines()
    span = joke_section(lines)
    if span is None:
        return text
    start, end = span
    out = lines[:start]
    skipping = False
    for line in lines[start:end]:
        if JOKE_FILE_RE.match(line) or JOKE_SLOT_RE.match(line):
            skipping = bool(JOKE_SLOT_RE.match(line))
            out.append(line)
        elif not skipping:
            out.append(line)
    return "\n".join([*out, *lines[end:]]) + "\n"


def collapse_blank_lines(text: str) -> str:
    """Reduce runs of 3+ blank lines to 2 and end with a single newline."""
    return re.sub(r"\n{4,}", "\n\n\n", text).rstrip("\n") + "\n"


def language(path: str) -> str:
    name = Path(path).name
    return "make" if name == "Makefile" else LANGS.get(Path(path).suffix, "")


def render_file(path: str, text: str) -> str:
    longest = max((len(m) for m in re.findall(r"`+", text)), default=0)
    fence = "`" * max(3, longest + 1)
    body = text.rstrip("\n")
    return f"### `{path}`\n\n{fence}{language(path)}\n{body}\n{fence}"


def repository_files(root: Path) -> list[str]:
    puzzles = sorted(p.name for p in root.glob("[a-z]_*.py"))
    return ["README.md", "Makefile", *puzzles]


def render_repository(root: Path, allow_markers: bool) -> str:
    blocks = []
    for path in repository_files(root):
        text = (root / path).read_text(encoding="utf-8")
        if not allow_markers and LEAK_RE.search(text):
            sys.exit(f"{path} contains instructor markers (solutions would leak); pass --allow-markers to override")
        blocks.append(render_file(path, text))
    return "\n\n".join(blocks)


def render(template: str, variant: str, root: Path, allow_markers: bool, jokes: Jokes, rng: random.Random) -> str:
    if template.splitlines().count(MARKER) != 1:
        sys.exit(f"expected the line {MARKER} exactly once in the template")
    lines = filter_variant(template, variant).splitlines()
    if variant != "chat":
        lines = [line for line in lines if line != MARKER]
    text = fill_jokes("\n".join(lines) + "\n", jokes, rng)
    text = collapse_blank_lines(text)
    if variant == "chat":
        section = render_repository(root, allow_markers)
        text = text.replace(MARKER + "\n", section + "\n")
    return text


def write_outputs(variant: str, text: str, root: Path, ignore_jokes: bool = False) -> list[tuple[Path, str | None]]:
    """Return (path, new content or None to delete) for each output that would
    change. With `ignore_jokes`, outputs that differ only in their randomly
    picked jokes count as unchanged."""

    def same(old: str, new: str) -> bool:
        return without_jokes(old) == without_jokes(new) if ignore_jokes else old == new

    wanted: list[tuple[Path, str | None]]
    claude = root / "CLAUDE.md"
    if variant == "chat":
        wanted = [(root / "chat-bundle.md", text)]
    elif variant == "coding":
        wanted = [(root / "AGENTS.md", text), (claude, CLAUDE_MD)]
    else:
        wanted = [(root / "AGENTS.md", text)]
        if claude.exists() and claude.read_text(encoding="utf-8") == CLAUDE_MD:
            wanted.append((claude, None))
    changes: list[tuple[Path, str | None]] = []
    for path, content in wanted:
        if content is None:
            changes.append((path, None))
        elif not path.exists() or not same(path.read_text(encoding="utf-8"), content):
            changes.append((path, content))
    return changes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("variant", choices=VARIANTS)
    parser.add_argument("--check", action="store_true", help="exit 1 if the output would change; write nothing")
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE, help="template file (default: agents/template.md)")
    parser.add_argument("--allow-markers", action="store_true", help="chat only: allow instructor solution markers in the bundle")
    parser.add_argument(
        "--jokes", type=Path, default=DEFAULT_JOKES, help="joke options (default: agents/jokes.md; slots stay empty if it is missing)"
    )
    parser.add_argument("--seed", type=int, default=None, help="seed for picking the jokes, to repeat a build exactly")
    args = parser.parse_args()
    template = args.template.read_text(encoding="utf-8")
    jokes = parse_jokes(args.jokes.read_text(encoding="utf-8")) if args.jokes.exists() else {}
    text = render(template, args.variant, ROOT, args.allow_markers, jokes, random.Random(args.seed))
    # --check ignores the jokes, which change on every build.
    changes = write_outputs(args.variant, text, ROOT, ignore_jokes=args.check)
    if args.check:
        if changes:
            names = ", ".join(path.name for path, _ in changes)
            sys.exit(
                f"out of date: {names}; run `make agent-{args.variant}`"
                if args.variant != "chat"
                else f"out of date: {names}; run `make chat-bundle`"
            )
        return
    for path, content in changes:
        if content is None:
            path.unlink()
        else:
            path.write_text(content, encoding="utf-8")
    written = [path.name for path, content in changes if content is not None]
    removed = [path.name for path, content in changes if content is None]
    parts = [f"wrote {', '.join(written)}"] if written else ["already up to date"]
    if removed:
        parts.append(f"removed {', '.join(removed)}")
    print("; ".join(parts))
    print(NEXT_STEPS[args.variant])


if __name__ == "__main__":
    main()
