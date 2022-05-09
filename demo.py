import random
from dataclasses import dataclass

import conway
from conway import all_blocks, fps

# Remove black color in dark theme environments.
cell_colors = list(all_blocks.keys())
cell_colors.pop(cell_colors.index('sb'))


def color_choices():
    return random.choice(cell_colors)


@dataclass
class Hist:
    gen: int = 0
    born: int = 0
    killed: int = 0
    survived: int = 0
    loss: float = 0.0


if __name__ == '__main__':

    env = conway.Env(
        conway.Cell([32, 64], p=1 - 0.6),
        k=3,
        render='console',
        return_dict=True,
    )

    ngens = 5
    t = 0
    gen = 0
    rnd_color = color_choices()  # Random cell color per generation.

    # Independent sampling probability used for drawing the ~Bernoulli(p) dist.
    p_dist = [round(random.uniform(0.2, 0.8), 1) for p_sample in range(ngens)]

    while gen < ngens:
        stat, loss, done = env.step(t)
        hist = Hist(gen+1, loss=loss, **stat)
        env.render(t, hist, ccolor=rnd_color)
        fps(18)
        if done:
            next_p = p_dist.pop()
            env = env.reset(p=next_p)
            rnd_color = color_choices()
            gen += 1
        t += 1
