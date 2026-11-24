"""
Pictures for the visual puzzles. You don't need to read this file.

The puzzle files call `check(name, fn)`, which builds the input for one
problem, runs your function on it, and shows the input, your result and the
target side by side.
"""

import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any

import numpy as np

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

# A 16 x 24 pixel-art robot. It is deliberately not symmetric (antenna on the
# left, arm raised on the right, badge on the left), so every flip, rotation
# and transpose looks different, and it is not square, so reshaping (H, W) to
# (W, H) is never a no-op.
_ROBOT = [
    "......R.................",
    "......D............GG...",
    "......D............GG...",
    "...GGGGGGGG........DD...",
    "...GYYGGYYG........DD...",
    "...GYDGGYYG........DD...",
    "...GGGGGGGG........DD...",
    "...GGMMMMGG........DD...",
    "...GGGGGGGG........DD...",
    ".....DDDD..........DD...",
    "..GGGGGGGGGGDDDDDDDDD...",
    "..GBBGGGGGGG............",
    "..GBBGGRRGGG............",
    "..GGGGGGGGGG............",
    "...DD....DD.............",
    "KKKDDKKKKDDKKKKKKKKKKKKK",
]

_COLOURS = {
    "G": (160, 168, 180),  # body
    "D": (70, 74, 84),  # dark metal
    "Y": (250, 200, 40),  # eyes
    "M": (20, 20, 20),  # mouth
    "R": (220, 50, 50),  # antenna tip, button
    "B": (40, 110, 220),  # badge
    "K": (60, 150, 60),  # ground
}

_TINTS = [(160, 168, 180), (230, 120, 80), (90, 180, 120), (230, 190, 70), (200, 110, 190), (100, 160, 230)]


def robot(scale: int = 4, body: tuple[int, int, int] = _COLOURS["G"]) -> np.ndarray:
    """The robot as a (16 * scale, 24 * scale, 3) uint8 picture on a sky gradient."""

    h, w = len(_ROBOT), len(_ROBOT[0])
    img = np.zeros((h * scale, w * scale, 3), dtype=np.uint8)
    # Sky: dark blue at the top, light at the bottom, so up and down differ.
    sky = np.linspace([90, 140, 210], [215, 232, 250], h * scale).astype(np.uint8)
    img[:] = sky[:, None, :]
    colours = dict(_COLOURS, G=body)
    for i, row in enumerate(_ROBOT):
        for j, ch in enumerate(row):
            if ch != ".":
                img[i * scale : (i + 1) * scale, j * scale : (j + 1) * scale] = colours[ch]
    return img


def sprites() -> np.ndarray:
    """A batch of six small robots in different colours, shape (6, 32, 48, 3)."""

    return np.stack([robot(scale=2, body=t) for t in _TINTS])


def scrambled_robot() -> np.ndarray:
    """The robot cut into 16 x 16 patches, with the patch grid flipped on its diagonal. Shape (96, 64, 3)."""

    img = robot()
    out = np.zeros((96, 64, 3), dtype=np.uint8)
    for i in range(4):
        for j in range(6):
            out[j * 16 : (j + 1) * 16, i * 16 : (i + 1) * 16] = img[i * 16 : (i + 1) * 16, j * 16 : (j + 1) * 16]
    return out


# ---------------------------------------------------------------------------
# Drawing
# ---------------------------------------------------------------------------

_INK, _MUTED = "#0b0b0b", "#52514e"

# A panel is (title, array or None, kind, options). None means "this can't be
# drawn"; the message goes in options["error"].
Panel = tuple[str, Any, str, dict[str, Any]]


def _text(ax: Any, message: str) -> None:
    ax.text(0.5, 0.5, message, ha="center", va="center", wrap=True, fontsize=10, color=_MUTED, transform=ax.transAxes)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color("#d0d0d0")


def _image_problem(arr: np.ndarray) -> str | None:
    if arr.ndim == 2 or (arr.ndim == 3 and arr.shape[2] == 3):
        return None
    if arr.ndim == 3 and arr.shape[2] == 1:
        return f"shape {arr.shape}\n\nA picture needs (H, W) or (H, W, 3).\nThe last axis has size 1."
    if arr.ndim == 3 and arr.shape[0] == 3:
        return f"shape {arr.shape}\n\nA picture needs (H, W, 3):\nthe colour axis must be last."
    return f"shape {arr.shape}\n\nA picture needs (H, W) or (H, W, 3)."


def _draw_image(ax: Any, arr: np.ndarray, grid: int | None = None) -> None:
    problem = _image_problem(arr)
    if problem:
        _text(ax, problem)
        return
    ax.imshow(arr, cmap="gray" if arr.ndim == 2 else None, interpolation="nearest")
    if grid:
        for y in range(grid, arr.shape[0], grid):
            ax.axhline(y - 0.5, color="white", linewidth=1.5)
        for x in range(grid, arr.shape[1], grid):
            ax.axvline(x - 0.5, color="white", linewidth=1.5)
    ax.set_xticks([])
    ax.set_yticks([])


def _draw_planes(ax: Any, arr: np.ndarray) -> None:
    """(C, H, W) drawn as C grey pictures next to each other."""

    C, H, W = arr.shape
    gap = max(2, W // 16)
    canvas = np.full((H, C * W + (C - 1) * gap), 255, dtype=arr.dtype)
    for c in range(C):
        canvas[:, c * (W + gap) : c * (W + gap) + W] = arr[c]
        ax.text(c * (W + gap) + W / 2, H + gap, f"[{c}]", ha="center", va="top", fontsize=9, color=_MUTED)
    ax.imshow(canvas, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)


def _draw_tiles(ax: Any, arr: np.ndarray, vmax: int) -> None:
    """
    Numbered cells, shaded by value. The numbers are the elements' positions
    in the original array's reading order. A 3-D array is drawn as one 2-D
    slice per index of axis 0, left to right.
    """

    import matplotlib.pyplot as plt

    if arr.ndim == 2:
        arr = arr[None]
    if arr.ndim != 3:
        _text(ax, f"shape {arr.shape}\n\ncan only draw 2-D or 3-D tiles")
        return
    S, R, C = arr.shape
    cmap = plt.get_cmap("Blues")
    for s in range(S):
        x0 = s * (C + 1)
        for r in range(R):
            for c in range(C):
                v = int(arr[s, r, c])
                shade = 0.15 + 0.6 * v / max(vmax, 1)
                ax.add_patch(plt.Rectangle((x0 + c, r), 1, 1, facecolor=cmap(shade), edgecolor="white", linewidth=2))
                ax.text(x0 + c + 0.5, r + 0.5, str(v), ha="center", va="center", fontsize=9, color=_INK if shade < 0.55 else "white", zorder=5)
        if S > 1:
            ax.text(x0 + C / 2, -0.25, f"[{s}]", ha="center", va="bottom", fontsize=9, color=_MUTED)
    ax.set_xlim(-0.2, S * (C + 1) - 0.8)
    ax.set_ylim(R + 0.2, -0.8)
    ax.set_aspect("equal")
    ax.axis("off")


def _draw_patches(ax: Any, arr: np.ndarray, cols: int, numbers: bool = False) -> None:
    """
    (N, h, w, 3) drawn as a grid of small pictures with white gaps, `cols` per
    row, in index order. With `numbers`, each picture gets its index.
    """

    if arr.ndim != 4 or arr.shape[3] != 3:
        _text(ax, f"shape {arr.shape}\n\nexpected (N, h, w, 3)")
        return
    N, h, w, _ = arr.shape
    rows = -(-N // cols)
    gap = max(1, min(h, w) // 6)
    canvas = np.full((rows * (h + gap) - gap, cols * (w + gap) - gap, 3), 255, dtype=np.uint8)
    for n in range(N):
        r, c = divmod(n, cols)
        canvas[r * (h + gap) : r * (h + gap) + h, c * (w + gap) : c * (w + gap) + w] = arr[n]
    ax.imshow(canvas, interpolation="nearest")
    if numbers:
        for n in range(N):
            r, c = divmod(n, cols)
            ax.text(
                c * (w + gap) + 1,
                r * (h + gap) + 1,
                str(n),
                ha="left",
                va="top",
                fontsize=7,
                color=_INK,
                bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.5},
            )
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)


def _draw(ax: Any, panel: Panel) -> None:
    title, arr, kind, opts = panel
    ax.set_title(title, fontsize=10, color=_INK, loc="left")
    if arr is None:
        _text(ax, opts.get("error", "nothing to draw"))
        return
    arr = np.asarray(arr)
    if kind == "image":
        _draw_image(ax, arr, opts.get("grid"))
    elif kind == "planes":
        _draw_planes(ax, arr)
    elif kind == "tiles":
        _draw_tiles(ax, arr, opts.get("vmax", int(arr.max())))
    elif kind == "patches":
        _draw_patches(ax, arr, opts.get("cols", 6), opts.get("numbers", False))


def show(title: str, panels: list[Panel], cols: int | None = None, filename: str = "figure") -> None:
    """Draws the panels in a grid and shows the figure (or saves it, if there is no screen)."""

    import matplotlib.pyplot as plt

    cols = cols or len(panels)
    rows = -(-len(panels) // cols)
    fig, axes = plt.subplots(rows, cols, figsize=(3.6 * cols, 3.4 * rows), squeeze=False)
    for ax, panel in zip(axes.flat, panels, strict=False):
        _draw(ax, panel)
    for ax in axes.flat[len(panels) :]:
        ax.axis("off")
    fig.suptitle(title, fontsize=12, color=_INK, x=0.01, ha="left")
    fig.tight_layout()
    _present(fig, filename)


def _present(fig: Any, filename: str) -> None:
    """Shows the figure, or saves it if there is no screen, and closes it."""

    import matplotlib.pyplot as plt

    if plt.get_backend().lower() in {"agg", "pdf", "ps", "svg", "pgf", "cairo", "template"}:
        path = Path(tempfile.gettempdir()) / f"{filename}.png"
        fig.savefig(path, dpi=110)
        print(f"No screen to show the figure on. Saved it to {path}")
    else:
        plt.show()
    plt.close(fig)


# ---------------------------------------------------------------------------
# Checking an attempt
# ---------------------------------------------------------------------------


def _attempt(fn: Callable[..., Any], *args: Any) -> tuple[Any, str]:
    """Runs fn and returns (result, error message). Never raises."""

    try:
        out = fn(*args)
    except Exception as e:  # noqa: BLE001 - any error becomes a message in the picture
        return None, f"Your function raised\n{type(e).__name__}:\n{e}"
    if out is None:
        return None, "Your function returned None.\n(Not done yet?)"
    return np.asarray(out), ""


def _yours(fn: Callable[..., Any], target: np.ndarray, kind: str, opts: dict[str, Any], *args: Any) -> Panel:
    out, error = _attempt(fn, *args)
    if out is None:
        return ("yours", None, kind, {"error": error})
    if out.shape != target.shape:
        verdict = f"yours {out.shape}: wrong shape ✗"
    elif np.allclose(out, target):
        verdict = f"yours {out.shape}: matches ✓"
    else:
        verdict = f"yours {out.shape}: right shape, wrong values ✗"
    return (verdict, out, kind, opts)


def _compare(name: str, title: str, given: list[Panel], fn: Callable[..., Any], target: np.ndarray, kind: str, *args: Any, **opts: Any) -> None:
    panels = [*given, _yours(fn, target, kind, opts, *args), (f"target {target.shape}", target, kind, opts)]
    show(f"{name}: {title}", panels, filename=f"visual_{name}")


def _candidates(name: str, title: str, given: Panel, lines: dict[str, str], seed: int, kind: str, env: dict[str, Any], **opts: Any) -> None:
    """Shows the given array and the results of the code `lines`, as numbered panels in a shuffled order."""

    panels = [given]
    order = np.random.default_rng(seed).permutation(sorted(lines))
    for n, letter in enumerate(order, start=1):
        out = eval(lines[letter], {"np": np}, env)  # the lines are fixed strings in this file
        panels.append((f"{n}   shape {out.shape}", out, kind, opts))
    cols = 3 if kind == "tiles" and np.ndim(given[1]) == 3 else len(panels)
    show(f"{name}: {title}", panels, cols=cols, filename=f"visual_{name}")


def _cut_into_patches_steps(img: np.ndarray, p: int) -> None:
    """The worked example `cut_into_patches`, one panel per step, plus what happens without step 2."""

    import matplotlib.pyplot as plt

    H, W, _ = img.shape
    nh, nw = H // p, W // p
    step1 = img.reshape(nh, p, nw, p, 3)
    step2 = step1.transpose(0, 2, 1, 3, 4)
    step3 = step2.reshape(nh * nw, p, p, 3)
    skipped = img.reshape(nh * nw, p, p, 3)

    # Steps 1 and 2 are drawn by the same rule: one cell for each grid[i, j],
    # i down and j across. Flattening the first two axes lists the cells in
    # that order.
    cells1 = step1.reshape(nh * p, nw, p, 3)
    cells2 = step2.reshape(nh * nw, p, p, 3)

    fig = plt.figure(figsize=(10.8, 9.0))
    gs = fig.add_gridspec(3, 3, height_ratios=[1.0, 0.7, 1.0])
    panels: list[tuple[Any, Panel]] = [
        (gs[0, 0], (f"img {img.shape}, cut every {p} pixels", img, "image", {"grid": p})),
        (
            gs[1, :],
            (f"1. reshape to {step1.shape}:  cell (i, j) is grid[i, j], one picture row cut into {nw} pieces", cells1, "patches", {"cols": p}),
        ),
        (gs[2, 0], (f"2. transpose to {step2.shape}\ncell (i, j) is grid[i, j], one patch", cells2, "patches", {"cols": nw})),
        (gs[2, 1], (f"3. reshape to {step3.shape}\ncell n is result[n], in reading order", step3, "patches", {"cols": 12, "numbers": True})),
        (gs[2, 2], (f"without step 2: img.reshape{skipped.shape}\neach 'patch' is picture rows, folded", skipped, "patches", {"cols": nw})),
    ]
    for spec, panel in panels:
        _draw(fig.add_subplot(spec), panel)

    note = fig.add_subplot(gs[0, 1:])
    note.axis("off")
    note.text(
        0.0,
        0.5,
        "Steps 1 and 2 are drawn the same way: one cell for each grid[i, j],\n"
        "with i going down and j going across. Only the transpose turns\n"
        "grid[i, j] into a patch.",
        fontsize=10,
        color=_MUTED,
        va="center",
    )

    fig.suptitle("cut_into_patches, step by step", fontsize=12, color=_INK, x=0.01, ha="left")
    fig.tight_layout()
    _present(fig, "visual_cut_into_patches")


NAMES = [
    "Q1e",
    "Q1f",
    "rotate_clockwise",
    "merge_channels",
    "swap_halves",
    "cut_into_patches",
    "contact_sheet",
    "unscramble",
    "channels_last",
]


def check(name: str, fn: Any = None) -> None:
    """Shows one problem. `fn` is the student's function (not used by Q1e, Q1f and cut_into_patches)."""

    img = robot()
    H, W, _ = img.shape

    if name == "Q1e":
        s = np.arange(24).reshape(2, 3, 4)
        lines = {"A": "s.transpose(1, 0, 2)", "B": "s.transpose(0, 2, 1)", "C": "s.swapaxes(0, 2)", "D": "s.reshape(3, 2, 4)"}
        _candidates(name, "which line made which stack?", (f"s {s.shape}", s, "tiles", {"vmax": 23}), lines, 82, "tiles", {"s": s}, vmax=23)

    elif name == "Q1f":
        lines = {
            "A": "img.transpose(1, 0, 2)",
            "B": "img.reshape(W, H, 3)",
            "C": "img.transpose(2, 0, 1).reshape(H, W, 3)",
            "D": "img[::-1]",
        }
        _candidates(name, "which line made which picture?", (f"img {img.shape}", img, "image", {}), lines, 50, "image", {"img": img, "H": H, "W": W})

    elif name == "rotate_clockwise":
        target = np.rot90(img, k=-1)
        _compare(name, "rotate a quarter turn clockwise", [(f"given {img.shape}", img, "image", {})], fn, target, "image", img)

    elif name == "merge_channels":
        r, g, b = img[..., 0], img[..., 1], img[..., 2]
        channels: list[Panel] = [(f"r {r.shape}", r, "image", {}), (f"g {g.shape}", g, "image", {}), (f"b {b.shape}", b, "image", {})]
        _compare(name, "three channels to one colour picture", channels, fn, img, "image", r, g, b)

    elif name == "swap_halves":
        target = np.concatenate([img[:, W // 2 :], img[:, : W // 2]], axis=1)
        _compare(name, "swap the left and right halves", [(f"given {img.shape}", img, "image", {})], fn, target, "image", img)

    elif name == "cut_into_patches":
        _cut_into_patches_steps(img, 16)

    elif name == "contact_sheet":
        b = sprites()
        _, h, w, _ = b.shape
        target = np.zeros((2 * h, 3 * w, 3), dtype=np.uint8)
        for n in range(6):
            row, col = divmod(n, 3)
            target[row * h : (row + 1) * h, col * w : (col + 1) * w] = b[n]
        batch: Panel = (f"given {b.shape}", b, "patches", {"cols": 6})
        _compare(name, "a 2 x 3 contact sheet", [batch], fn, target, "image", b, 2, 3)

    elif name == "unscramble":
        s = scrambled_robot()
        _compare(name, "unscramble", [(f"given {s.shape}", s, "image", {})], fn, img, "image", s)

    elif name == "channels_last":
        # The robot as a batch of one channels-first picture; we show picture 0 of your result.
        x = np.ascontiguousarray(img.transpose(2, 0, 1))
        planes: list[Panel] = [(f"given {x.shape} (one picture of the batch)", x, "planes", {})]
        _compare(name, "channels first to channels last", planes, lambda batch: fn(batch)[0], img, "image", x[None])

    else:
        raise ValueError(f"there is no picture called {name!r}")
