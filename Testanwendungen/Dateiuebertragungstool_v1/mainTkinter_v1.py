import tkinter as tk
from tkinter import filedialog
import threading
import sendFile_v2
import receiveFile_v2
from configparser import ConfigParser
import configwriter
import os


def choose_file():
    file = filedialog.askopenfilename(title="Datei auswählen")
    if file:
        print(f"Ausgewählte Datei: {file}")
    return file

def init_sending():

    #-------------------------------Auswahl Inputfile---------------------------------------#
    inputFile = choose_file()
    #Vorgang abbrechen, wenn keine Datei ausgewählt wurde
    if inputFile == '':
        return
    
    #----------------------------Versenden des Inputfiles------------------------------------#
    #Sendevorgang starten
    thread2 = threading.Thread(target=sendFile_v2.sendFile, args=(inputFile, blockLength, bufferTime,))
    thread2.daemon = True
    thread2.start()
    return


# Erstellen des Hauptfensters
root = tk.Tk()
root.title("Dateiuebertragungstool")

# Festlegen der Größe auf 700x300 Pixel
root.geometry("800x300")

#Initialisierungsdatei erstellen, wenn nicht vorhanden:
if not os.path.exists(os.path.dirname(os.path.abspath(__file__)) + "/dateiuebertragungsTool.ini"):
    try:
        configwriter.configwriter()
    except:
        print("*** ERROR: Initialisierungsdatei konnte nicht erstellt werden ***")
        exit(1)

#Default Settings aus Initialisierungsdatei lesen; Abbruch wenn nicht lesbar oder nicht vorhanden
if os.path.isfile("dateiuebertragungsTool.ini"):
    config = ConfigParser()
    config.read("dateiuebertragungsTool.ini")
    try:
        configData = config["DEFAULT"]
    except:
        print("Konfigurationseinstellungen konnten nicht übernommen werden")
        exit(1)

    blockLength = int(configData["blockLength"])
    outputPath = configData["outputPath"]
    bufferTime = float(configData["bufferTime"])
else:
    exit(1)

#Receive Funktion separatem Thread zuweisen und starten
thread1 = threading.Thread(target=receiveFile_v2.receiveFile, args=(outputPath,blockLength,bufferTime))
thread1.daemon = True
thread1.start()

#Erstellen von Labels um die Initialisierungseinstellungen anzuzeigen:
blockLength_label = tk.Label(root, text="Segmentgröße: " + str(blockLength) + "Byte")
blockLength_label.place(relx = 0.05, rely = 0.6)

bufferTime_label = tk.Label(root, text="Pufferzeit: " + str(bufferTime) + "s")
bufferTime_label.place(relx = 0.05, rely = 0.7)

outputPath_label = tk.Label(root, text="Ausgabepfad: " + outputPath)
outputPath_label.place(relx = 0.05, rely = 0.8)


# Erstellen von Buttons; Send Funktion dem Button "Senden" zuweisen
send_button = tk.Button(root, text="Senden", command=lambda: init_sending(), width=30, height=5)
send_button.place(relx=0.65, rely=0.3, anchor=tk.E)

# Starten der Tkinter-Schleife
root.mainloop()