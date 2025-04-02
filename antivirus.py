
# import psutil
# import time

# def get_current_processes():
#     """
#     Raccoglie i processi attualmente in esecuzione.
#     Restituisce un dizionario con chiave: PID e valore: nome del processo.
#     """
#     processes = {}
#     for proc in psutil.process_iter(['pid', 'name']):
#         try:
#             processes[proc.info['pid']] = proc.info['name']
#         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#             continue
#     return processes

# def monitor_new_processes(interval=5):
#     """
#     Monitora continuamente i processi confrontandoli con una baseline iniziale.
#     Se vengono rilevati nuovi processi, li visualizza con un numero identificativo e chiede all'utente se desidera terminare uno o più processi.
#     """
#     print("Acquisizione della lista iniziale dei processi...")
#     baseline = get_current_processes()
#     print("Baseline acquisita.\n")
    
#     while True:
#         time.sleep(interval)
#         current = get_current_processes()
#         # Individua i processi che non erano presenti nella baseline
#         new_processes = {pid: name for pid, name in current.items() if pid not in baseline}
#         if new_processes:
#             print("\nNuovi processi rilevati:")
#             # Crea una lista numerata dei nuovi processi
#             new_process_list = list(new_processes.items())
#             for index, (pid, name) in enumerate(new_process_list, start=1):
#                 print(f"{index}. PID: {pid}, Nome: {name}")
            
#             # Chiede all'utente se desidera terminare uno o più processi
#             user_input = input("\nInserisci i numeri dei processi da terminare separati da virgola (o premi invio per ignorare): ")
#             if user_input.strip():
#                 # Analizza l'input separato da virgola
#                 selections = user_input.split(',')
#                 for selection in selections:
#                     try:
#                         num = int(selection.strip())
#                         if 1 <= num <= len(new_process_list):
#                             pid_to_kill, process_name = new_process_list[num-1]
#                             try:
#                                 proc = psutil.Process(pid_to_kill)
#                                 proc.kill()
#                                 print(f"Processo '{process_name}' (PID: {pid_to_kill}) terminato.")
#                             except Exception as e:
#                                 print(f"Errore nel terminare il processo '{process_name}' (PID: {pid_to_kill}): {e}")
#                         else:
#                             print(f"Numero '{num}' non valido.")
#                     except ValueError:
#                         print(f"Input '{selection.strip()}' non valido. Inserisci numeri interi.")
#             else:
#                 print("Nessuna azione intrapresa.")
            
#             # Aggiorna la baseline con i nuovi processi per evitare ripetizioni nelle iterazioni successive
#             baseline.update(new_processes)
#         else:
#             print("Nessun nuovo processo rilevato.")

# if __name__ == '__main__':
#     monitor_new_processes()
import os
import psutil
import time

def get_current_processes():
    """
    Raccoglie i processi attualmente in esecuzione.
    Restituisce un dizionario con chiave: PID e valore: nome del processo.
    """
    processes = {}
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            processes[proc.info['pid']] = proc.info['name']
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return processes

def search_folder(start_dir, target_folder="virus_simulation"):
    """
    Cerca ricorsivamente la cartella target_folder a partire dalla directory start_dir.
    Restituisce una lista di percorsi in cui è stata trovata la cartella.
    """
    matches = []
    for root, dirs, files in os.walk(start_dir):
        if target_folder in dirs:
            matches.append(os.path.join(root, target_folder))
    return matches

def monitor_new_processes(interval=5):
    """
    Monitora continuamente i processi confrontandoli con una baseline iniziale.
    Se vengono rilevati nuovi processi, li visualizza con un numero identificativo e chiede all'utente se desidera terminare uno o più processi.
    """
    print("Acquisizione della lista iniziale dei processi...")
    baseline = get_current_processes()
    print("Baseline acquisita.\n")
    
    while True:
        time.sleep(interval)
        current = get_current_processes()
        # Individua i processi che non erano presenti nella baseline
        new_processes = {pid: name for pid, name in current.items() if pid not in baseline}
        if new_processes:
            print("\nNuovi processi rilevati:")
            # Crea una lista numerata dei nuovi processi
            new_process_list = list(new_processes.items())
            for index, (pid, name) in enumerate(new_process_list, start=1):
                print(f"{index}. PID: {pid}, Nome: {name}")
            
            # Chiede all'utente se desidera terminare uno o più processi
            user_input = input("\nInserisci i numeri dei processi da terminare separati da virgola (o premi invio per ignorare): ")
            if user_input.strip():
                # Analizza l'input separato da virgola
                selections = user_input.split(',')
                for selection in selections:
                    try:
                        num = int(selection.strip())
                        if 1 <= num <= len(new_process_list):
                            pid_to_kill, process_name = new_process_list[num-1]
                            try:
                                proc = psutil.Process(pid_to_kill)
                                proc.kill()
                                print(f"Processo '{process_name}' (PID: {pid_to_kill}) terminato.")
                            except Exception as e:
                                print(f"Errore nel terminare il processo '{process_name}' (PID: {pid_to_kill}): {e}")
                        else:
                            print(f"Numero '{num}' non valido.")
                    except ValueError:
                        print(f"Input '{selection.strip()}' non valido. Inserisci numeri interi.")
            else:
                print("Nessuna azione intrapresa.")
            
            # Aggiorna la baseline con i nuovi processi per evitare ripetizioni nelle iterazioni successive
            baseline.update(new_processes)
        else:
            print("Nessun nuovo processo rilevato.")

if __name__ == '__main__':
    # Chiede all'utente se desidera cercare la cartella virus_simulation
    search_choice = input("Vuoi cercare la cartella 'virus_simulation' a partire dalla directory corrente? (s/n): ")
    if search_choice.lower() == 's':
        start_dir = os.getcwd()
        results = search_folder(start_dir)
        if results:
            print("Cartella 'virus_simulation' trovata nei seguenti percorsi:")
            for path in results:
                print(f"  {path}")
        else:
            print(f"Cartella 'virus_simulation' non trovata a partire da {start_dir}.")
    
    # Avvia il monitoraggio dei processi
    monitor_new_processes()
