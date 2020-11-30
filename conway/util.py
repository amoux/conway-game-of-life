import os
import sys
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Callable, Optional, Union, overload

try:
    from IPython.display import clear_output
except ImportError as e:
    print(e)


@dataclass
class Stats:
    born: int = field(default=0, hash=True)
    killed: int = field(default=0, hash=True)
    survived: int = field(default=0, hash=True)


C_PADDING = " "
C_COLORS = {
    "cr": "🔴",
    "cg": "🟢",
    "cp": "🟣",
    "cw": "⚪",
    "cb": "⚫",
    "cy": "🟡",
    "co": "🟠",
    "sr": "🟥",
    "sg": "🟩",
    "sp": "🟪",
    "sw": "⬜",
    "sb": "⬛",
    "sy": "🟨",
    "so": "🟧"
}
C_SQUARE_COLORS = {k: v for k, v in C_COLORS.items() if k[0] == 's'}
C_CIRCLE_COLORS = {k: v for k, v in C_COLORS.items() if k[0] == 'c'}
ST_FORMAT = "born: {born}, killed: {killed}, survived: {survived}"

Function = Callable[[
    Any, Optional[int], Union[str, Stats, None], str, str, str], None]


def stringify_param_class(cls_obj, tmpl="{}: {}", suffix=" | "):
    tmpl = tmpl.format  # verify by calling the format attribute
    if isinstance(cls_obj, dict):
        cls_obj = dict(cls_obj.items())
    elif hasattr(cls_obj, '_asdict'):
        cls_obj = dict(cls_obj._asdict())
    else:
        cls_obj = dict(cls_obj.__dict__.items())
    mapped = [tmpl(k, v) for k, v in cls_obj.items()]
    strseq = suffix.join(mapped)
    return strseq


def process_header(stats=None, step=None):
    header = "" if step is None else f"\bsteps: {step}, "
    if stats is not None:
        if isinstance(stats, str):
            header = f"{stats}"
        elif isinstance(stats, Stats):
            header += ST_FORMAT.format_map(asdict(stats))
        elif isinstance(stats, dict) \
                or hasattr(stats, '_asdict') \
                or hasattr(stats, '__dict__'):
            header += stringify_param_class(stats)
    return header


def fps(rate=10):
    """Shortcut for time.sleep(1/rate)."""
    time.sleep(1 / rate)


def clear_console() -> None:
    """Clear the console using a system command based on OS."""
    if sys.platform.startswith("win"):
        os.system("cls")
    elif sys.platform.startswith("linux"):
        os.system("clear")
    else:
        print("Unable to clear terminal. "
              "Your operating system is not supported.\n\r")


def resize_console(nrows: int, ncols: int) -> None:
    """Resize the console to the size of rows x columns."""
    if ncols < 32:
        ncols = 32
    if sys.platform.startswith("win"):
        ncols = ncols + ncols
        nrows = nrows + 5
        os.system(f"mode con: cols={ncols} lines={nrows}")
    elif sys.platform.startswith("linux"):
        ncols = ncols + ncols
        nrows = nrows + 3
        sys.stdout.write(f"\x1b[8;{nrows};{ncols}t")
    else:
        print("Unable to resize terminal. Your "
              "operating system is not supported.\n\r")


def render_console(
        cell,
        step: Optional[int] = None,
        stats: Optional[Union[str, Stats]] = None,
        state: str = "root",
        ccolor: str = "cr",
        gcolor: str = "cb"
) -> None:
    clear_console()
    output = []
    alive_cell_color = C_COLORS[ccolor]
    dead_cell_color = C_COLORS[gcolor]
    grid = cell.grids()[state]
    header = process_header(stats, step=step)
    output += [f"{header}\n\r"]

    for i in range(cell.shape[0]):
        for j in range(cell.shape[1]):
            cell_state = ""
            if grid[i][j] == 0:  # <dead cell id>
                cell_state = dead_cell_color
            else:
                cell_state = alive_cell_color
            output.append(cell_state)
        output.append("\n\r")

    padding = C_PADDING * len(alive_cell_color)
    sequence = "".join(output)
    print(sequence, end=padding)


def render_jupyter(
    cell,
    step: Optional[int] = None,
    stats: Optional[Union[str, Stats]] = None,
    state: str = "root",
    ccolor: str = "cr",
    gcolor: str = "cb",
) -> None:
    output = []
    alive_cell_color = C_COLORS[ccolor]
    dead_cell_color = C_COLORS[gcolor]
    grid = cell.grids()[state]
    header = process_header(stats, step=step)
    output += [f"{header}\n\r"]

    for i in range(cell.shape[0]):
        for j in range(cell.shape[1]):
            cell_state = ""
            if grid[i][j] == 0:  # <dead cell id>
                cell_state = dead_cell_color
            else:
                cell_state = alive_cell_color
            output.append(cell_state)
        output.append("\n\r")

    clear_output(True)
    padding = C_PADDING * len(alive_cell_color)
    sequence = "".join(output)
    print(sequence, end=padding)
