import os
import sys
from typing import Optional, TypeVar

try:
    from IPython.display import clear_output
except ImportError as e:
    print(e)

CellType = TypeVar('CellType')


CELL_COLORS = {
    "blue": "🔵",
    "red": "🔴",
    "green": "♍",
    "purple": "♒",
    "white": "⚪",
    "black": "⚫",
    "yello": "♌",
}

CELL_PADDING = " "
STATS = (
    "\n\tsteps: {step} gen-id: {genid}, alive: "
    "{alive}, hidden: {hidden}, dead: {dead}\n\n\r"
)


def clear_console() -> None:
    """Clear the console using a system command based on OS.
    """
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
                   state="root",
                   cellcolor="red",
                   gridcolor="black",
                   stats: Optional[str] = None,
                   ) -> None:
    clear_console()
    alive_cell_color = CELL_COLORS[cellcolor]
    dead_cell_color = CELL_COLORS[gridcolor]

    grid = cell.grids()[state]

    output = []
    if step is not None:
        output += [f"\b\tSteps: {step}\n\r"]
    elif stats is not None:
        output += [f"\b\t{stats}\n\r"]

    for i in range(cell.shape[0]):
        for j in range(cell.shape[1]):
            cell_state = ""
            if grid[i][j] == 0:
                cell_state = dead_cell_color
            else:
                cell_state = alive_cell_color
            output.append(cell_state)
        output.append("\n\r")

    padding = CELL_PADDING * len(alive_cell_color)
    sequence = "".join(output)
    print(sequence, end=padding)


def render_jupyter(cell: CellType,
                   step: Optional[int] = None,
                   state="root",
                   cellcolor="red",
                   gridcolor="black",
                   stats: Optional[str] = None,
                   ) -> None:
    alive_cell_color = CELL_COLORS[cellcolor]
    dead_cell_color = CELL_COLORS[gridcolor]

    grid = cell.grids()[state]

    output = []
    if step is not None:
        output += [f"\b\tSteps: {step}\n\r"]
    elif stats is not None:
        output += [f"\b\t{stats}\n\r"]

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
    padding = CELL_PADDING * len(alive_cell_color)
    sequence = "".join(output)
    print(sequence, end=padding)
