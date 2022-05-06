from math import sqrt, floor, ceil, e
import numpy as np
from multiprocessing import Pool


def real_fitness(n, d, lmbd, zeros_flipped):
    ones_flipped = 2 * lmbd - zeros_flipped
    fitness = n - d

    for _ in range(zeros_flipped):
        if np.random.uniform() < 1 / lmbd:
            fitness += 1

    for _ in range(ones_flipped):
        if np.random.uniform() < 1 / lmbd:
            fitness -= 1

    return fitness, n - d < fitness


def noisy_fitness(n, f_real, q):
    fitness = f_real

    for _ in range(f_real):
        if np.random.uniform() < q / n:
            fitness -= 1

    for _ in range(n - f_real):
        if np.random.uniform() < q / n:
            fitness += 1

    return fitness


def simulate(n, d, lmbd, zeros_flipped, q, runs, file):
    file.write(f'd={d}\t lambda={lmbd}\t n={n}\n')
    for run in range(runs):
        file.write(f'run={run}\n')

        for i in range(lmbd):
            f_real, is_good = real_fitness(n, d, lmbd, zeros_flipped)
            f_noisy = noisy_fitness(n, f_real, q)
            file.write(f'{f_real}\t {f_noisy}\t {is_good}\n')


def thread_main(id):
    for deg in range(12, 17):
        n = 2 ** deg
        with open(f'fitness/{n}_{id}.txt', 'w') as file:
            runs = 32
            q = 1 / (6 * e)
            for d in [n // 2, floor(sqrt(n)), 2]:
                for lmbd in [8 * n // d, n // d, floor(sqrt(n)) // d]:
                    if 2 <= lmbd <= ceil(n ** (2 / 3)):
                        zeros_flipped = ceil(lmbd * d / (2 * n))
                        assert d >= zeros_flipped
                        assert n - d >= (2 * lmbd - zeros_flipped)
                        assert 2 * lmbd >= zeros_flipped
                        assert zeros_flipped > 0
                        simulate(n, d, lmbd, zeros_flipped, q, runs, file)


if __name__ == '__main__':
    threads_num = 32
    with Pool(threads_num) as p:
        p.map(thread_main, range(threads_num))
