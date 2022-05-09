import random
from collections import OrderedDict, namedtuple
from typing import (Any, Dict, Iterator, List, NamedTuple, Optional, Tuple,
                    Union)

from .util import Stats

Point = Tuple[int, int]

id_to_label = ["dead", "alive"]
DEFAULT_SHAPE = (16, 32)
DEAD_CELL = 0
ALIVE_CELL = 1

Observation = namedtuple(
    'Observation', ['born', 'killed', 'survived'])


class GridTable(Dict):
    def hidden(self):
        return self.get('hidden', [])

    def visible(self):
        return self.get('visible', [])


class NeighborNode(NamedTuple):
    state: int
    label: str
    loc: Point

    def __repr__(self):
        return f"NeighborNode({self.label}, loc={self.loc})"


class NeighborList(List[NeighborNode]):
    alive: int = 0

    def __new__(cls, iterable=[]):
        return super().__new__(cls, iterable)

    def get_alive_cells(self) -> List[NeighborNode]:
        return list(filter(lambda cell: cell.state == 1, self))

    def get_dead_cells(self) -> List[NeighborNode]:
        return list(filter(lambda cell: cell.state == 0, self))

    def linearsearch(self, loc: Point) -> Optional[NeighborNode]:
        for cell in self:
            if cell.loc == loc:
                return cell
        return None

    def set_alive(self, alive: int):
        self.alive = alive
        return self

    def add(self, state: int, loc: Tuple[int, int]):
        self.append(NeighborNode(state, id_to_label[state], loc))

    @staticmethod
    def points() -> List[Point]:
        p = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                p.append((i, j))
        return p

    def __repr__(self) -> str:
        return "{}(alive={}, size={})".format(
            self.__class__.__name__, self.alive, len(self))


class Grid(object):
    """Base body for an individual cell."""
    kernels = NeighborList.points()

    def __init__(self, *shape: Any, p: float = 0.5, **kwargs: Any):
        shape = kwargs.get('shape', shape)
        if len(shape) > 0 and isinstance(shape[0], (tuple, list)):
            shape = tuple(shape[0])
        if not shape:
            shape = DEFAULT_SHAPE
        if len(shape) != 2:
            raise ValueError('shape must be a tuple pair of size 2')
        if shape[0] < 3 and shape[1] < 3:
            raise ValueError('shape must be at least 3x3')
        p = float(p)
        if p > 1 or p < 0:
            raise ValueError('p must be between 0.0 and 1.0')
        self.shape = shape
        self.size = shape[0] * shape[1]
        self.p = p
        self.visible = self.bernoulli(p)
        self.hidden = self.zeros()

    def reset(self, p: Optional[float] = None):
        if p is None:
            p = self.p
        self.visible = self.bernoulli(p)
        self.hidden = self.zeros()
        return self

    def grid_shape(self):
        return self.shape

    def grid_table(self) -> GridTable:
        return GridTable(visible=self.visible, hidden=self.hidden)

    def zeros(self) -> List[List[int]]:
        return [[0 for col in range(self.shape[1])]
                for row in range(self.shape[0])]

    def bernoulli(self, p=0.5):
        return [[int(random.uniform(0, 1) < p) for col in range(self.shape[1])]
                for row in range(self.shape[0])]

    def flatten(self) -> Tuple[List[int], List[int]]:
        def flat(x):
            return [j for i in x for j in i]
        visible, hidden = map(flat, (self.visible, self.hidden))
        return visible, hidden

    def invert(self):
        """Invert the visible and hidden grids in-place."""
        self.__invert__()
        return self

    def orthogonal(self, stride: int, fill_value=1, matrix=None):
        if matrix is None:
            matrix = self.zeros()
        m, n = self.shape
        for (ik, jk) in self.kernels:
            matrix[(ik + stride) % m][(jk + stride) % n] = fill_value
        return matrix

    def __invert__(self):
        self.visible, self.hidden = self.hidden, self.visible

    def __getitem__(self, item) -> Tuple[List[int], List[int]]:
        return self.visible[item], self.hidden[item]


class Cell(Grid):
    dead_id = DEAD_CELL
    alive_id = ALIVE_CELL
    directions = NeighborList.points()

    def __init__(self, *shape: Any, p: float = 0.5, **kwargs: Any):
        super(Cell, self).__init__(*shape, p=p, **kwargs)
        self.neighbors: Optional[NeighborList] = None

    def compute_neighbors(self, *cell_target) -> NeighborList:
        row, col, m, n = cell_target
        neighbors = NeighborList()
        num_alive = 0
        visible_grid = self.visible
        for (i, j) in self.directions:
            i_k, j_k = (i + row) % m, (j + col) % n
            cell_state = visible_grid[i_k][j_k]
            num_alive += cell_state
            neighbors.add(cell_state, (i_k, j_k))
        return neighbors.set_alive(num_alive)

    def step(self) -> Observation:
        m, n = self.grid_shape()
        visible_grid, hidden_grid = self.visible, self.hidden
        born, killed, survived = 0, 0, 0
        for i in range(m):
            for j in range(n):
                to_update = self.compute_neighbors(i, j, m, n)
                num_alive = to_update.alive
                if num_alive < 2 or num_alive > 3:
                    hidden_grid[i][j] = DEAD_CELL
                    killed += 1
                elif num_alive == 3 and visible_grid[i][j] == 0:
                    hidden_grid[i][j] = ALIVE_CELL
                    born += 1
                else:
                    hidden_grid[i][j] = visible_grid[i][j]
                    survived += 1
                self.neighbors = to_update
        return Observation(born, killed, survived)

    def forward(self) -> Stats:
        obs = self.step()
        self.invert()
        return Stats(*obs)

    def get_alive_neighbors(self, *cell_point, **kwd) -> NeighborList:
        row = kwd.get('row', cell_point[0])
        col = kwd.get('col', cell_point[1])
        return self.compute_neighbors(row, col, *self.grid_shape())

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(shape={self.shape})'


class CellBatch:
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
