import enum
import random as rand
from collections import OrderedDict
from typing import Dict, Iterator, List, Optional, Tuple, Union

from .nearest import NearestNeighbors, encode_neighbors
from .util import Stats


@enum.unique
class CellState(enum.IntEnum):
    BORN = 0
    KILLED = 1
    SURVIVED = 2


class Grid(object):
    """Base body for an individual cell."""

    def __init__(self, nrows: int = 16, ncols: int = 32, probe: int = 7):
        self.nrows = nrows
        self.ncols = ncols
        self.probe = probe
        self.root = self.init()
        self.hidden = self.base()

    def state(self) -> int:
        return 1 if rand.randint(0, self.probe) == 0 else 0

    def base(self) -> List[List[int]]:
        return [[0 for col in range(self.ncols)]
                for row in range(self.nrows)]

    def init(self) -> List[List[int]]:
        grid = self.base()
        for row in range(self.nrows):
            for col in range(self.ncols):
                grid[row][col] = self.state()
        return grid

    def flatten(self) -> Tuple[List[int], List[int]]:
        def flat(x):
            return [j for i in x for j in i]
        root, hidden = map(flat, (self.root, self.hidden))
        return root, hidden

    def invert(self) -> None:
        """Inverse the root and hidden grids in-place.
        ```python
        grid = Grid()  # initial: root | hidden
        grid.invert()  # method : hidden | root
         ~ grid        # bitwise: root | hidden
        ```
        """
        self.__invert__()

    def __invert__(self):
        self.root, self.hidden = self.hidden, self.root


class Cell(Grid):
    dead_id = 0
    alive_id = 1

    def __init__(self, shape: Tuple[int, int] = (16, 32), probe: int = 7):
        assert sum((shape)) >= 6, \
            f'A grid most be of shape `6x6` or greater, not {shape}'
        super(Cell, self).__init__(*shape, probe)
        self.shape = shape
        self.nn: Optional[NearestNeighbors] = None
        self.size: int = self.shape[0] * self.shape[1]

    def grids(self) -> Dict[str, List[List[int]]]:
        return {'root': self.root, 'hidden': self.hidden}

    def scan(self) -> List[int]:
        alive_id, dead_id = self.alive_id, self.dead_id
        shape, nearest_neighbors = self.shape, encode_neighbors
        observation = [0, 0, 0]  # <born, killed, survived>
        for i in range(shape[0]):
            for j in range(shape[1]):
                self.nn = nearest_neighbors(row=i, col=j, cell=self)
                num_alive_neighbors = self.nn.alive
                if num_alive_neighbors < 2 or num_alive_neighbors > 3:
                    self.hidden[i][j] = dead_id
                    observation[CellState.KILLED] += 1
                elif num_alive_neighbors == 3 and self.root[i][j] == 0:
                    self.hidden[i][j] = alive_id
                    observation[CellState.BORN] += 1
                else:
                    self.hidden[i][j] = self.root[i][j]
                    observation[CellState.SURVIVED] += 1
        return observation

    def forward(self) -> Stats:
        obs = self.scan()
        stats = Stats(*obs)
        self.invert()
        return stats

    def reset(self) -> 'Cell':
        return Cell(self.shape, self.probe)

    def __getitem__(self, idx: int) -> Tuple[List[int], List[int]]:
        return self.root[idx], self.hidden[idx]

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(shape={self.shape})'


class CellBatch(object):
    def __init__(self, cells: List[Cell]):
        self.batch = OrderedDict()
        for i, cell in enumerate(cells):
            cell_id = f'cell_{i}'
            setattr(cell, 'id', cell_id)
            self.batch[cell_id] = cell

    @property
    def batch_size(self) -> int:
        return len(self.batch)

    def __getitem__(self, item: Union[str, int]):
        if isinstance(item, str):
            if item in self.batch:
                return self.batch[item]
        if isinstance(item, int):
            item = f'cell_{item}'
            if item in self.batch:
                return self.batch[item]

    def __iter__(self) -> Iterator[Cell]:
        for cell in self.batch.values():
            yield cell

    def __len__(self) -> int:
        return self.batch_size

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(batch_size={self.batch_size})'
