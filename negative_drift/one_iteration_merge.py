from math import log
import numpy as np
from matplotlib import pyplot as plt


if __name__ == '__main__':
    n_threads = 32
    n_runs = 32
    deg_from = 5
    deg_to = 11

    d_name = 'n/2'

    n_range = []
    logn_bad_winner = []
    sqrtn_bad_winner = []
    n23_bad_winner = []

    logn_real_good = []
    logn_noisy_good = []
    logn_real_bad = []
    logn_noisy_bad = []

    sqrtn_real_good = []
    sqrtn_noisy_good = []
    sqrtn_real_bad = []
    sqrtn_noisy_bad = []

    n23_real_good = []
    n23_noisy_good = []
    n23_real_bad = []
    n23_noisy_bad = []

    for deg in range(deg_from, deg_to):
        n = 2 ** deg
        n_range.append(n)

        logn_n_bad_winner = []
        logn_winer = []

        sqrtn_n_bad_winner = []
        sqrtn_winer = []

        n23_n_bad_winner = []
        n23_winer = []

        for lmbd in [int(log(n)), int(n ** (2 / 3)), int(np.sqrt(n))]:
            with open(f'../iter_result/n_{n}_lambda_{lmbd}.txt', 'w') as output:
                for thread_id in range(n_threads):
                    with open(f'../iter_runs/n_div_2_n_{n}_lambda_{lmbd}_thread_{thread_id}.txt', 'r') as input:
                        for run_id in range(n_runs):
                            for _ in range(5):
                                s = input.readline()
                                output.write(s)

                            prob = int(input.readline().split(':')[1])
                            f_best_good = float(input.readline().split(':')[1])
                            f_noisy_best_good = float(input.readline().split(':')[1])
                            f_best_bad = float(input.readline().split(':')[1])
                            f_noisy_best_bad = float(input.readline().split(':')[1])

                            if lmbd == int(log(n)):
                                logn_n_bad_winner.append(prob)
                                logn_winer.append([f_best_good, f_noisy_best_good, f_best_bad, f_noisy_best_bad])
                            elif lmbd == int(np.sqrt(n)):
                                sqrtn_n_bad_winner.append(prob)
                                sqrtn_winer.append([f_best_good, f_noisy_best_good, f_best_bad, f_noisy_best_bad])
                            else:
                                n23_n_bad_winner.append(prob)
                                n23_winer.append([f_best_good, f_noisy_best_good, f_best_bad, f_noisy_best_bad])

                            for _ in range(1):
                                s = input.readline()

        logn_n_bad_winner = np.array(logn_n_bad_winner)
        logn_bad_winner.append(logn_n_bad_winner.mean())

        logn_winer = np.array(logn_winer)
        logn_real_good.append(logn_winer[:, 0].mean())
        logn_noisy_good.append(logn_winer[:, 1].mean())
        logn_real_bad.append(logn_winer[:, 2].mean())
        logn_noisy_bad.append(logn_winer[:, 3].mean())

        sqrtn_n_bad_winner = np.array(sqrtn_n_bad_winner)
        sqrtn_bad_winner.append(sqrtn_n_bad_winner.mean())

        n23_n_bad_winner = np.array(n23_n_bad_winner)
        n23_bad_winner.append(n23_n_bad_winner.mean())


    plt.title(f'Mean fitness, lambda=log(n), d={d_name}, 1024 runs')
    plt.plot(n_range, logn_real_good, label=f'read good')
    plt.plot(n_range, logn_noisy_good, label=f'noisy good')
    plt.plot(n_range, logn_real_bad, label=f'read bad')
    plt.plot(n_range, logn_noisy_bad, label=f'noisy bad')
    plt.legend()
    plt.xlabel('n')
    plt.ylabel('mean fitness')
    plt.show()


    plt.title(f'Probability that bad individual wins crossover, d={d_name}, 1024 runs')
    plt.plot(n_range, logn_bad_winner, label=f'lambda=log(n)')
    plt.plot(n_range, sqrtn_bad_winner, label=f'lambda=sqrt(n)')
    plt.plot(n_range, n23_bad_winner, label=f'lambda=n^(2/3)')
    plt.legend()
    plt.yscale('log')
    plt.xlabel('n')
    plt.ylabel('p, probability')
    plt.show()
