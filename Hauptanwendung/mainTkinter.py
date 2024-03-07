import tkinter as tk
from tkinter import filedialog
import threading
import sendFile
import receiveFile
from configparser import ConfigParser
import os
from configdataHandler import configdataHandler
import math
from functools import partial



class DateiuebertragungsTool:
    def __init__(self,root):
        self.root = root

        #Einstellungen Hauptfenster
        self.root.title("Dateiuebertragungstool")
        self.root.geometry("500x300")
        
        #Initialisierungsdatei erstellen, wenn nicht vorhanden:
        if not os.path.exists(os.path.dirname(os.path.abspath(__file__)) + "/dateiuebertragungsTool.ini"):
            try:
                self.generateIni()
            except:
                print("*** ERROR: Initialisierungsdatei konnte nicht erstellt werden ***")
                exit(1)

        #Default Settings aus Initialisierungsdatei lesen und ein Objekt der Klasse "configdataHandler" damit initialisieren
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
        
        #receiveFile() separatem Thread zuweisen und starten
        self.thread1 = threading.Thread(target=receiveFile.receiveFile, args=(configHandler,))
        self.thread1.daemon = True
        self.thread1.start()

        #---------------------------------GUI Elemente------------------------------#
        #Eingabefeld für Segmentgröße
        self.blockLength_inputField_label = tk.Label(root, text = "Segmentgröße in Byte: ")
        self.blockLength_inputField_label.place(relx = 0.05, rely = 0.05)
        self.blockLength_inputField = tk.Entry(root)
        self.blockLength_inputField.place(relx = 0.05, rely = 0.125, relheight= 0.1, relwidth=0.22)
        self.blockLength_okButton = tk.Button(root, text = "Ok", command=lambda: self.read_inputField("blockLength",configHandler))
        self.blockLength_okButton.place(relx = 0.275, rely=0.125, relheight=0.1)
        #Eingabefeld für Pufferzeit
        self.bufferTime_inputField_label = tk.Label(root, text = "Pufferzeit in s: ")
        self.bufferTime_inputField_label.place(relx = 0.05, rely = 0.225)
        self.bufferTime_inputField = tk.Entry(root)
        self.bufferTime_inputField.place(relx = 0.05, rely = 0.3, relheight= 0.1, relwidth=0.22)
        self.bufferTime_okButton = tk.Button(root, text = "Ok", command=lambda: self.read_inputField("bufferTime",configHandler))
        self.bufferTime_okButton.place(relx = 0.275, rely=0.3, relheight=0.1)
        #Eingabefeld für InputFile
        self.chooseInputFile_Button = tk.Button(root, text = "Eingabedatei auswählen", command=lambda: self.choose_file(configHandler))
        self.chooseInputFile_Button.place(relx = 0.05, rely=0.45, relheight=0.1, relwidth=0.29)
        #Eingabefeld für Ausgabepfad
        self.chooseOutputPath_Button = tk.Button(root, text = "Ausgabepfad auswählen", command=lambda: self.choose_filepath(configHandler))
        self.chooseOutputPath_Button.place(relx = 0.05, rely=0.55, relheight=0.1, relwidth=0.29)
        #Label für Segmentgröße
        self.blockLength_label = tk.Label(root, text="Segmentgröße: " + str(configHandler.getConfigdata("blockLength")) + " Byte")
        self.blockLength_label.place(relx = 0.05, rely = 0.675)
        #Label für Pufferzeit
        self.bufferTime_label = tk.Label(root, text="Pufferzeit: " + str(configHandler.getConfigdata("bufferTime")) + " s")
        self.bufferTime_label.place(relx = 0.05, rely = 0.75)
        #Label für InputFile
        self.inputFile_label = tk.Label(root, text="Eingabe Datei: " + configHandler.getConfigdata("inputFile"))
        self.inputFile_label.place(relx = 0.05, rely = 0.825)
        #Label für outputPath
        self.outputPath_label = tk.Label(root, text="Ausgabepfad: " + configHandler.getConfigdata("outputPath"))
        self.outputPath_label.place(relx = 0.05, rely = 0.9)
        #Label Segmentanzahl gesamt
        self.segmentsToSend_label = tk.Label(root, text= "Segmentanzahl gesamt: " + str(configHandler.getConfigdata("segmentsToSend")))
        self.segmentsToSend_label.place(relx = 0.5, rely = 0.675)
        #Label Segmentanzahl gesendet
        self.segmentsSended_label = tk.Label(root, text= "Segmentanzahl gesendet: " + str(configHandler.getConfigdata("segmentsSended")))
        self.segmentsSended_label.place(relx = 0.5, rely = 0.75)
        self.updateLabel("segmentsSended",configHandler)
        #Button Senden
        send_button = tk.Button(root, text="Senden", command=lambda: self.init_sending(configHandler), width=40, height=8)
        send_button.place(relx=0.95, rely=0.325, anchor=tk.E)

    #--------------------------------Hilfsmethoden-----------------------------------#
    def generateIni(self):
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
        if file == "":
            print('*** INFO: Operation "choose Inputfile" was cancelled! ***')
            return
        if file:
            print(f"Ausgewählte Datei: {file}")
        if not(os.path.exists(file)):
            print('*** ERROR:  Input file ' + file +' does not exist! ***')
            exit(1)
        configHandler.setConfigdata("inputFile", file)
        configHandler.setConfigdata("segmentsToSend", math.ceil(os.path.getsize(file)/configHandler.getConfigdata("blockLength")))
        self.updateLabel("inputFile",configHandler)
        self.updateLabel("segmentsToSend",configHandler)
        return

    def choose_filepath(self, configHandler: configdataHandler):
        filepath = filedialog.askdirectory(title="Dateipfad auswählen")
        if filepath == "":
            print('*** INFO: Operation "choose Outputfilepath" was cancelled! ***')
            return
        if not(os.path.exists(filepath)):
            print('*** ERROR: Outputpath ' + filepath +' does not exist! ***')
            exit(1)
        configHandler.setConfigdata("outputPath", filepath)
        self.updateLabel("outputPath", configHandler)
        return
    
    def read_inputField(self,configAttr:str, configHandler: configdataHandler):
        if configAttr == "blockLength":
            try:
                blockLength = self.blockLength_inputField.get()
                blockLength = int(blockLength)
                if blockLength > 0:
                    configHandler.setConfigdata(configAttr,blockLength)
                    configHandler.setConfigdata("segmentsToSend", math.ceil(os.path.getsize(configHandler.inputFile)/configHandler.getConfigdata("blockLength")))
                    self.updateLabel("blockLength", configHandler)
                    self.updateLabel("segmentsToSend", configHandler)
                else:
                    raise ValueError
            except:
                print("*** VALUE ERROR: Positive integer Number is needed ***")
                return
        elif configAttr == "bufferTime":
            try:
                bufferTime = self.bufferTime_inputField.get()
                bufferTime = float(bufferTime)
                if bufferTime > 0:
                    configHandler.setConfigdata(configAttr,bufferTime)
                    self.updateLabel("bufferTime", configHandler)
                    return
                else:
                    raise ValueError
            except:
                print("*** VALUE ERROR: Positive float Number is needed ***")
                return
        return

    def updateLabel(self, configAttr: str, configHandler: configdataHandler):
        if configAttr == "blockLength":
            self.blockLength_label.config(text= "Segmentgröße: " + str(configHandler.getConfigdata("blockLength")) + " Byte")
        elif configAttr == "bufferTime":
            self.bufferTime_label.config(text= "Pufferzeit: " + str(configHandler.getConfigdata("bufferTime")) + " s")
        elif configAttr == "outputPath":
            self.outputPath_label.config(text="Ausgabepfad: " + configHandler.getConfigdata("outputPath"))
        elif configAttr == "inputFile":
            self.inputFile_label.config(text= "Eingabe Datei: " + configHandler.getConfigdata("inputFile"))
        elif configAttr == "segmentsToSend":
            self.segmentsToSend_label.config(text= "Segmentanzahl gesamt: " + str(configHandler.getConfigdata("segmentsToSend")))
        elif configAttr == "segmentsSended":
            self.segmentsSended_label.config(text= "Segmentanzahl gesendet: " + str(configHandler.getConfigdata("segmentsSended")))
            self.root.after(500, partial(self.updateLabel, "segmentsSended", configHandler))
        return
        
    def init_sending(self, configHandler: configdataHandler):
        #Lokalen Empfangsthread stoppen:
        configHandler.stopEvent.set()
        #Sendevorgang starten
        thread2 = threading.Thread(target=sendFile.sendFile, args=( configHandler,))
        thread2.daemon = True
        thread2.start()
        return

def main():
    root = tk.Tk()
    dateiuebertragunsTool = DateiuebertragungsTool(root)
    root.mainloop()
    
main()