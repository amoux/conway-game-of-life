# Conway's Game of Life

> Usage

Construct a new `Cell` object.

```python
import conway

cell = conway.Cell(shape=(5, 5), probe=3)
cell.grids()
...
```

Each cell contains two grids; `root` and `hidden` for current and next states.

```bash
{'root': [[0, 0, 1, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 1, 0, 1, 0],
  [0, 1, 0, 1, 0],
  [0, 0, 0, 1, 1]],
 'hidden': [[0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0]]}
```

Initialize the game of life for a single cell by iterating `num_steps` and calling the `cell.forward()` method.

```python
cell = conway.Cell(shape=(20, 25), probe=7)

steps = 50
for step in range(steps):
    stats = cell.forward()
    conway.render_jupyter(
        cell=cell,
        step=step,
        stats=stats,
        state='hidden',
        cellcolor='cy',
        gridcolor='cb',
    )
    conway.fps(29)
...
```

Here's an example of a grid after 29 steps.

```markdown
   steps: 49, born: 0, killed: 440, survived: 60
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫🟡⚫🟡⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫🟡⚫⚫🟡⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫🟡🟡⚫⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫🟡🟡⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫🟡🟡⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫🟡🟡⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫🟡⚫⚫🟡⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫🟡⚫⚫🟡⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫🟡🟡⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫🟡🟡⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫🟡🟡⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫🟡⚫⚫
```

You can also construct a batch of cells with the `CellBatch` container class.

```python
batch = conway.CellBatch([
    conway.Cell(shape=(14, 17), probe=3),
    conway.Cell(shape=(15, 20), probe=1)
])
print(batch)
...
#  CellBatch(batch_size=2)
```

```python
list(batch)
...
#  [Cell(shape=(14, 17)), Cell(shape=(15, 20))]
```

```python
for C in batch:
    print(C.id, C.shape, C.hidden[0])
...
#  cell_0 (14, 17) [0, 0, 0, 0, 0, ...]
#  cell_1 (15, 20) [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ...]
```

```python
max_steps = 60
for C in batch:
    step = 0
    while step < max_steps:
        stats = C.forward()
        conway.render_jupyter(C, step, stats)
        conway.fps(10)
        step += 1
...
```

```markdown
   steps: 59, born: 22, killed: 194, survived: 84
    ⚫⚫⚫⚫⚫🔴🔴🔴⚫⚫⚫🔴🔴🔴⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫🔴🔴🔴⚫⚫⚫🔴🔴🔴⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫🔴🔴⚫⚫⚫🔴🔴⚫⚫⚫⚫⚫⚫⚫
    🔴🔴⚫⚫⚫⚫⚫🔴🔴🔴🔴🔴⚫⚫⚫⚫⚫⚫⚫⚫
    🔴🔴⚫⚫⚫⚫⚫⚫🔴🔴🔴⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫🔴🔴🔴⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫🔴🔴⚫⚫⚫⚫⚫⚫⚫🔴🔴⚫⚫⚫⚫⚫
    ⚫⚫⚫🔴⚫⚫🔴⚫⚫⚫⚫⚫🔴⚫⚫🔴⚫⚫⚫⚫
    ⚫⚫⚫⚫🔴🔴⚫⚫⚫⚫⚫⚫⚫🔴🔴⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫🔴🔴🔴⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫🔴🔴🔴⚫⚫⚫⚫⚫⚫⚫⚫⚫
    🔴⚫⚫⚫⚫⚫⚫🔴🔴🔴🔴🔴⚫⚫⚫⚫⚫⚫⚫🔴
    🔴⚫⚫⚫⚫⚫🔴🔴⚫⚫⚫🔴🔴⚫⚫⚫⚫⚫⚫🔴
```
