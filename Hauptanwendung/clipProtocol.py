import pyperclip
import time
import logging
from configdataHandler import configdataHandler

class clipProtocol:
    def __init__(self, isSender: bool, configHandler: configdataHandler, logger: logging.Logger):
        self.sender = isSender

        self.tmpClip = ""

        self.actionString_StartSending = "StartSending"
        self.actionString_StartReceiving = "StartReceiving"
        self.actionString_Proceed = "Proceed"
        self.actionString_Finish = "finish"

        self.destinationString_Re = "toRe_"
        self.destinationString_Se = "toSe_"

        self.configHandler = configHandler
        self.goSleep = False
        self.sleeps = False

        self.logger = logger

    def start(self):
        try:
            pyperclip.copy(self.destinationString_Re + self.actionString_StartReceiving)
        except pyperclip.PyperclipException as pe:
            self.logger.exception("Fehler beim schreiben in die Zwischenablage")
            raise
        self.logger.info("Start Mitteilung in die Zwischenablage geschrieben: " + self.destinationString_Re + self.actionString_StartReceiving)
        result = self.wait()
        return result
        
    def proceed(self, data):
        if self.sender == True:
            try:
                pyperclip.copy(self.destinationString_Re + self.actionString_Proceed + ";"+data)
            except pyperclip.PyperclipException as pe:
                self.logger.exception("Fehler beim schreiben in die Zwischenablage")
                raise
            self.logger.info("Proceed Mitteilung und Segment in die Zwischenablage geschrieben: " + self.destinationString_Re + self.actionString_Proceed + ";" + data[:30])
            result = self.wait()
            return result
            
        else:
            try:
                pyperclip.copy(self.destinationString_Se + self.actionString_Proceed)
            except pyperclip.PyperclipException as pe:
                self.logger.exception("Fehler beim schreiben in die Zwischenablage")
                raise
            self.logger.info("Proceed Mitteilung in die Zwischenablage geschrieben: " + self.destinationString_Se + self.actionString_Proceed)
            result = self.wait()
            return result 
        
    def wait(self):
        self.logger.info("clipProtocol.wait() betreten")
        #Pufferzeit
        time.sleep(self.configHandler.getConfigdata(configdataHandler.BUFFER_TIME))
        
        #Erprobungsversuch - Diesen Block weglassen / TmpClip mit Standardstring initialisieren
        '''try:
            self.tmpClip = pyperclip.paste()
        except pyperclip.PyperclipWindowsException as wine:
            wineCounter += 1
            if self.configHandler.getConfigdata(configdataHandler.TRANSMISSION_RUNS) == True:
                self.logger.warning("PyperclipWindowsException raised zum %s. mal", wineCounter)
            if wineCounter < 5:
                time.sleep(1)
                self.tmpClip = pyperclip.paste()
            else:
                self.logger.exception("PyperclipWindowsException tritt zu oft auf")
                raise
        except pyperclip.PyperclipException as pe:
            self.logger.exception("Fehler beim lesen aus der Zwischenablage")
            raise'''
        self.tmpClip = "ini"

        loopCounter = 0
        toeCounter = 0
        wineCounter = 0
        while True:
            loopCounter += 1
            if self.configHandler.getConfigdata(configdataHandler.TRANSMISSION_RUNS) == True:
                self.logger.info("String, der in Warteschleifendurchlauf %s , aus der Zwischenablage gelesen wurde: %s", loopCounter, self.tmpClip[:30])
            if self.goSleep == True:
                self.logger.info("Lokale receiveFile Funktion geht schlafen")
                self.sleep()
                self.logger.info("Lokale receiveFile Funktion wacht auf")
                try:
                    pyperclip.copy("Dateiuebertragungstool")
                except pyperclip.PyperclipException as pe:
                    self.logger.exception("Fehler beim schreiben in die Zwischenablage")
                    raise
                self.logger.info("Initialisierungsstring 'Dateiuebertragungstool' in die Zwischenablage kopiert")
            if self.tmpClip == self.destinationString_Re + self.actionString_StartReceiving and self.sender == False:
                self.logger.info("Start Mitteilung empfangen: " + self.destinationString_Re + self.actionString_StartReceiving)
                try:
                    pyperclip.copy(self.destinationString_Se + self.actionString_StartSending)
                except pyperclip.PyperclipException as pe:
                    self.logger.exception("Fehler beim schreiben in die Zwischenablage")
                    raise
                self.logger.info("Start Mitteilung in die Zwischenablage geschrieben: " + self.destinationString_Se + self.actionString_StartSending)
                return self.wait()
            elif self.tmpClip == self.destinationString_Se + self.actionString_StartSending and self.sender == True:
                self.logger.info("Start Mitteilung empfangen: " + self.destinationString_Se + self.actionString_StartSending)
                break
            elif self.tmpClip.split(";")[0] == self.destinationString_Re + self.actionString_Proceed and self.sender == False:
                self.logger.info("Proceed Mitteilung empfangen: " + self.destinationString_Re + self.actionString_Proceed)
                return self.tmpClip.split(";")[1]
            elif self.tmpClip == self.destinationString_Se + self.actionString_Proceed and self.sender == True:
                self.logger.info("Proceed Mitteilung empfangen: " + self.destinationString_Se + self.actionString_Proceed)
                break
            elif self.tmpClip == self.destinationString_Se + self.actionString_Finish and self.sender == True:
                self.logger.info("Finish Mitteilung empfangen: " + self.destinationString_Se + self.actionString_Finish)
                break
            elif self.tmpClip == self.destinationString_Re + self.actionString_Finish and self.sender == False:
                self.logger.info("Finish Mitteilung empfangen: " + self.destinationString_Re + self.actionString_Finish)
                try:
                    pyperclip.copy(self.destinationString_Se + self.actionString_Finish)
                except pyperclip.PyperclipException as pe:
                    self.logger.exception("Fehler beim schreiben in die Zwischenablage")
                    raise
                self.logger.info("Finish Mitteilung in die Zwischenablage geschrieben: " + self.destinationString_Se + self.actionString_Finish)
                return "exit"
            else:
                try:
                    self.tmpClip = pyperclip.waitForNewPaste(timeout=1)
                except pyperclip.PyperclipTimeoutException as toe:
                    toeCounter += 1
                    if self.configHandler.getConfigdata(configdataHandler.TRANSMISSION_RUNS) == True:
                        self.logger.warning("PyperclipTimeoutException raised zum %s. mal", toeCounter)
                    self.tmpClip = pyperclip.paste()
                    print("*** pyperclip.waitForNewPaste() Timeout raised in clipProtocol.wait() ***")
                except pyperclip.PyperclipWindowsException as wine:
                    wineCounter += 1
                    if self.configHandler.getConfigdata(configdataHandler.TRANSMISSION_RUNS) == True:
                        self.logger.warning("PyperclipWindowsException raised zum %s. mal", wineCounter)
                    if wineCounter < 5:
                        time.sleep(1)
                        self.tmpClip = pyperclip.paste()
                    else:
                        self.logger.exception("PyperclipWindowsException tritt zu oft auf")
                        raise
                except pyperclip.PyperclipException as pe:
                    self.logger.exception("Fehler beim lesen aus der Zwischenablage")
                    raise
        self.logger.info("clipProtocol.wait() verlassen")
        return ""
    
    def sleep(self):
        while True:
            self.sleeps = True
            if self.configHandler.getConfigdata(configdataHandler.TRANSMISSION_RUNS) == False:
                self.goSleep = False
                self.sleeps = False
                break
            time.sleep(1)
        return
    
    def finish(self):
        try:
            pyperclip.copy(self.destinationString_Re + self.actionString_Finish)
        except pyperclip.PyperclipException as pe:
            self.logger.exception("Fehler beim schreiben in die Zwischenablage")
            raise
        self.logger.info("Finish Mitteilung in die Zwischenablage geschrieben: " + self.destinationString_Re + self.actionString_Finish)
        self.wait()
        return