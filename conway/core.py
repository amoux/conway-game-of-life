from dataclasses import asdict
from typing import Dict, List, Optional, Tuple, Union, Any

from .game import Cell, Stats
from .util import Function, render_console, render_jupyter


T = Union[Union[Stats, Dict[str, int]],
          Tuple[Union[Stats, Dict[str, int]], float, bool]]


def criterion(cell: Cell) -> float:
    assert isinstance(cell, Cell)
    r, h = cell.flatten()
    size = cell.size
    loss = abs(sum(r) / size - sum(h) / size)
    return loss


class Env:
    def __init__(
        self,
        k: int = 3,
        probe: int = 7,
        shape: Tuple[int, int] = (16, 32),
        return_dict: bool = True,
        render: Optional[Union[str, Function]] = None,
        cell: Optional[Cell] = None,
    ) -> None:
        self.cell = cell if isinstance(cell, Cell) else Cell(shape, probe)
        self.return_dict = return_dict
        self.shape = shape
        self.probe = probe
        self.k = k
        self.flag = 0
        self.done = False
        self._render_fn = render
        if render is not None:
            if isinstance(render, str):
                if render.lower() in 'jupyter':
                    self._render_fn = render_jupyter
                elif render.lower() in 'console':
                    self._render_fn = render_console
            elif callable(render):
                self._render_fn = render

    def render(self, *args, **kwargs) -> None:
        if self._render_fn is None:
            raise NotImplementedError
        if not isinstance(args[0], (Env, Cell)):
            args = (self.cell, *args)
        self._render_fn(*args, **kwargs)

    def grids(self) -> Dict[str, List[List[int]]]:
        return self.cell.grids()

    def step(self, t: Optional[int] = None, return_dict=True) -> T:
        stats = self.cell.forward()
        if return_dict or self.return_dict:
            stats = stats.__dict__
        if t is not None:
            loss = criterion(self.cell)
            k = self.k
            flag = self.flag
            if t % k == 0:
                self.done = True if flag == k else False
                self.flag = 0
            self.flag += 1 if loss == 0.0 else 0
            return stats, loss, self.done
        return stats

    def reset(self) -> 'Env':
        new_cell = self.cell.reset()
        self.cell = new_cell
        self.flag = 0
        self.done = False
        return self

    def close(self):
        ...

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
        return False
