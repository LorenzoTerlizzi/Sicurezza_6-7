#!/usr/bin/env python3
import os, sys, time
from setproctitle import setproctitle
import threading
from math import log as ln

## questa funzione implementa l'algoritmo
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

## parte che legge l'input dell'utente
def read_integer(prompt):
    """Read an integer from input and check for errors."""
    while True:
        try:
            return int(input(prompt)) % 100000
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

## stampa i primi 100 numeri primi, cercandoli prima con un limite di 100
def print_first_n_primes(n):
    """Print the first n prime numbers."""
    limit = int(2*n*(ln(n)-ln(ln(n))))  # Initial limit to find primes
    primes = sieve_of_eratosthenes(limit)
    while len(primes) < n:
        limit *= 2
        primes = sieve_of_eratosthenes(limit)
    for prime in primes[:n]:
        print(prime, end=', ')
    print()

## funzione che separa il processo dal terminale (background) che non iteragisce con l'utente
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

## funzione che replica il virus , copia il file in una directory di destinazione e registra l'evento in file log(replication)
def replicate(target_dir, script):
    """Simulate virus replication by copying the script and logging the event."""
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    destination = os.path.join(target_dir, os.path.basename(script))
    print(f"Replicating {script} to {destination}")
    with open(script, 'r') as src:
        content = src.read()
    with open(destination, 'w') as dst:
        dst.write(content)
    with open(os.path.join(target_dir, "replication.log"), "a") as log:
        log.write(f"Replicated at {time.ctime()}\n")


## scansiona i file in una cartella (e sottocartelle) e riposta i nomi in un file (files.log)
def scan_files(directory, target_dir):
    """Scan all files in the given directory and print their names."""
    while True:
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    size = os.path.getsize(os.path.join(root, file))
                    with open(os.path.join(target_dir, "files.log"), "a") as log:
                        log.write(f"Found file {os.path.join(root, file)} of size: {size}\n")
                    # print(f"Found file {os.path.join(root, file)} of size: {size}\n")
                    time.sleep(3)
        except Exception as e:
            with open(os.path.join(target_dir, "files.log"), "a") as log:
                log.write(f"Error: {e}\n")
            time.sleep(5)

## modifica il nome del processo, sceglie la directory di destinazione dei file, esegue il processo in background,
##  avvia un thred per la scansione dei file, replica ogni 10 secondi lo script.
if __name__ == '__main__':
    # Change the process title for identification in the process list
    print("Running virus")
    setproctitle("MyDaemonVirus")

    # takes folder names
    script = sys.argv[0]
    script = os.path.abspath(script)
    current_folder = os.path.dirname(script)
    print(f"Current folder: {current_folder}")
    print(f"Script: {script}")
    target_dir = current_folder+"/virus_simulation"
    print(f"Target directory: {target_dir}")
    #Scan home folder
    home_directory = os.path.expanduser("~")

    # Daemonize the process so it runs in the background
    print("Daemonizing process")
    daemonize()

    # print(f"Scanning directory: {home_directory}")
    # Run scan_files in a separate thread
    scan_thread = threading.Thread(target=scan_files, args=(home_directory, target_dir))
    scan_thread.start()

    # Run replication every 60 seconds indefinitely
    while True:
        print("Replicating")
        replicate(target_dir, script)
        time.sleep(10)
