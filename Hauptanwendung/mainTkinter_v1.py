import tkinter as tk
from tkinter import filedialog
import threading
import sendFile_v2
import receiveFile_v2


def choose_file():
    file = filedialog.askopenfilename(title="Datei auswählen")
    if file:
        print(f"Ausgewählte Datei: {file}")
    return file

def choose_filepath():
    file_path = filedialog.askdirectory(title="Dateipfad auswählen")
    if file_path:
        print(f"Ausgewählter Dateipfad: {file_path}")
    return file_path

def init_sending():

    #-------------------------------Auswahl Inputfile---------------------------------------#
    inputFile = choose_file()
    #Vorgang abbrechen, wenn keine Datei ausgewählt wurde
    if inputFile == '':
        return
    
    #----------------------------Versenden des Inputfiles------------------------------------#
    #Sendevorgang starten
    thread2 = threading.Thread(target=sendFile_v2.sendFile, args=(inputFile,))
    thread2.daemon = True
    thread2.start()
    return


# Erstellen des Hauptfensters
root = tk.Tk()
root.title("Dateiuebertragungstool")

# Festlegen der Größe auf 500x500 Pixel
root.geometry("500x300")

#Threads initialisieren
thread1 = threading.Thread(target=receiveFile_v2.receiveFile)
thread1.daemon = True

#Receive Funktion im Hintergrund starten
thread1.start()


# Erstellen von Widgets; Send Funktion dem Button "Senden" zuweisen
send_button = tk.Button(root, text="Senden", command=lambda: init_sending(), width=30, height=5)
send_button.place(relx=0.7, rely=0.5, anchor=tk.E)

# Starten der Tkinter-Schleife
root.mainloop()