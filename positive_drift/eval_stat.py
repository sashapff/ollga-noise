import re
import numpy as np


def eval_stat(n, cases_num, runs):
    with open(f'fitness_{n}.txt', 'r') as file, \
            open(f'prop_stat_{n}.txt', 'w') as stat_file:
        heads = []
        numpy_data = np.empty((cases_num, 3))
        for case in range(cases_num):
            head = file.readline()
            heads.append(re.sub(r"[\t\n]*", "", head))
            lmbd = int(head.split()[1].split('=')[1])

            good_props = np.empty(runs)
            best_cnt = np.empty(runs)
            best_noisy_values = np.empty(runs)
            best_real_values = np.empty(runs)
            for run in range(runs):
                file.readline()
                fs = np.empty((lmbd, 3), dtype=int)
                for i in range(lmbd):
                    line = file.readline()
                    f_real, f_noisy, is_good = line.split()
                    is_good = True if is_good == 'True' else False
                    f_real = int(f_real)
                    f_noisy = int(f_noisy)
                    fs[i] = (f_real, f_noisy, is_good)

                best_value = np.max(fs[:, 1])
                best_noisy_values[run] = best_value
                best_real_values[run] = np.max(fs[:, 0])
                best = fs[fs[:, 1] == best_value]
                good_best = best[best[:, 2] == 1]
                good_props[run] = good_best.shape[0] / best.shape[0]
                best_cnt[run] = best.shape[0]

            stat_file.write(head)
            stat_file.write(f'Average good_best/best proportion: {np.mean(good_props)}\n')
            stat_file.write(f'Average total best count: {np.mean(best_cnt)}\n')
            stat_file.write(f'Average best noisy fitness: {np.mean(best_noisy_values)}\n\n')
            stat_file.write(f'Average best real fitness: {np.mean(best_real_values)}\n\n')
            numpy_data[case] = (np.mean(good_props), np.mean(best_cnt), np.mean(best_noisy_values))


if __name__ == '__main__':
    cases_num = 4
    runs = 32 * 32
    # df = pd.DataFrame()
    for deg in range(12, 17):
        n = 2 ** deg
        eval_stat(n, cases_num, runs)

