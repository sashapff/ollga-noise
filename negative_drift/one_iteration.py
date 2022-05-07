from math import e, log, sqrt
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
    f_best_good = -1
    f_noisy_best_good = -1
    f_best_bad = -1
    f_noisy_best_bad = -1
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

        is_good = f(y) >= f(x)

        if is_good:
            if f_y > f_noisy_best_good:
                f_noisy_best_good = f_y
                f_best_good = f(y)
            if f_y == f_noisy_best_good:
                f_best_good = max(f(y), f_best_good)
        else:
            if f_y > f_noisy_best_bad:
                f_noisy_best_bad = f_y
                f_best_bad = f(y)
            if f_y == f_noisy_best_bad:
                f_best_bad = max(f(y), f_best_bad)

    return y_crossover, f_y_crossover, offspring_fs, offspring_fs_noisy, f_best_good, f_noisy_best_good, f_best_bad, f_noisy_best_bad


def run_iter(n, lmbd, n_ones, q=1/(6*e)):
    x = np.zeros(n)
    x[:n_ones] = 1

    x_mutated, f_x_mutated, l = mutation(n, lmbd, q, x)
    y, f_y, offspring_fs, offspring_fs_noisy, f_best_good, f_noisy_best_good, f_best_bad, f_noisy_best_bad = crossover(n, lmbd, q, x, x_mutated)
    is_bad_winner = 1 if f(y) < f(x) else 0
    is_good_winner = 1 if f(y) > f(x) else 0

    return l, f(x_mutated), f_x_mutated, offspring_fs, offspring_fs_noisy, is_bad_winner, is_good_winner, f_best_good, f_noisy_best_good, f_best_bad, f_noisy_best_bad


def thread_main(thread_id, n_runs=32):
    np.random.seed(thread_id)
    deg_from = 5
    deg_to = 11
    for deg in range(deg_from, deg_to):
        n = 2 ** deg

        d_file_name = '3n_div_4'
        n_ones = int(3 * n / 4)

        for lmbd in [int(log(n)), int(n ** (2 / 3)), int(sqrt(n))]:
            with open(f'runs/{d_file_name}_n_{n}_lambda_{lmbd}_thread_{thread_id}.txt', 'w') as f:
                for run_id in range(n_runs):
                    l, f_x, f_x_mutated, offspring_fs, offspring_fs_noisy, is_bad_winner, is_good_winner, f_best_good, f_noisy_best_good, f_best_bad, f_noisy_best_bad = run_iter(n, lmbd, n_ones)
                    f.write(f'l: {l}\n')
                    f.write(f'Real fitness of mutation winner: {f_x}\n')
                    f.write(f'Noisy fitness of mutation winner: {f_x_mutated}\n')
                    f.write(f'Crossover offspring real fitness: {offspring_fs}\n')
                    f.write(f'Crossover offspring noisy fitness: {offspring_fs_noisy}\n')
                    f.write(f'Is bad individual winner: {is_bad_winner}\n')
                    f.write(f'Is good individual winner: {is_good_winner}\n')
                    f.write(f'Real fitness of best good: {f_best_good}\n')
                    f.write(f'Noisy fitness of best good: {f_noisy_best_good}\n')
                    f.write(f'Real fitness of best bad: {f_best_bad}\n')
                    f.write(f'Noisy fitness of best bad: {f_noisy_best_bad}\n')
                    f.write(f'\n')


if __name__ == '__main__':
    n_threads = 32
    with Pool(n_threads) as p:
        p.map(thread_main, range(n_threads))