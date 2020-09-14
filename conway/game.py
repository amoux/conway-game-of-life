import random
from collections import OrderedDict
from copy import deepcopy
from typing import Dict, Iterator, List, Optional, Tuple, Union

from .nearest import NearestNeighbors, encode_neighbors
from .util import Stats


class Grid(object):
    """Base body for an individual cell."""

    def __init__(self, nrows: int = 10, ncols: int = 10, probe: int = 7):
        self.nrows = nrows
        self.ncols = ncols
        self.probe = probe
        self.root = self.init()
        self.hidden = self.base()

    def state(self) -> int:
        return 1 if random.randint(0, self.probe) == 0 else 0

    def base(self) -> List[List[int]]:
        return [[0 for col in range(self.ncols)]
                for row in range(self.nrows)]

    def init(self) -> List[List[int]]:
        grid = self.base()
        for row in range(self.nrows):
            for col in range(self.ncols):
                grid[row][col] = self.state()
        return grid


class Cell(Grid):
    def __init__(self, shape: Tuple[int, int] = (10, 10), probe: int = 7):
        assert sum((shape)) >= 6, \
            f'A grid most be of shape `6x6` or greater, not {shape}'
        super(Cell, self).__init__(*shape, probe)
        self.shape = shape
        self.nn: Optional[NearestNeighbors] = None
        self.size: int = self.shape[0] * self.shape[1]

    def grids(self) -> Dict[str, List[List[int]]]:
        return {'root': self.root, 'hidden': self.hidden}

    def forward(self) -> Stats:
        stats = Stats()
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.nn = encode_neighbors(row=i, col=j, cell=self)
                if self.nn.alive < 2 or self.nn.alive > 3:
                    self.hidden[i][j] = 0
                    stats.killed += 1
                elif self.nn.alive == 3 and self.root[i][j] == 0:
                    self.hidden[i][j] = 1
                    stats.born += 1
                else:
                    self.hidden[i][j] = self.root[i][j]
                    stats.survived += 1

        self.root, self.hidden = (deepcopy(self.hidden),
                                  deepcopy(self.root))
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
