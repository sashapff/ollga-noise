from math import log
import numpy as np


if __name__ == '__main__':
    n_threads = 32
    n_runs = 4
    deg_from = 4
    deg_to = 8

    for deg in range(deg_from, deg_to):
        # n = 2 ** deg
        n = 110
        iters = []
        for thread_id in range(n_threads):
            with open(f'with_noise_runs/n_{n}_thread_{thread_id}.txt', 'r') as f:
                for run_id in range(n_runs):
                    iters.append(int(f.readline()))
        iters = np.array(iters)
        with open(f'with_noise_result/n_{n}.txt', 'w') as f:
            f.write(f'n: {n}\n')
            f.write(f'Median: {np.median(iters)}\n')
            f.write(f'Mean: {iters.mean()}\n')
            f.write(f'Std: {iters.std()}\n')
            f.write(f'Number of terminated evaluations (iters > n ^ 3): {len(iters[iters == n ** 3])}\n')
            f.write(np.array2string(iters, separator=', '))
