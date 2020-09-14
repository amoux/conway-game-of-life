import os
import sys
import time
from dataclasses import dataclass, field
from typing import Optional, TypeVar, Union

try:
    from IPython.display import clear_output
except ImportError as e:
    print(e)

CellType = TypeVar('CellType')

ST_FORMAT = "born: {born}, killed: {killed}, survived: {survived}"

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


@dataclass
class Stats:
    born: int = field(default=0, hash=True)
    killed: int = field(default=0, hash=True)
    survived: int = field(default=0, hash=True)


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


def render_console(cell: CellType,
                   step: Optional[int] = None,
                   stats: Optional[Union[str, Stats]] = None,
                   state="root",
                   ccolor="cr",
                   gcolor="cb",
                   ) -> None:
    clear_console()
    alive_cell_color = C_COLORS[ccolor]
    dead_cell_color = C_COLORS[gcolor]

    grid = cell.grids()[state]

    output = []
    header = "" if step is None else f"\bsteps: {step}, "
    if stats is not None:
        if isinstance(stats, Stats):
            header += ST_FORMAT.format_map(stats.__dict__)
        else:
            header = f"{stats}"
        output += [f"{header}\n\r"]

    for i in range(cell.shape[0]):
        for j in range(cell.shape[1]):
            cell_state = ""
            if grid[i][j] == 0:
                cell_state = dead_cell_color
            else:
                cell_state = alive_cell_color
            output.append(cell_state)
        output.append("\n\r")

    padding = C_PADDING * len(alive_cell_color)
    sequence = "".join(output)
    print(sequence, end=padding)


def render_jupyter(cell: CellType,
                   step: Optional[int] = None,
                   stats: Optional[Union[str, Stats]] = None,
                   state="root",
                   ccolor="cr",
                   gcolor="cb",
                   ) -> None:
    alive_cell_color = C_COLORS[ccolor]
    dead_cell_color = C_COLORS[gcolor]

    grid = cell.grids()[state]

    output = []
    header = "" if step is None else f"steps: {step}, "
    if stats is not None:
        if isinstance(stats, Stats):
            header += ST_FORMAT.format_map(stats.__dict__)
        else:
            header = f"{stats}"
        output += [f"{header}\n\r"]

    for i in range(cell.shape[0]):
        for j in range(cell.shape[1]):
            cell_state = ""
            if grid[i][j] == 0:
                cell_state = dead_cell_color
            else:
                cell_state = alive_cell_color
            output.append(cell_state)
        output.append("\n\r")

    clear_output(True)
    padding = C_PADDING * len(alive_cell_color)
    sequence = "".join(output)
    print(sequence, end=padding)
