from math import log


if __name__ == '__main__':
    n_threads = 32
    n_runs = 4
    deg_from = 5
    deg_to = 11

    for deg in range(deg_from, deg_to):
        n = 2 ** deg
        for lmbd in [int(log(n)), int(n ** (2 / 3))]:
            with open(f'iter_result/n_{n}_lambda_{lmbd}.txt', 'w') as output:
                for thread_id in range(n_threads):
                    with open(f'iter_runs/n_{n}_lambda_{lmbd}_thread_{thread_id}.txt', 'r') as input:
                        for run_id in range(n_runs):
                            for _ in range(5):
                                s = input.readline()
                                output.write(s)