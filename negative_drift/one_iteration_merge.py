from math import log
import numpy as np
from matplotlib import pyplot as plt


if __name__ == '__main__':
    n_threads = 32
    n_runs = 32
    deg_from = 5
    deg_to = 11

    d_plot_name = '3n/4'
    d_file_name = '3n_div_4'

    n_range = []
    logn_bad_winner = []
    logn_good_winner = []
    sqrtn_bad_winner = []
    sqrtn_good_winner = []
    n23_bad_winner = []
    n23_good_winner = []

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
        logn_n_good_winner = []
        logn_winer = []

        sqrtn_n_bad_winner = []
        sqrtn_n_good_winner = []
        sqrtn_winer = []

        n23_n_bad_winner = []
        n23_n_good_winner = []
        n23_winer = []

        for lmbd in [int(log(n)), int(n ** (2 / 3)), int(np.sqrt(n))]:
            with open(f'result/{d_file_name}_n_{n}_lambda_{lmbd}.txt', 'w') as output:
                for thread_id in range(n_threads):
                    with open(f'runs/{d_file_name}_n_{n}_lambda_{lmbd}_thread_{thread_id}.txt', 'r') as input:
                        for run_id in range(n_runs):
                            for _ in range(5):
                                s = input.readline()
                                output.write(s)

                            s = input.readline()
                            bad_prob = int(s.split(':')[1])
                            output.write(s)

                            s = input.readline()
                            good_prob = int(s.split(':')[1])
                            output.write(s)

                            s = input.readline()
                            f_best_good = float(s.split(':')[1])
                            output.write(s)

                            s = input.readline()
                            f_noisy_best_good = float(s.split(':')[1])
                            output.write(s)

                            s = input.readline()
                            f_best_bad = float(s.split(':')[1])
                            output.write(s)

                            s = input.readline()
                            f_noisy_best_bad = float(s.split(':')[1])
                            output.write(s)

                            if lmbd == int(log(n)):
                                logn_n_bad_winner.append(bad_prob)
                                logn_n_good_winner.append(good_prob)
                                logn_winer.append([f_best_good, f_noisy_best_good, f_best_bad, f_noisy_best_bad])
                            elif lmbd == int(np.sqrt(n)):
                                sqrtn_n_bad_winner.append(bad_prob)
                                sqrtn_n_good_winner.append(good_prob)
                                sqrtn_winer.append([f_best_good, f_noisy_best_good, f_best_bad, f_noisy_best_bad])
                            else:
                                n23_n_bad_winner.append(bad_prob)
                                n23_n_good_winner.append(good_prob)
                                n23_winer.append([f_best_good, f_noisy_best_good, f_best_bad, f_noisy_best_bad])

                            for _ in range(1):
                                s = input.readline()
                                output.write(s)

        logn_n_bad_winner = np.array(logn_n_bad_winner)
        logn_n_good_winner = np.array(logn_n_good_winner)
        logn_bad_winner.append(logn_n_bad_winner.mean())
        logn_good_winner.append(logn_n_good_winner.mean())

        logn_winer = np.array(logn_winer)
        logn_real_good.append(logn_winer[:, 0].mean())
        logn_noisy_good.append(logn_winer[:, 1].mean())
        logn_real_bad.append(logn_winer[:, 2].mean())
        logn_noisy_bad.append(logn_winer[:, 3].mean())

        sqrtn_n_bad_winner = np.array(sqrtn_n_bad_winner)
        sqrtn_n_good_winner = np.array(sqrtn_n_good_winner)
        sqrtn_bad_winner.append(sqrtn_n_bad_winner.mean())
        sqrtn_good_winner.append(sqrtn_n_good_winner.mean())

        n23_n_bad_winner = np.array(n23_n_bad_winner)
        n23_n_good_winner = np.array(n23_n_good_winner)
        n23_bad_winner.append(n23_n_bad_winner.mean())
        n23_good_winner.append(n23_n_good_winner.mean())


    # plt.title(f'Mean fitness, lambda=log(n), d={d_plot_name}, 1024 runs')
    # plt.plot(n_range, logn_real_good, label=f'read good')
    # plt.plot(n_range, logn_noisy_good, label=f'noisy good')
    # plt.plot(n_range, logn_real_bad, label=f'read bad')
    # plt.plot(n_range, logn_noisy_bad, label=f'noisy bad')
    # plt.legend()
    # plt.xlabel('n')
    # plt.ylabel('mean fitness')
    # plt.savefig(f'plot/{d_file_name}_lambda_log(n)_count.png')

    plt.clf()
    plt.title(f'Probability that bad individual wins crossover, fitness={d_plot_name}, 1024 runs')
    plt.plot(n_range, logn_good_winner, label=f'positive, lambda=log(n)', color='blue')
    plt.plot(n_range, logn_bad_winner, label=f'negative, lambda=log(n)', color='darkblue')
    plt.plot(n_range, sqrtn_good_winner, label=f'positive, lambda=sqrt(n)', color='red')
    plt.plot(n_range, sqrtn_bad_winner, label=f'negative, lambda=sqrt(n)', color='darkred')
    plt.plot(n_range, n23_good_winner, label=f'positive, lambda=n^(2/3)', color='green')
    plt.plot(n_range, n23_bad_winner, label=f'negative, lambda=n^(2/3)', color='darkgreen')
    plt.legend()
    # plt.yscale('log')
    plt.xlabel('n')
    plt.ylabel('p, probability')
    plt.savefig(f'plot/{d_file_name}_prob.png')
