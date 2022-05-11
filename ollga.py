from math import e, log, ceil
from multiprocessing import Pool
import numpy as np


def flip(x, i):
    x[i] = (x[i] + 1) % 2


def f(x):
    return x.sum()


def f_noisy(x, q, n):
    # return f(x)
    x_noisy = x.copy()
    for i in range(len(x)):
        if np.random.uniform() < q / n:
            flip(x_noisy, i)
    return f(x_noisy)


def mutation(n, lmbd, q, x):
    l = np.random.binomial(n, lmbd / n)
    x_mutated = x.copy()
    f_x_mutated = -1
    for _ in range(lmbd):
        y = x.copy()
        idx = np.random.choice(n, l, replace=False)
        for i in idx:
            flip(y, i)
        f_y = f_noisy(y, q, n)

        if f_y > f_x_mutated:
            x_mutated = y
            f_x_mutated = f_y

    return x_mutated, f_x_mutated


def crossover(n, lmbd, q, x, x_mutated):
    y_crossover = x.copy()
    f_y_crossover = -1
    for _ in range(lmbd):
        y = x.copy()
        for i in range(n):
            if x[i] != x_mutated[i] and np.random.uniform() < 1 / lmbd:
                flip(y, i)
        f_y = f_noisy(y, q, n)

        if f_y > f_y_crossover:
            y_crossover = y
            f_y_crossover = f_y

    return y_crossover, f_y_crossover


def ollga(n, lmbd, q=1/(6*e)):
    n_iters = 0
    x = np.random.randint(2, size=n)
    f_x = f_noisy(x, q, n)
    while f(x) != n and n_iters < n ** 2:
        x_mutated, _ = mutation(n, lmbd, q, x)
        y, f_y = crossover(n, lmbd, q, x, x_mutated)
        if f_x <= f_y:
            x = y
        n_iters += 1
        f_x = f_noisy(x, q, n)
    return n_iters


def thread_main(thread_id, n_runs=4):
    deg_from = 5
    deg_to = 12
    np.random.seed(thread_id)
    for deg in range(deg_from, deg_to):
        n = 2 ** deg
        for lmbd in [int(log(n) / 2)]:
            with open(f'with_noise_runs/n_{n}_lambda_{lmbd}_thread_{thread_id}.txt', 'w') as f:
                for run_id in range(n_runs):
                    f.write(f'{ollga(n, lmbd)}\n')


if __name__ == '__main__':
    n_threads = 32
    with Pool(n_threads) as p:
        p.map(thread_main, range(n_threads))