from math import log


if __name__ == '__main__':
    n_threads = 32
    n_runs = 4
    deg_from = 5
    deg_to = 11

    for deg in range(deg_from, deg_to):
        n = 2 ** deg
        for lmbd in [int(log(n)), int(n ** (2 / 3))]:
            for thread_id in range(n_threads):
                with open(f'iter_result/n_{n}_lambda_{lmbd}_without_noise.txt', 'w') as output:
                    with open(f'iter/n_{n}_lambda_{lmbd}_thread_{thread_id}.txt', 'r') as input:
                        for run_id in range(n_runs):
                            s = input.readline()
                            output.write(s)