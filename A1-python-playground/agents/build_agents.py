"""Build the agent instructions for this repository from `agents/template.md`.

Usage: `uv run python agents/build_agents.py {kisski,coding,chat}`

- `kisski`: write `AGENTS.md` for KISSKI, the university AI service.
- `coding`: write `AGENTS.md` and `CLAUDE.md` for your own coding agent.
- `chat`: write `chat-bundle.md`, one file to upload to a chat in the browser.

Template syntax: lines between `<!-- only: kisski coding -->` and
`<!-- /only -->` are kept only for the listed variants, and the line
`<!-- REPOSITORY FILES -->` marks where `chat` inlines the repository.
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TEMPLATE = Path(__file__).resolve().parent / "template.md"
VARIANTS = ("kisski", "coding", "chat")
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


def render(template: str, variant: str, root: Path, allow_markers: bool) -> str:
    if template.splitlines().count(MARKER) != 1:
        sys.exit(f"expected the line {MARKER} exactly once in the template")
    lines = filter_variant(template, variant).splitlines()
    if variant != "chat":
        lines = [line for line in lines if line != MARKER]
    text = collapse_blank_lines("\n".join(lines) + "\n")
    if variant == "chat":
        section = render_repository(root, allow_markers)
        text = text.replace(MARKER + "\n", section + "\n")
    return text


def write_outputs(variant: str, text: str, root: Path) -> list[tuple[Path, str | None]]:
    """Return (path, new content or None to delete) for each output that would change."""
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
        elif not path.exists() or path.read_text(encoding="utf-8") != content:
            changes.append((path, content))
    return changes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("variant", choices=VARIANTS)
    parser.add_argument("--check", action="store_true", help="exit 1 if the output would change; write nothing")
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE, help="template file (default: agents/template.md)")
    parser.add_argument("--allow-markers", action="store_true", help="chat only: allow instructor solution markers in the bundle")
    args = parser.parse_args()
    template = args.template.read_text(encoding="utf-8")
    text = render(template, args.variant, ROOT, args.allow_markers)
    changes = write_outputs(args.variant, text, ROOT)
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


if __name__ == "__main__":
    main()
