# Conway's Game of Life

![game-of-life-demo](src/demo.gif)

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
C = conway.Cell(shape=(20, 25), probe=7)

steps = 50
for t in range(steps):
    stats = C.forward()
    conway.render_jupyter(C, t, stats, ccolor='cy', gcolor='cb')
    conway.fps(16)
...
```

Here's an example of a grid after 49 steps.

```markdown
   steps: 49, born: 0, killed: 440, survived: 60
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟢⬜🟢⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟢⬜⬜🟢⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟢🟢⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟢🟢⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟢🟢⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜🟢🟢⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜🟢⬜⬜🟢⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜🟢⬜⬜🟢⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜🟢🟢⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜🟢🟢⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜🟢🟢⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟢⬜⬜
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
    t = 0
    while t < max_steps:
        stats = C.forward()
        conway.render_jupyter(C, t, stats)
        conway.fps(10)
        t += 1
...
```

```markdown
   steps: 59, born: 22, killed: 194, survived: 84
    ⬜⬜⬜⬜⬜🔴🔴🔴⬜⬜⬜🔴🔴🔴⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜🔴🔴🔴⬜⬜⬜🔴🔴🔴⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜🔴🔴⬜⬜⬜🔴🔴⬜⬜⬜⬜⬜⬜⬜
    🔴🔴⬜⬜⬜⬜⬜🔴🔴🔴🔴🔴⬜⬜⬜⬜⬜⬜⬜⬜
    🔴🔴⬜⬜⬜⬜⬜⬜🔴🔴🔴⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜🔴🔴🔴⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜🔴🔴⬜⬜⬜⬜⬜⬜⬜🔴🔴⬜⬜⬜⬜⬜
    ⬜⬜⬜🔴⬜⬜🔴⬜⬜⬜⬜⬜🔴⬜⬜🔴⬜⬜⬜⬜
    ⬜⬜⬜⬜🔴🔴⬜⬜⬜⬜⬜⬜⬜🔴🔴⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜🔴🔴🔴⬜⬜⬜⬜⬜⬜⬜⬜⬜
    ⬜⬜⬜⬜⬜⬜⬜⬜🔴🔴🔴⬜⬜⬜⬜⬜⬜⬜⬜⬜
    🔴⬜⬜⬜⬜⬜⬜🔴🔴🔴🔴🔴⬜⬜⬜⬜⬜⬜⬜🔴
    🔴⬜⬜⬜⬜⬜🔴🔴⬜⬜⬜🔴🔴⬜⬜⬜⬜⬜⬜🔴
```

## Demo script

- `k`: N steps to accumulate (.0 losses) before evaluating a state as *"halted"*.
- `probe`: Initial population size (e.g., greater value; less alive cells).

```python
from dataclasses import dataclass
import conway
from conway import fps, all_blocks

# remove black color in dark theme environments.
cell_colors = list(all_blocks.keys())
cell_colors.pop(cell_colors.index('sb'))

def color_choice():
    return conway.rand.choice(cell_colors)

@dataclass
class Hist:
    # customize what information to render (optional).
    gen: int = 0
    born: int = 0
    killed: int = 0
    survived: int = 0
    loss: float = 0.0

env = conway.Env(
    k=3,
    probe=7,
    shape=(32, 64),
    render='jupyter',
    return_dict=True,  # also works; env.step(t,return_dict=True)
)

ngens = 5
t = 0
gen = 0
color = color_choice()
while gen < ngens:
    stats, loss, done = env.step(t)
    hist = Hist(gen, loss=loss, **stats)
    env.render(t+1, hist, ccolor=color)
    fps(16)
    if done:  # similar to open-ai's gym api.
        env = env.reset()
        color = color_choice()
        gen += 1
    t += 1
...
```

`steps: 148, gen: 0 | born: 53 | killed: 1771 | survived: 224 | loss: 0.000488`
