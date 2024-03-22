import pyperclip
import time
from configdataHandler import configdataHandler

class clipProtocol:
    def __init__(self, isSender: bool, configHandler: configdataHandler):
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

    def start(self):
        try:
            pyperclip.copy(self.destinationString_Re + self.actionString_StartReceiving)
        except pyperclip.PyperclipException as pe:
            print(f"Fehler beim schreiben in die Zwischenablage: {str(pe)}")
        result = self.wait()
        return result
        
    def proceed(self, data):
        if self.sender == True:
            try:
                pyperclip.copy(self.destinationString_Re + self.actionString_Proceed + ";"+data)
            except pyperclip.PyperclipException as pe:
                print(f"Fehler beim schreiben in die Zwischenablage: {str(pe)}")
            result = self.wait()
            return result
            
        else:
            try:
                pyperclip.copy(self.destinationString_Se + self.actionString_Proceed)
            except pyperclip.PyperclipException as pe:
                print(f"Fehler beim schreiben in die Zwischenablage: {str(pe)}")
            result = self.wait()
            return result 
        
    def wait(self):
        #Pufferzeit
        time.sleep(self.configHandler.getConfigdata(configdataHandler.BUFFER_TIME))
        
        #Erprobungsversuch - Diesen Block weglassen / TmpClip mit Standardstring initialisieren
        '''
        try:
            self.tmpClip = pyperclip.paste()
        except pyperclip.PyperclipWindowsException as wine:
            wineCounter += 1
            if self.configHandler.getConfigdata(configdataHandler.TRANSMISSION_RUNS) == True:
                print(f"PyperclipWindowsException: {str(wine)} raised zum %s. mal", wineCounter)
            if wineCounter < 5:
                time.sleep(1)
                self.tmpClip = pyperclip.paste()
            else:
                raise
        except pyperclip.PyperclipException as pe:
            print(f"Fehler beim lesen aus der Zwischenablage: {str(pe)}")
        '''
        self.tmpClip = "ini"

        loopCounter = 0
        toeCounter = 0
        wineCounter = 0
        while True:
            loopCounter += 1
            if self.goSleep == True:
                self.sleep()
                try:
                    pyperclip.copy("Dateiuebertragungstool")
                except pyperclip.PyperclipException as pe:
                    print(f"Fehler beim schreiben in die Zwischenablage: {str(pe)}")
            if self.tmpClip == self.destinationString_Re + self.actionString_StartReceiving and self.sender == False:
                try:
                    pyperclip.copy(self.destinationString_Se + self.actionString_StartSending)
                except pyperclip.PyperclipException as pe:
                    print(f"Fehler beim schreiben in die Zwischenablage: {str(pe)}")
                return self.wait()
            elif self.tmpClip == self.destinationString_Se + self.actionString_StartSending and self.sender == True:
                break
            elif self.tmpClip.split(";")[0] == self.destinationString_Re + self.actionString_Proceed and self.sender == False:
                return self.tmpClip.split(";")[1]
            elif self.tmpClip == self.destinationString_Se + self.actionString_Proceed and self.sender == True:
                break
            elif self.tmpClip == self.destinationString_Se + self.actionString_Finish and self.sender == True:
                break
            elif self.tmpClip == self.destinationString_Re + self.actionString_Finish and self.sender == False:
                try:
                    pyperclip.copy(self.destinationString_Se + self.actionString_Finish)
                except pyperclip.PyperclipException as pe:
                    print(f"Fehler beim schreiben in die Zwischenablage: {str(pe)}")
                return "exit"
            else:
                try:
                    self.tmpClip = pyperclip.waitForNewPaste(timeout=1)
                except pyperclip.PyperclipTimeoutException as toe:
                    toeCounter += 1
                    if self.configHandler.getConfigdata(configdataHandler.TRANSMISSION_RUNS) == True:
                        print(f"PyperclipTimeoutException: {str(toe)} raised zum %s. mal", toeCounter)
                    self.tmpClip = pyperclip.paste()
                    print("*** pyperclip.waitForNewPaste() Timeout raised in clipProtocol.wait() ***")
                except pyperclip.PyperclipWindowsException as wine:
                    wineCounter += 1
                    if self.configHandler.getConfigdata(configdataHandler.TRANSMISSION_RUNS) == True:
                        print(f"PyperclipWindowsException: {str(wine)} raised zum %s. mal", wineCounter)
                    if wineCounter < 5:
                        time.sleep(1)
                        self.tmpClip = pyperclip.paste()
                    else:
                        print("PyperclipWindowsException tritt zu oft auf")
                        raise
                except pyperclip.PyperclipException as pe:
                    raise
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
            print("Fehler beim schreiben in die Zwischenablage")
            raise
        self.wait()
        return