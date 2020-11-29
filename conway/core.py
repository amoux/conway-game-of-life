from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from .game import Cell, Stats

Args = Tuple[Any, ...]
Kwargs = Dict[str, Args]


def flatten(x: List[List[Any]]) -> List[Any]:
    return [j for i in x for j in i]


def flatten_grids(cell: Cell) -> Tuple[List[int], List[int]]:
    assert isinstance(cell, Cell)
    g = cell.grids()
    root, hidden = map(flatten, (g['root'], g['hidden']))
    return root, hidden


def criterion(cell: Cell) -> float:
    r, h = flatten_grids(cell)
    size = cell.size
    loss = abs(sum(r) / size - sum(h) / size)
    return loss


class Env:
    def __init__(
        self, k: int = 3,
        probe: int = 7,
        shape: Tuple[int, int] = (16, 32),
        cell: Optional[Cell] = None,
        render_fn: Optional[Callable[[Args, Kwargs], None]] = None,
    ) -> None:
        self.cell = cell if isinstance(cell, Cell) else Cell(shape, probe)
        self.shape = shape
        self.probe = probe
        self.k = k
        self.flag = 0
        self.done = False
        self._render_fn = render_fn

    def grids(self) -> Dict[str, List[List[int]]]:
        return self.cell.grids()

    def step(self, t: Optional[int] = None,
             ) -> Union[Stats, Tuple[Stats, float, bool]]:
        stats = self.cell.forward()
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

    def render(self, *args, **kwargs) -> None:
        if self._render_fn is None:
            raise NotImplementedError
        self._render_fn(*args, **kwargs)

    def reset(self) -> 'Env':
        cell = self.cell.reset()
        return Env(self.k, self.probe, self.shape, cell=cell)

    def close(self):
        ...

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
        return False
