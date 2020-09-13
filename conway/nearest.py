from typing import List, NamedTuple, Tuple, TypeVar

CellType = TypeVar('CellType')


class Neighbor(NamedTuple):
    state: int
    token: str
    loc: Tuple[int, int]


class NearestNeighbors(List[Neighbor]):
    cell: CellType
    alive: int
    dead: int

    @property
    def num_alive(self) -> int:
        return self.alive

    @property
    def num_dead(self) -> int:
        return self.dead

    def alive_cells(self) -> List[Neighbor]:
        return list(filter(lambda cell: cell.state == 1, self))

    def dead_cells(self) -> List[Neighbor]:
        return list(filter(lambda cell: cell.state == 0, self))

    def __repr__(self) -> str:
        return '{}(alive={}, dead={})'.format(
            self.__class__.__name__, self.num_alive, self.num_dead)


def encode_neighbors(row: int, col: int, cell: CellType) -> None:
    neighbors, alive = [], 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            ix = ((row + i) % cell.shape[0])
            jx = ((col + j) % cell.shape[1])
            state = cell.root[ix][jx]
            token = 'alive' if state == 1 else 'dead'
            alive += state
            neighbors.append(Neighbor(state=state,
                                      token=token,
                                      loc=(ix, jx)))
    assert len(neighbors) == 8
    nn = NearestNeighbors(neighbors)
    nn.alive = alive
    nn.dead = len(nn.dead_cells())
    setattr(cell, 'nn', nn)
