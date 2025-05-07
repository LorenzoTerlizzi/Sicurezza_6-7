
import pandas as pd
import numpy as np

# Carica il CSV
df = pd.read_csv("Darknet.csv")

# Rimuovi eventuali colonne duplicate
df = df.loc[:, ~df.columns.duplicated()]

# Funzione per formattare blocchi di statistica
def descrivi_statistiche(colonne, nome_blocco):
    risultati = [f"--- {nome_blocco} ---"]
    for col in colonne:
        if col in df.columns:
            serie = pd.to_numeric(df[col], errors='coerce')
            risultati.append(f"{col}:\n"
                             f"  - media: {serie.mean():.2f}\n"
                             f"  - std:   {serie.std():.2f}\n"
                             f"  - min:   {serie.min():.2f}\n"
                             f"  - max:   {serie.max():.2f}")
        else:
            risultati.append(f"{col}: Non presente nel dataset.")
    return "\n".join(risultati)

# Blocchi logici di variabili per sezioni 1-14
report = []


# 1. Identificatori del flusso
report.append("--- 1. Identificatori del Flusso ---")
id_campi = ["Src IP", "Src Port", "Dst IP", "Dst Port", "Protocol", "Timestamp", "Flow Duration"]
for campo in id_campi:
    if campo in df.columns:
        unique = df[campo].nunique()
        report.append(f"{campo}: {unique} valori unici")
        # Se il campo è "Protocol", aggiungi i protocolli unici
        if campo == "Protocol":
            protocolli_unici = df[campo].unique()
            report.append(f"Protocol unici: {', '.join(map(str, protocolli_unici))}")
    else:
        report.append(f"{campo}: Non presente")

# 2. Conteggi pacchetti e byte
report.append(descrivi_statistiche(["Total Fwd Packet", "Total Bwd packets"], "2. Conteggi di Pacchetti"))
report.append(descrivi_statistiche(["Total Length of Fwd Packet", "Total Length of Bwd Packet"], "2. Lunghezza Totale Pacchetti"))

# 3. Statistiche lunghezza pacchetti
report.append(descrivi_statistiche(["Fwd Packet Length Max", "Fwd Packet Length Min", "Fwd Packet Length Mean", "Fwd Packet Length Std"], "3. Lunghezza Pacchetti Fwd"))
report.append(descrivi_statistiche(["Bwd Packet Length Max", "Bwd Packet Length Min", "Bwd Packet Length Mean", "Bwd Packet Length Std"], "3. Lunghezza Pacchetti Bwd"))

# 4. Larghezza di banda e frequenze
report.append(descrivi_statistiche(["Flow Bytes/s", "Flow Packets/s", "Fwd Packets/s", "Bwd Packets/s"], "4. Banda e Frequenze"))

# 5. Tempi di Inter-Arrivo (IAT)
report.append(descrivi_statistiche(["Flow IAT Mean", "Flow IAT Std", "Flow IAT Max", "Flow IAT Min"], "5. IAT del Flusso"))
report.append(descrivi_statistiche(["Fwd IAT Total", "Fwd IAT Mean", "Fwd IAT Std", "Fwd IAT Max", "Fwd IAT Min"], "5. IAT Fwd"))
report.append(descrivi_statistiche(["Bwd IAT Total", "Bwd IAT Mean", "Bwd IAT Std", "Bwd IAT Max", "Bwd IAT Min"], "5. IAT Bwd"))

# 6. TCP Flags
report.append(descrivi_statistiche(["Fwd PSH Flags", "Bwd PSH Flags", "Fwd URG Flags", "Bwd URG Flags",
                                    "FIN Flag Count", "SYN Flag Count", "RST Flag Count", "ACK Flag Count",
                                    "URG Flag Count", "CWE Flag Count", "ECE Flag Count"], "6. TCP Flags"))

# 7. Lunghezze header
report.append(descrivi_statistiche(["Fwd Header Length", "Bwd Header Length"], "7. Lunghezza Header"))

# 8. Distribuzione dimensioni pacchetti
report.append(descrivi_statistiche(["Packet Length Min", "Packet Length Max", "Packet Length Mean", "Packet Length Std", "Packet Length Variance"], "8. Dimensione Pacchetti"))

# 9. Rapporti direzionali
report.append(descrivi_statistiche(["Down/Up Ratio", "Average Packet Size", "Fwd Segment Size Avg", "Bwd Segment Size Avg"], "9. Rapporti Direzionali e Medie"))

# 10. Bulk traffic
report.append(descrivi_statistiche(["Fwd Avg Bytes/Bulk", "Bwd Avg Bytes/Bulk", "Fwd Avg Packets/Bulk",
                                    "Bwd Avg Packets/Bulk", "Fwd Avg Bulk Rate", "Bwd Avg Bulk Rate"], "10. Traffico Bulk"))

# 11. Sottoflussi
report.append(descrivi_statistiche(["Subflow Fwd Packets", "Subflow Bwd Packets", "Subflow Fwd Bytes", "Subflow Bwd Bytes"], "11. Sottoflussi"))

# 12. TCP Window e pacchetti
report.append(descrivi_statistiche(["Init_Win_bytes_forward", "Init_Win_bytes_backward",
                                    "act_data_pkt_fwd", "min_seg_size_forward"], "12. Finestra TCP e Pacchetti Dati"))

# 13. Attività/Inattività
report.append(descrivi_statistiche(["Active Mean", "Active Std", "Active Max", "Active Min"], "13. Tempi Attività"))
report.append(descrivi_statistiche(["Idle Mean", "Idle Std", "Idle Max", "Idle Min"], "13. Tempi Inattivi"))

# 14. Etichette
report.append("--- 14. Etichettatura ---")
if "Label" in df.columns:
    report.append(str(df["Label"].value_counts()))
else:
    report.append("Etichetta non presente nel file.")

# Salva tutto in un file .txt
with open("report_flussi.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(report))

print("Report generato in 'report_flussi.txt'")