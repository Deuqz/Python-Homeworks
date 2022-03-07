import concurrent.futures
import multiprocessing as mp
import time


N = 200000
times = 10


def fib(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 0
    else:
        res = (0, 1)
        for i in range(n - 2):
            res = (res[1], res[0] + res[1])
        return res[1]


def check_synch_fib():
    start = time.time()
    for i in range(times):
        x = fib(N)
    finish = time.time()
    with open("artifacts/Easy.txt", "a") as f:
        f.write(f"Synchronously: {str(finish - start)}\n")


def check_treading_fib():
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(times):
            executor.submit(fib, N)
    finish = time.time()
    with open("artifacts/Easy.txt", "a") as f:
        f.write(f"Threading: {str(finish - start)}\n")


def check_multiprocessing_fib():
    processes = []
    for i in range(times):
        processes.append(mp.Process(target=fib, args=(N,)))
    start = time.time()
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    finish = time.time()
    with open("artifacts/Easy.txt", "a") as f:
        f.write(f"Multiprocessing: {str(finish - start)}\n")


def run():
    check_synch_fib()
    check_treading_fib()
    check_multiprocessing_fib()