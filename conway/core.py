from typing import Dict, Optional, Tuple, Union

from .game import Cell, Stats
from .util import _setup_render_env

T = Union[Union[Stats, Dict[str, int]],
          Tuple[Union[Stats, Dict[str, int]], float, bool]]


def criterion(cell: Cell) -> float:
    r, h = cell.flatten()
    size = cell.size
    loss = abs(sum(r) / size - sum(h) / size)
    return loss


class Env:
    def __init__(self, cell, k=3, return_dict=True, render=None):
        if not isinstance(cell, Cell):
            raise TypeError("cell must be an instance of Cell")
        self.cell = cell
        self.k = k
        self.return_dict = return_dict
        self._render_fn = _setup_render_env(render)
        self.flag = 0
        self.done = False

    def render(self, *args, **kwargs) -> None:
        if self._render_fn is None:
            raise NotImplementedError
        if not isinstance(args[0], (Env, Cell)):
            args = (self.cell, *args)
        self._render_fn(*args, **kwargs)

    def grid_table(self):
        return self.cell.grid_table()

    def step(self, t: Optional[int] = None, return_dict=True) -> T:
        stats = self.cell.forward()
        if return_dict or self.return_dict:
            stats = stats.__dict__  # type: ignore
        if t is not None:
            loss = criterion(self.cell)
            k = self.k
            flag = self.flag
            if t % k == 0:
                self.done = True if flag == k else False
                self.flag = 0
            self.flag += 1 if loss == 0.0 else 0
            return stats, loss, self.done
        else:
            return stats

    def reset(self, p: Optional[float] = None) -> 'Env':
        new_cell = self.cell.reset(p)
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
