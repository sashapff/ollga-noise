from math import log
import numpy as np


if __name__ == '__main__':
    n_threads = 32
    n_runs = 4
    deg_from = 6
    deg_to = 7

    for deg in range(deg_from, deg_to):
        n = 2 ** deg
        for lmbd in [int(log(n)), int(n ** (2 / 3))]:
            iters = []
            for thread_id in range(n_threads):
                with open(f'iters/n_{n}_lambda_{lmbd}_thread_{thread_id}.txt', 'r') as f:
                    for run_id in range(n_runs):
                        iters.append(int(f.readline()))
            iters = np.array(iters)
            with open(f'result/n_{n}_lambda_{lmbd}.txt', 'w') as f:
                f.write(f'n: {n}\n')
                f.write(f'lambda: {lmbd}\n')
                f.write(f'Median: {np.median(iters)}\n')
                f.write(f'Mean: {iters.mean()}\n')
                f.write(f'Std: {iters.std()}\n')
                f.write(f'Number of terminated evaluations (iters > n ^ 3): {len(iters[iters == n ** 3])}\n')
                f.write(np.array2string(iters, separator=', '))
