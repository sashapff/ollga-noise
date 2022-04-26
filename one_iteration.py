from math import e, log, ceil, sqrt
from multiprocessing import Pool
import numpy as np


def flip(x, i):
    x[i] = (x[i] + 1) % 2


def f(x):
    return x.sum()


def f_noisy(x, q, n):
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

    return x_mutated, f_x_mutated, l


def crossover(n, lmbd, q, x, x_mutated):
    y_crossover = x.copy()
    f_y_crossover = -1
    offspring_fs = []
    offspring_fs_noisy = []
    for _ in range(lmbd):
        y = x.copy()
        for i in range(n):
            if x[i] != x_mutated[i] and np.random.uniform() < 1 / lmbd:
                flip(y, i)
        f_y = f_noisy(y, q, n)

        offspring_fs.append(f(y))
        offspring_fs_noisy.append(f_y)

        if f_y > f_y_crossover:
            y_crossover = y
            f_y_crossover = f_y

    return y_crossover, f_y_crossover, offspring_fs, offspring_fs_noisy


def run_iter(n, lmbd, q=1/(6*e)):
    x = np.zeros(n)
    x[:int(n / 2)] = 1

    x_mutated, f_x_mutated, l = mutation(n, lmbd, q, x)
    y, f_y, offspring_fs, offspring_fs_noisy = crossover(n, lmbd, q, x, x_mutated)

    return l, f_x_mutated, offspring_fs, offspring_fs_noisy


def thread_main(thread_id, n_runs=4):
    deg_from = 5
    deg_to = 11
    for deg in range(deg_from, deg_to):
        n = 2 ** deg
        for lmbd in [int(log(n)), int(n ** (2 / 3)), int(sqrt(n))]:
            with open(f'iter_runs/n_{n}_lambda_{lmbd}_thread_{thread_id}.txt', 'w') as f:
                for run_id in range(n_runs):
                    l, f_x_mutated, offspring_fs, offspring_fs_noisy = run_iter(n, lmbd)
                    f.write(f'l: {l}\n')
                    f.write(f'Fitness of mutation winner: {f_x_mutated}\n')
                    f.write(f'Crossover offspring real fitness: {offspring_fs}\n')
                    f.write(f'Crossover offspring noisy fitness: {offspring_fs_noisy}\n')
                    f.write(f'\n')


if __name__ == '__main__':
    n_threads = 32
    with Pool(n_threads) as p:
        p.map(thread_main, range(n_threads))