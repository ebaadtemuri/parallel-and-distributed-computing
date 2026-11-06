import socket
import threading
from queue import Queue
from time import perf_counter


HOST = "127.0.0.1"
START_PORT = 1
END_PORT = 1024
MAX_WORKERS = 32
TIMEOUT_SECONDS = 0.1


def scan_worker(port_queue, open_ports, results_lock):
    while True:
        port = port_queue.get()

        try:
            if port is None:
                return

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
                connection.settimeout(TIMEOUT_SECONDS)
                result = connection.connect_ex((HOST, port))

            if result == 0:
                with results_lock:
                    open_ports.append(port)
        except OSError:
            pass
        finally:
            port_queue.task_done()


def main():
    port_queue = Queue()
    for port in range(START_PORT, END_PORT + 1):
        port_queue.put(port)

    open_ports = []
    results_lock = threading.Lock()
    worker_count = min(MAX_WORKERS, END_PORT - START_PORT + 1)

    workers = [
        threading.Thread(
            target=scan_worker,
            args=(port_queue, open_ports, results_lock),
            name=f"scanner-{number}",
        )
        for number in range(worker_count)
    ]

    for _ in workers:
        port_queue.put(None)

    start_time = perf_counter()

    for worker in workers:
        worker.start()

    port_queue.join()

    for worker in workers:
        worker.join()

    elapsed_time = perf_counter() - start_time

    print(f"Scanned localhost ({HOST}), ports {START_PORT}-{END_PORT}")
    if open_ports:
        print("Open TCP ports:", ", ".join(str(port) for port in sorted(open_ports)))
    else:
        print("No open TCP ports found.")

    print(f"Elapsed time: {elapsed_time:.3f} seconds")


if __name__ == "__main__":
    main()
