from typing import List, NamedTuple, Tuple, TypeVar

CellType = TypeVar('CellType')


class CellState(NamedTuple):
    state: int
    token: str
    loc: Tuple[int, int]


class NearestNeighbors(List[CellState]):
    alive: int

    def alive_cells(self) -> List[CellState]:
        return list(filter(lambda cell: cell.state == 1, self))

    def dead_cells(self) -> List[CellState]:
        return list(filter(lambda cell: cell.state == 0, self))

    def __repr__(self) -> str:
        return '{}(alive={}, dead={})'.format(
            self.__class__.__name__, self.alive, self.dead)


def encode_neighbors(row: int, col: int, cell: CellType) -> NearestNeighbors:
    alive = 0
    states = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            ix = ((row + i) % cell.shape[0])
            jx = ((col + j) % cell.shape[1])
            state = cell.root[ix][jx]
            alive += state
            token = 'alive' if state == 1 else 'dead'

            states.append(CellState(state, token, loc=(ix, jx)))

    assert len(states) == 8
    nn = NearestNeighbors(states)
    nn.alive = alive

    return nn
