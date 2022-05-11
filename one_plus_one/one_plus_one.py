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


def mutation(n, x, q):
    y = x.copy()
    for i in range(n):
        if np.random.uniform() < 1 / n:
            flip(y, i)
    f_y = f_noisy(y, q, n)
    return y, f_y


def opo(n, q=1/(6*e)):
    n_iters = 0
    x = np.random.randint(2, size=n)
    f_x = f_noisy(x, q, n)
    while f(x) != n and n_iters < n ** 3:
        x_mutated, f_x_mutated = mutation(n, x, q)
        if f_x <= f_x_mutated:
            x = x_mutated
        n_iters += 1
        f_x = f_noisy(x, q, n)
    return n_iters


def thread_main(thread_id, n_runs=4):
    deg_from = 5
    deg_to = 11
    np.random.seed(thread_id)
    for deg in range(deg_from, deg_to):
        n = 2 ** deg
        with open(f'with_noise_runs/n_{n}_thread_{thread_id}.txt', 'w') as f:
            for run_id in range(n_runs):
                f.write(f'{opo(n)}\n')


if __name__ == '__main__':
    n_threads = 32
    with Pool(n_threads) as p:
        p.map(thread_main, range(n_threads))