import math
import multiprocessing
import time
import concurrent.futures as pool


def integrate_part(f, a, b, n_iter):
    start = time.time()
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc, (start, a, b)


def integrate_processes(f, a, b, *, n_jobs=1, n_iter=1000):
    start = time.time()
    n_iter = int(n_iter / n_jobs)
    step = (b - a) / n_jobs
    acc = 0
    log = []
    with pool.ProcessPoolExecutor(max_workers=n_jobs) as executor:
        futures = [executor.submit(integrate_part, f, a + i * step, a + (i + 1) * step, n_iter)
                   for i in range(n_jobs)]
        for future in pool.as_completed(futures):
            result = future.result()
            acc += result[0]
            log.append(result[1])
    time_prog = time.time() - start
    with open("artifacts/MediumLogsProcesses.txt", 'a') as f:
        f.write(f"start work: n_jobs={n_jobs}, start={start}\n")
        for elem in log:
            f.write(f"  integration [{elem[1]}, {elem[2]}] starts in {elem[0]}\n")
    return acc, time_prog


def integrate_threads(f, a, b, *, n_jobs=1, n_iter=1000):
    start = time.time()
    n_iter = int(n_iter / n_jobs)
    step = (b - a) / n_jobs
    acc = 0
    log = []
    with pool.ThreadPoolExecutor(max_workers=n_jobs) as executor:
        futures = [executor.submit(integrate_part, f, a + i * step, a + (i + 1) * step, n_iter)
                   for i in range(n_jobs)]
        for future in pool.as_completed(futures):
            result = future.result()
            acc += result[0]
            log.append(result[1])
    time_prog = time.time() - start
    with open("artifacts/MediumLogsThreads.txt", 'a') as f:
        f.write(f"start work: n_jobs={n_jobs}, start={start}\n")
        for elem in log:
            f.write(f"  integration [{elem[1]}, {elem[2]}] starts in {elem[0]}\n")
    return acc, time_prog


def run():
    open("artifacts/MediumComparisonProcesses.txt", 'w').close()
    open("artifacts/MediumComparisonThreads.txt", 'w').close()
    open("artifacts/MediumLogsThreads.txt", 'w').close()
    open("artifacts/MediumLogsProcesses.txt", 'w').close()
    for n_jobs in range(1, 2 * multiprocessing.cpu_count()):
        res = integrate_threads(math.cos, 0, math.pi / 2, n_jobs=n_jobs, n_iter=1000000)
        with open("artifacts/MediumComparisonThreads.txt", 'a') as f:
            f.write(f"n_jobs={n_jobs} works {res[1]}\n")
    for n_jobs in range(1, 2 * multiprocessing.cpu_count()):
        res = integrate_processes(math.cos, 0, math.pi / 2, n_jobs=n_jobs, n_iter=1000000)
        with open("artifacts/MediumComparisonProcesses.txt", 'a') as f:
            f.write(f"n_jobs={n_jobs} works {res[1]}\n")