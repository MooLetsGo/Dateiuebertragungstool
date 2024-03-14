import tkinter as tk
from tkinter import filedialog
import threading
import sendFile
import receiveFile
from configparser import ConfigParser
import os
from configdataHandler import configdataHandler
from clipProtocol import clipProtocol
import math
from functools import partial
import logging


class DateiuebertragungsTool:
    def __init__(self,root,configHandler: configdataHandler, protocolSender: clipProtocol, protocolReceiver: clipProtocol):
        self.root = root

        self.configHandler = configHandler
        self.protocolSender = protocolSender
        self.protocolReceiver = protocolReceiver

        #Einstellungen Hauptfenster
        self.root.title("Dateiuebertragungstool")
        self.root.geometry("500x300")

        #receiveFile() separatem Thread zuweisen und starten
        self.thread1 = threading.Thread(target=receiveFile.receiveFile, args=(self.configHandler, self.protocolReceiver))
        self.thread1.daemon = True
        self.thread1.start()

        #---------------------------------GUI Elemente------------------------------#
        #Eingabefeld für Segmentgröße
        self.blockLength_inputField_label = tk.Label(root, text = "Segmentgröße in Byte: ")
        self.blockLength_inputField_label.place(relx = 0.05, rely = 0.05)
        self.blockLength_inputField = tk.Entry(root)
        self.blockLength_inputField.place(relx = 0.05, rely = 0.125, relheight= 0.1, relwidth=0.22)
        self.blockLength_okButton = tk.Button(root, text = "Ok", command=lambda: self.read_inputField(configdataHandler.BLOCK_LENGTH))
        self.blockLength_okButton.place(relx = 0.275, rely=0.125, relheight=0.1)
        #Eingabefeld für Pufferzeit
        self.bufferTime_inputField_label = tk.Label(root, text = "Pufferzeit in s: ")
        self.bufferTime_inputField_label.place(relx = 0.05, rely = 0.225)
        self.bufferTime_inputField = tk.Entry(root)
        self.bufferTime_inputField.place(relx = 0.05, rely = 0.3, relheight= 0.1, relwidth=0.22)
        self.bufferTime_okButton = tk.Button(root, text = "Ok", command=lambda: self.read_inputField(configdataHandler.BUFFER_TIME))
        self.bufferTime_okButton.place(relx = 0.275, rely=0.3, relheight=0.1)
        #Eingabefeld für InputFile
        self.chooseInputFile_Button = tk.Button(root, text = "Eingabedatei auswählen", command=lambda: self.choose_file())
        self.chooseInputFile_Button.place(relx = 0.05, rely=0.45, relheight=0.1, relwidth=0.29)
        #Eingabefeld für Ausgabepfad
        self.chooseOutputPath_Button = tk.Button(root, text = "Ausgabepfad auswählen", command=lambda: self.choose_filepath())
        self.chooseOutputPath_Button.place(relx = 0.05, rely=0.55, relheight=0.1, relwidth=0.29)
        #Label für Segmentgröße
        self.blockLength_label = tk.Label(root, text="Segmentgröße: " + str(self.configHandler.getConfigdata(configdataHandler.BLOCK_LENGTH)) + " Byte")
        self.blockLength_label.place(relx = 0.05, rely = 0.675)
        self.updateLabel(configdataHandler.BLOCK_LENGTH)
        #Label für Pufferzeit
        self.bufferTime_label = tk.Label(root, text="Pufferzeit: " + str(self.configHandler.getConfigdata(configdataHandler.BUFFER_TIME)) + " s")
        self.bufferTime_label.place(relx = 0.05, rely = 0.75)
        #Label für InputFile
        self.inputFile_label = tk.Label(root, text="Eingabe Datei: " + self.configHandler.getConfigdata(configdataHandler.INPUT_FILE))
        self.inputFile_label.place(relx = 0.05, rely = 0.825)
        #Label für outputPath
        self.outputPath_label = tk.Label(root, text="Ausgabepfad: " + self.configHandler.getConfigdata(configdataHandler.OUTPUT_PATH))
        self.outputPath_label.place(relx = 0.05, rely = 0.9)
        #Label Segmentanzahl gesamt
        self.segmentsToSend_label = tk.Label(root, text= "Segmentanzahl gesamt: " + str(self.configHandler.getConfigdata(configdataHandler.SEGMENTS_TO_SEND)))
        self.segmentsToSend_label.place(relx = 0.5, rely = 0.675)
        self.updateLabel(configdataHandler.SEGMENTS_TO_SEND)
        #Label Segmentanzahl gesendet
        self.segmentsSended_label = tk.Label(root, text= "Segmentanzahl übertragen: " + str(self.configHandler.getConfigdata(configdataHandler.SEGMENTS_SENDED)))
        self.segmentsSended_label.place(relx = 0.5, rely = 0.75)
        self.updateLabel(configdataHandler.SEGMENTS_SENDED)
        #Button Senden
        send_button = tk.Button(root, text="Senden", command=lambda: self.init_sending(), width=40, height=8)
        send_button.place(relx=0.95, rely=0.325, anchor=tk.E)

    #--------------------------------Methoden-----------------------------------#

    def choose_file(self):
        file = filedialog.askopenfilename(title="Datei auswählen")
        if file == "":
            return
        if not(os.path.exists(file)):
            print('*** ERROR:  File ' + file +' does not exist! ***')
            exit(1)
        self.configHandler.setConfigdata(configdataHandler.INPUT_FILE, file)
        self.configHandler.setConfigdata(configdataHandler.SEGMENTS_TO_SEND, math.ceil(os.path.getsize(file)/self.configHandler.getConfigdata(configdataHandler.BLOCK_LENGTH)))
        self.updateLabel(configdataHandler.INPUT_FILE)
        self.updateLabel(configdataHandler.SEGMENTS_TO_SEND)
        return

    def choose_filepath(self):
        filepath = filedialog.askdirectory(title="Dateipfad auswählen")
        if filepath == "":
            return
        if not os.path.exists(filepath):
            print('*** ERROR: Filepath ' + filepath +' does not exist! ***')
            exit(1)
        self.configHandler.setConfigdata(configdataHandler.OUTPUT_PATH, filepath)
        self.updateLabel(configdataHandler.OUTPUT_PATH)
        return
    
    def read_inputField(self,configHandlerAttr:str):
        if configHandlerAttr == configdataHandler.BLOCK_LENGTH:
            try:
                blockLength = self.blockLength_inputField.get()
                blockLength = int(blockLength)
                if blockLength > 0:
                    self.configHandler.setConfigdata(configHandlerAttr,blockLength)
                    if self.configHandler.inputFile != "":
                        self.configHandler.setConfigdata(configdataHandler.SEGMENTS_TO_SEND, math.ceil(os.path.getsize(self.configHandler.inputFile)/self.configHandler.getConfigdata(configdataHandler.BLOCK_LENGTH)))
                    self.updateLabel(configdataHandler.BLOCK_LENGTH)
                    self.updateLabel(configdataHandler.SEGMENTS_TO_SEND)
                else:
                    raise ValueError
            except ValueError as ve:
                print("*** VALUE ERROR: Positive integer Number is needed ***")
            except Exception as e:
                raise
        elif configHandlerAttr == configdataHandler.BUFFER_TIME:
            try:
                bufferTime = self.bufferTime_inputField.get()
                bufferTime = float(bufferTime)
                if bufferTime > 0:
                    self.configHandler.setConfigdata(configHandlerAttr,bufferTime)
                    self.updateLabel(configdataHandler.BUFFER_TIME)
                else:
                    raise ValueError
            except ValueError as ve:
                print("*** VALUE ERROR: Positive float Number is needed ***")
            except Exception as e:
                raise
        return

    def updateLabel(self, configAttr: str):
        if configAttr == configdataHandler.BLOCK_LENGTH:
            self.blockLength_label.config(text= "Segmentgröße: " + str(self.configHandler.getConfigdata(configdataHandler.BLOCK_LENGTH)) + " Byte")
            self.root.after(400, partial(self.updateLabel, configdataHandler.BLOCK_LENGTH))
        elif configAttr == configdataHandler.BUFFER_TIME:
            self.bufferTime_label.config(text= "Pufferzeit: " + str(self.configHandler.getConfigdata(configdataHandler.BUFFER_TIME)) + " s")
        elif configAttr == configdataHandler.OUTPUT_PATH:
            self.outputPath_label.config(text="Ausgabepfad: " + self.configHandler.getConfigdata(configdataHandler.OUTPUT_PATH))
        elif configAttr == configdataHandler.INPUT_FILE:
            self.inputFile_label.config(text= "Eingabe Datei: " + self.configHandler.getConfigdata(configdataHandler.INPUT_FILE))
        elif configAttr == configdataHandler.SEGMENTS_TO_SEND:
            self.segmentsToSend_label.config(text= "Segmentanzahl gesamt: " + str(self.configHandler.getConfigdata(configdataHandler.SEGMENTS_TO_SEND)))
            self.root.after(500, partial(self.updateLabel, configdataHandler.SEGMENTS_TO_SEND))
        elif configAttr == configdataHandler.SEGMENTS_SENDED:
            self.segmentsSended_label.config(text= "Segmentanzahl übertragen: " + str(self.configHandler.getConfigdata(configdataHandler.SEGMENTS_SENDED)))
            self.root.after(300, partial(self.updateLabel, configdataHandler.SEGMENTS_SENDED))
        return
        
    def init_sending(self):
        if self.configHandler.getConfigdata(configdataHandler.TRANSMISSION_RUNS) == True:
            print("*** WARNING: Transmission is already running ***")
            return
        if self.configHandler.getConfigdata(configdataHandler.INPUT_FILE) == "":
            print("*** WARNING: No Inputfile selected! ***")
            return
        self.configHandler.setConfigdata(configdataHandler.TRANSMISSION_RUNS,True)
        #Lokalen Empfangsthread stoppen:
        self.protocolReceiver.goSleep = True
        while True:
            if self.protocolReceiver.sleeps == True:
                break
        #Sendevorgang starten
        thread2 = threading.Thread(target=sendFile.sendFile, args=( self.configHandler, self.protocolSender))
        thread2.daemon = True
        thread2.start()
        return

def main():
    logging.basicConfig(level=logging.INFO)
    
    sendEvents_logger = logging.getLogger("sendEvents_logger")
    sendEvents_logger.propagate = False
    sendEvents_logger_handler = logging.FileHandler("sendEvents.log")
    sendEvents_logger_formatter = logging.Formatter("%(asctime)s - %(name)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s")
    sendEvents_logger_handler.setFormatter(sendEvents_logger_formatter)
    sendEvents_logger.addHandler(sendEvents_logger_handler)
    
    receiveEvents_logger = logging.getLogger("receiveEvents_logger")
    receiveEvents_logger.propagate = False
    receiveEvents_logger_handler = logging.FileHandler("receiveEvents.log")
    receiveEvents_logger_formatter = logging.Formatter("%(asctime)s - %(name)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s")
    receiveEvents_logger_handler.setFormatter(receiveEvents_logger_formatter)
    receiveEvents_logger.addHandler(receiveEvents_logger_handler)
    
    #---------------------------INI Datei Erstellen-----------------------#
    config = ConfigParser()
    #Initialisierungsdatei erstellen, wenn nicht vorhanden:
    if not os.path.exists(os.path.dirname(os.path.abspath(__file__)) + "/" + configdataHandler.INI_FILE_NAME):
        config[configdataHandler.INI_FILE_CONFIG_NAME] = {
        configdataHandler.BLOCK_LENGTH: 1048576,
        configdataHandler.BUFFER_TIME: 0.8,
        configdataHandler.OUTPUT_PATH:  os.path.join(os.path.expanduser("~")), 
        }
        try:
            with open(configdataHandler.INI_FILE_NAME, "w") as file:
                config.write(file)
        except Exception as e:
            print("*** Initialisierungsdatei konnte nicht erstellt werden ***")
            raise 
    
    
    #---------------configdataHandler Instanz initialiesieren-------------#
    #Default Settings aus INI Datei lesen 
    if os.path.isfile(configdataHandler.INI_FILE_NAME):
        config.read(configdataHandler.INI_FILE_NAME)
        configData = config[configdataHandler.INI_FILE_CONFIG_NAME]
        try:
            blockLength = int(configData[configdataHandler.BLOCK_LENGTH])
            bufferTime = float(configData[configdataHandler.BUFFER_TIME])
            if blockLength <= 0 or bufferTime <= 0:
                raise ValueError
            outputPath = str(configData[configdataHandler.OUTPUT_PATH])
            if not os.path.exists(outputPath):
                raise FileNotFoundError
        except ValueError as ve:
            print("*** VALUE WARNING: Werte der Initialisierungsparameter in INI-Datei können nicht verwendet werden ***")
        except FileNotFoundError as fnfe:
            print("*** FILE NOT FOUND WARNING: Pfad des Initialisierungsparameters 'outputPath' in INI-Datei existiert nicht ***")
        except Exception as e:
            raise

    #Objekt vom Typ "configdataHandler" initialisieren
    configHandler = configdataHandler(blockLength, bufferTime, outputPath)
    #Protokoll Instanzen für die sendFile() und receiveFile() Funktionen initialisieren
    protocolSender = clipProtocol(True,configHandler,sendEvents_logger)
    protocolReceiver = clipProtocol(False,configHandler,receiveEvents_logger)
    root = tk.Tk()
    dateiuebertragunsTool = DateiuebertragungsTool(root,configHandler,protocolSender,protocolReceiver)
    root.mainloop()
if __name__ == '__main__':    
    main()