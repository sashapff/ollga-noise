def merge_fitness(n, threads_num, cases_num):
    runs = 32
    with open(f'fitness_{n}.txt', 'w') as final_file:
        heads = []
        values = [[['' for _ in range(runs)] for _ in range(threads_num)] for _ in range(cases_num)]

        for id in range(threads_num):
            with open(f'fitness/{n}_{id}.txt', 'r') as file:
                for case in range(cases_num):
                    head = file.readline()
                    lmbd = int(head.split()[1].split('=')[1])
                    if id == 0:
                        heads.append(head)
                    for run in range(runs):
                        file.readline()
                        for _ in range(lmbd):
                            line = file.readline()
                            values[case][id][run] += line

        for case in range(cases_num):
            final_file.write(heads[case])
            for id in range(threads_num):
                for run in range(runs):
                    final_file.write(f'run={id * 32 + run}\n')
                    final_file.write(values[case][id][run])


if __name__ == '__main__':
    threads_num = 32
    cases_num = 4
    for deg in range(12, 17):
        n = 2 ** deg
        merge_fitness(n, threads_num, cases_num)
