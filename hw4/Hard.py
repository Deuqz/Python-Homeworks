import multiprocessing
import time
from sys import stdin
import codecs


def process_A(a, str_queue):
    while(True):
        str = str_queue.get()
        time.sleep(5)
        a.send(str.lower())


def process_B(b_consumer, b_producer):
    while(True):
        str = b_consumer.recv()
        b_producer.send(codecs.encode(str, "rot-13"))


def main_process():
    str_queue = multiprocessing.Queue()
    b_consumer, a = multiprocessing.Pipe(duplex=False)
    main, b_producer = multiprocessing.Pipe(duplex=False)
    multiprocessing.Process(target=process_A, name="process_A", args=(a, str_queue), daemon=True).start()
    multiprocessing.Process(target=process_B, name="process_B", args=(b_consumer, b_producer), daemon=True).start()
    open("artifacts/Hard_stdin.txt", 'w').close()   # Очищаю файлы, если там что-то было
    open("artifacts/Hard_stdout.txt", 'w').close()
    count = 0
    for str in stdin.readlines():
        with open("artifacts/Hard_stdin.txt", 'a') as f:
            f.write(f"{str[:-1]} | time:{time.time()}\n")
        str_queue.put(str)
        count += 1
    for i in range(count):
        new_str = main.recv()
        with open("artifacts/Hard_stdout.txt", 'a') as f:
            f.write(f"{new_str[:-1]} | time:{time.time()}\n")
        print(new_str, end='')
