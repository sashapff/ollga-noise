from math import log
import numpy as np
from matplotlib import pyplot as plt


def get(n, n_threads, n_runs):
    iters_noise = []
    iters_without_noise = []
    for thread_id in range(n_threads):
        with open(f'with_noise_runs/n_{n}_thread_{thread_id}.txt', 'r') as f:
            with open(f'without_noise_runs/n_{n}_thread_{thread_id}.txt', 'r') as f2:
                for run_id in range(n_runs):
                    iters_noise.append(int(f.readline()))
                    iters_without_noise.append(int(f2.readline()))
    iters_noise = np.array(iters_noise)
    iters_without_noise = np.array(iters_without_noise)

    return iters_noise, iters_without_noise


if __name__ == '__main__':
    n_threads = 32
    n_runs = 4
    deg_from = 4
    deg_to = 7

    plt.title('Number of iterations to find the optimum, (1+1) EA')

    n_iters_noise = []
    n_iters_without_noise = []

    points = []

    for deg in range(deg_from, deg_to):
        n = 2 ** deg
        iters_noise, iters_without_noise = get(n, n_threads, n_runs)

        n_iters_noise.append(iters_noise.mean())
        n_iters_without_noise.append(iters_without_noise.mean())

        # plt.errorbar(n, iters_noise.mean(),
        #              [[iters_noise.mean() - iters_noise.min()],
        #                                          [iters_noise.max() - iters_noise.mean()]],
        #                  color='tab:red', capsize=3)
        # plt.errorbar(n, iters_without_noise.mean(),
        #                  [[iters_without_noise.mean() - iters_without_noise.min()],
        #                   [iters_without_noise.max() - iters_without_noise.mean()]],
        #                  color='black', capsize=3)

        plt.errorbar(n, iters_noise.mean(),
                     [[np.quantile(iters_noise, 0.025)],
                      [np.quantile(iters_noise, 0.975)]],
                     color='tab:red', capsize=3)

        plt.errorbar(n, iters_without_noise.mean(),
                     [[np.quantile(iters_without_noise, 0.025)],
                      [np.quantile(iters_without_noise, 0.975)]],
                         color='black', capsize=3)

        points.append(n)

    plt.plot(points, n_iters_noise, label='With noise', color='tab:red')
    plt.plot(points, n_iters_without_noise, label='Without noise', color='black')
    plt.legend()
    plt.xlabel('n')
    plt.ylabel('iterations')
    plt.savefig('plots/one_plus_one.png')
