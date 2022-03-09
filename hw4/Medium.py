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
    return acc, f"  integrate [{a}, {b}] starts in {start}\n"


def integrate_processes(f, a, b, *, n_jobs=1, n_iter=1000):
    n_iter = int(n_iter / n_jobs)
    step = (b - a) / n_jobs
    acc = 0
    log = f"start work: n_jobs={n_jobs}, start={time.time()}\n"
    with pool.ProcessPoolExecutor(max_workers=n_jobs) as executor:
        futures = [executor.submit(integrate_part, f, a + i * step, a + (i + 1) * step, n_iter)
                   for i in range(n_jobs)]
        for future in pool.as_completed(futures):
            result = future.result()
            acc += result[0]
            log += result[1]
    with open("artifacts/MediumLogsProcesses.txt", 'a') as f:
        f.write(f"{log}\n")
    return acc


def integrate_threads(f, a, b, *, n_jobs=1, n_iter=1000):
    n_iter = int(n_iter / n_jobs)
    step = (b - a) / n_jobs
    acc = 0
    log = f"start work: n_jobs={n_jobs}, start={time.time()}\n"
    with pool.ThreadPoolExecutor(max_workers=n_jobs) as executor:
        futures = [executor.submit(integrate_part, f, a + i * step, a + (i + 1) * step, n_iter)
                   for i in range(n_jobs)]
        for future in pool.as_completed(futures):
            result = future.result()
            acc += result[0]
            log += result[1]
    with open("artifacts/MediumLogsThreads.txt", 'a') as f:
        f.write(f"{log}\n")
    return acc


def run():
    for n_jobs in range(1, 2 * multiprocessing.cpu_count()):
        start = time.time()
        integrate_threads(math.cos, 0, math.pi / 2, n_jobs=n_jobs)
        with open("artifacts/MediumComparisonThreads.txt", 'a') as f:
            f.write(f"n_jobs={n_jobs} works {time.time() - start}\n")
    for n_jobs in range(1, 2 * multiprocessing.cpu_count()):
        start = time.time()
        integrate_processes(math.cos, 0, math.pi / 2, n_jobs=n_jobs)
        with open("artifacts/MediumComparisonProcesses.txt", 'a') as f:
            f.write(f"n_jobs={n_jobs} works {time.time() - start}\n")