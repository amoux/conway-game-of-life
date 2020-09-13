# Conway's Game of Life

> Usage

Construct a new `Cell` object.

```python
import conway

cell = conway.Cell(shape=(5, 5), max_p=3)
cell.grids()
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
S = "step: {}, alive: {}, dead: {}"

num_steps = 30
cell = conway.Cell(shape=(20, 20), max_p=5)

for step in range(num_steps):
    cell.forward()
    # customize how the grids are rendered.
    conway.render_jupyter(
        cell=cell,
        state='hidden',
        cellcolor='purple',
        gridcolor='black',
        stats=S.format(step, cell.nn.alive, cell.nn.dead)
    )
    conway.time.sleep(1/10)
....
```

Here's an example of a grid after 29 steps.

```markdown
    step: 29, alive: 2, dead: 6
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫♒⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫♒♒♒⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫♒⚫⚫♒♒⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫♒♒⚫⚫⚫♒⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫♒⚫♒♒⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫♒♒⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫♒♒⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫♒⚫⚫⚫⚫♒♒⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫♒♒♒♒⚫♒⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫♒⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫♒♒⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫♒⚫⚫♒
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫♒⚫⚫♒
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫♒♒⚫
```

You can also construct a batch of cells with the `CellBatch` container class.

```python
batch = conway.CellBatch([
    conway.Cell(shape=(14, 17), max_p=3),
    conway.Cell(shape=(15, 20), max_p=1)
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
        C.forward()
        conway.render_jupyter(cell=C, step=step)
        conway.time.sleep(1/10)
        step += 1
...
```

```markdown
    Steps: 24
    ⚫⚫🔴⚫⚫⚫🔴⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    🔴🔴⚫⚫⚫⚫⚫🔴🔴⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫⚫🔴⚫⚫⚫⚫🔴⚫⚫⚫⚫⚫⚫⚫⚫⚫🔴
    ⚫⚫⚫🔴⚫🔴⚫⚫⚫🔴⚫⚫⚫⚫⚫⚫⚫⚫⚫🔴
    ⚫⚫⚫⚫🔴⚫⚫⚫⚫🔴⚫⚫⚫⚫⚫⚫⚫⚫⚫🔴
    🔴🔴⚫⚫⚫⚫⚫🔴🔴⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫🔴⚫⚫⚫🔴⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫🔴⚫⚫⚫🔴⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫🔴🔴🔴⚫⚫⚫⚫⚫⚫⚫⚫⚫🔴⚫⚫⚫🔴
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫🔴⚫⚫🔴⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫🔴⚫🔴⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫🔴⚫⚫
    ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫⚫🔴🔴🔴⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
    ⚫⚫🔴⚫⚫⚫🔴⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫
```
