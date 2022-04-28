from math import log
import numpy as np
from matplotlib import pyplot as plt


def get(n, lmbd, n_threads, n_runs):
    iters_noise = []
    iters_without_noise = []
    for thread_id in range(n_threads):
        with open(f'with_noise_runs/n_{n}_lambda_{lmbd}_thread_{thread_id}.txt', 'r') as f:
            with open(f'without_noise_runs/n_{n}_lambda_{lmbd}_thread_{thread_id}.txt', 'r') as f2:
                for run_id in range(n_runs):
                    iters_noise.append(int(f.readline()))
                    iters_without_noise.append(int(f2.readline()))
    iters_noise = np.array(iters_noise)
    iters_without_noise = np.array(iters_without_noise)

    return iters_noise, iters_without_noise


if __name__ == '__main__':
    n_threads = 32
    n_runs = 4
    deg_from = 5
    deg_to = 12

    plt.title('Number of iterations to find the optimum, lambda=ln(n)')

    n_iters_noise_ln = []
    n_iters_without_noise_ln = []
    n_iters_noise_23 = []
    n_iters_without_noise_23 = []

    points = []

    for deg in range(deg_from, deg_to):
        n = 2 ** deg
        for lmbd in [int(log(n)), int(n ** (2 / 3))]:
            if lmbd == int(log(n)):
                iters_noise_ln, iters_without_noise_ln = get(n, lmbd, n_threads, n_runs)

                n_iters_noise_ln.append(iters_noise_ln.mean())
                n_iters_without_noise_ln.append(iters_without_noise_ln.mean())

                # plt.errorbar(n, iters_noise_ln.mean(), [[iters_noise_ln.mean() - iters_noise_ln.min()],
                #                                         [iters_noise_ln.max() - iters_noise_ln.mean()]],
                #              color='tab:red', capsize=3)
                # plt.errorbar(n, iters_without_noise_ln.mean(),
                #              [[iters_without_noise_ln.mean() - iters_without_noise_ln.min()],
                #               [iters_without_noise_ln.max() - iters_without_noise_ln.mean()]],
                #              color='black', capsize=3)

            else:
                iters_noise_23, iters_without_noise_23 = get(n, lmbd, n_threads, n_runs)

                n_iters_noise_23.append(iters_noise_23.mean())
                n_iters_without_noise_23.append(iters_without_noise_23.mean())

                plt.errorbar(n, iters_noise_23.mean(), [[iters_noise_23.mean() - iters_noise_23.min()],
                                                        [iters_noise_23.max() - iters_noise_23.mean()]],
                             color='tab:red', capsize=3)
                plt.errorbar(n, iters_without_noise_23.mean(),
                             [[iters_without_noise_23.mean() - iters_without_noise_23.min()],
                              [iters_without_noise_23.max() - iters_without_noise_23.mean()]],
                             color='black', capsize=3)

        points.append(n)

    # plt.plot(points, n_iters_noise_ln, label='With noise', color='tab:red')
    # plt.plot(points, n_iters_without_noise_ln, label='Without noise', color='black')
    plt.plot(points, n_iters_noise_23, label='With noise', color='tab:red')
    plt.plot(points, n_iters_without_noise_23, label='Without noise', color='black')
    plt.legend()
    plt.xlabel('n')
    plt.ylabel('iterations')
    plt.show()
