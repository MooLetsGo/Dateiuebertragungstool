import tkinter as tk
from tkinter import filedialog
import threading
import sendFile
import receiveFile
from configparser import ConfigParser
import os
from configdataHandler import configdataHandler
import math
import time



class DateiuebertragungsTool:
    #--------------------------------Klasse für die Hauptanwendung----------------------------#
    def __init__(self,root):
        self.root = root

        #Einstellungen Hauptfenster
        self.root.title("Dateiuebertragungstool")
        self.root.geometry("500x300")
        

        #Initialisierungsdatei erstellen, wenn nicht vorhanden:
        if not os.path.exists(os.path.dirname(os.path.abspath(__file__)) + "/dateiuebertragungsTool.ini"):
            try:
                self.writeDefaultConfig()
            except:
                print("*** ERROR: Initialisierungsdatei konnte nicht erstellt werden ***")
                exit(1)

        #Default Settings aus Initialisierungsdatei lesen und einen "configHandler" damit initialisieren; Abbruch wenn nicht lesbar oder nicht vorhanden
        if os.path.isfile("dateiuebertragungsTool.ini"):
            config = ConfigParser()
            config.read("dateiuebertragungsTool.ini")
            try:
                configData = config["SETTINGS"]
            except:
                print("Konfigurationseinstellungen konnten nicht übernommen werden")
                exit(1)

            blockLength = int(configData["blockLength"])
            bufferTime = float(configData["bufferTime"])
            outputPath = configData["outputPath"]

            configHandler = configdataHandler(blockLength, bufferTime, outputPath)

        else:
            exit(1)
        
        #Receive Funktion separatem Thread zuweisen und starten
        self.thread1 = threading.Thread(target=receiveFile.receiveFile, args=(configHandler,))
        self.thread1.daemon = True
        self.thread1.start()

        #Eingabefeld für Segmentgröße
        self.blockLength_inputField_label = tk.Label(root, text = "Segmentgröße in Byte: ")
        self.blockLength_inputField_label.place(relx = 0.05, rely = 0.05)
        self.blockLength_inputField = tk.Entry(root)
        self.blockLength_inputField.place(relx = 0.05, rely = 0.125, relheight= 0.1, relwidth=0.22)
        self.blockLength_okButton = tk.Button(root, text = "Ok", command=lambda: self.read_inputField(0,configHandler))
        self.blockLength_okButton.place(relx = 0.275, rely=0.125, relheight=0.1)

        #Eingabefeld für Pufferzeit
        self.bufferTime_inputField_label = tk.Label(root, text = "Pufferzeit in s: ")
        self.bufferTime_inputField_label.place(relx = 0.05, rely = 0.225)
        self.bufferTime_inputField = tk.Entry(root)
        self.bufferTime_inputField.place(relx = 0.05, rely = 0.3, relheight= 0.1, relwidth=0.22)
        self.bufferTime_okButton = tk.Button(root, text = "Ok", command=lambda: self.read_inputField(1,configHandler))
        self.bufferTime_okButton.place(relx = 0.275, rely=0.3, relheight=0.1)

        #Eingabefeld für InputFile
        self.chooseInputFile_Button = tk.Button(root, text = "Eingabedatei auswählen", command=lambda: self.choose_file(configHandler))
        self.chooseInputFile_Button.place(relx = 0.05, rely=0.45, relheight=0.1, relwidth=0.29)

        #Eingabefeld für Ausgabepfad
        self.chooseOutputPath_Button = tk.Button(root, text = "Ausgabepfad auswählen", command=lambda: self.choose_filepath(configHandler))
        self.chooseOutputPath_Button.place(relx = 0.05, rely=0.55, relheight=0.1, relwidth=0.29)

        #Labels um die Konfigurationseinstellungen anzuzeigen:
        self.blockLength_label = tk.Label(root, text="Segmentgröße: " + str(configHandler.blockLength) + " Byte")
        self.blockLength_label.place(relx = 0.05, rely = 0.675)

        self.bufferTime_label = tk.Label(root, text="Pufferzeit: " + str(configHandler.bufferTime) + " s")
        self.bufferTime_label.place(relx = 0.05, rely = 0.75)

        self.inputFile_label = tk.Label(root, text="Eingabe Datei: " + configHandler.inputFile)
        self.inputFile_label.place(relx = 0.05, rely = 0.825)

        self.outputPath_label = tk.Label(root, text="Ausgabepfad: " + configHandler.outputPath)
        self.outputPath_label.place(relx = 0.05, rely = 0.9)

        #Label um die Segmentanzahl (verbleibend und übertragen) anzuzeigen:
        self.segmentsToSend_label = tk.Label(root, text= "Segmentanzahl gesamt: " + str(configHandler.segmentsToSend))
        self.segmentsToSend_label.place(relx = 0.5, rely = 0.675)

        self.segmentsSended_label = tk.Label(root, text= "Segmentanzahl gesendet: " + str(configHandler.segmentsSended))
        self.segmentsSended_label.place(relx = 0.5, rely = 0.75)

        # Erstellen von Buttons; Send Funktion dem Button "Senden" zuweisen
        send_button = tk.Button(root, text="Senden", command=lambda: self.init_sending(configHandler), width=40, height=8)
        send_button.place(relx=0.95, rely=0.325, anchor=tk.E)

    #--------------------------------Hilfsmethoden-----------------------------------#
    def writeDefaultConfig(self):
        config = ConfigParser()
        config["SETTINGS"] = {
            "blockLength": 1048576,
            "bufferTime": 0.8,
            "outputPath":  os.path.join(os.path.expanduser("~"), "Desktop"), #Desktop des lokalen Systems wird als Standard Ausgabepfad festgelegt
        }
        try:
            with open("dateiuebertragungsTool.ini", "w") as file:
                config.write(file)
        except:
            exit(1)


    def choose_file(self, configHandler: configdataHandler):
        file = filedialog.askopenfilename(title="Datei auswählen")
        if file:
            print(f"Ausgewählte Datei: {file}")
        #evtl. Existenzüberprüfung
        configHandler.setConfigdata(3, file)
        configHandler.setConfigdata(4, math.ceil(os.path.getsize(file)/configHandler.getConfigdata(0)))
        self.updateLabel(3,configHandler)
        self.updateLabel(4,configHandler)
        return

    def choose_filepath(self, configHandler: configdataHandler):
        file_path = filedialog.askdirectory(title="Dateipfad auswählen")
        configHandler.setConfigdata(2, file_path)
        self.updateLabel(2, configHandler)
        return
    
    #ToDo - Falscheingaben abfangen!!!
    def read_inputField(self,index:int, configHandler: configdataHandler):
        if index == 0:
            configHandler.setConfigdata(index,self.blockLength_inputField.get())
            self.updateLabel(index, configHandler)
        elif index == 1:
            configHandler.setConfigdata(index,self.bufferTime_inputField.get())
            self.updateLabel(index, configHandler)
        return
    
    #Todo Zugriff auf configHandler Daten korrekt machen
    def updateLabel(self, index: int, configHandler: configdataHandler):
        if index == 0:
            self.blockLength_label.config(text= "Segmentgröße: " + str(configHandler.blockLength) + " Byte")
        elif index == 1:
            self.bufferTime_label.config(text= "Pufferzeit: " + str(configHandler.bufferTime) + " s")
        elif index == 3:
            self.inputFile_label.config(text= "Eingabe Datei: " + configHandler.inputFile)
        elif index == 4:
            self.segmentsToSend_label.config(text= "Segmentanzahl gesamt: " + str(configHandler.segmentsToSend))
        elif index == 5:
            self.segmentsSended_label.config(text= "Segmentanzahl gesendet: " + str(configHandler.segmentsSended))
        return
        
    def init_sending(self, configHandler: configdataHandler):
        #Lokalen Empfangsthread stoppen:
        #configHandler.stopEvent.set()

        #Sendevorgang starten
        thread2 = threading.Thread(target=sendFile.sendFile, args=( configHandler,))
        thread2.daemon = True
        thread2.start()
        return

    

    #-----------------------------Hauptfunktion--------------------------------------#

def main():

    root = tk.Tk()
    dateiuebertragunsTool = DateiuebertragungsTool(root)
    root.mainloop()
    

main()