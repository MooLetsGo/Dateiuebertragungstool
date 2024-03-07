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
        except:
            print("*** ERROR: Fehler beim schreiben in die Zwischenablage; ID=clipProtocol.start() ***")
        return self.wait()
        
    def proceed(self, data):
        if self.sender == True:
            try:
                pyperclip.copy(self.destinationString_Re + self.actionString_Proceed + ";"+data)
                print("*** Datenblock in Zwischenablage kopiert ***")
            except:
                print("*** ERROR: Fehler beim schreiben in die Zwischenablage; ID=clipProtocol.proceed(toRe) ***")
            return self.wait()
            
        else:
            try:
                pyperclip.copy(self.destinationString_Se + self.actionString_Proceed)
            except:
                print("*** ERROR: Fehler beim schreiben in die Zwischenablage; ID=clipProtocol.proceed(toSe) ***")
            return self.wait() 
        
    def wait(self):
        print("*** Wait... ***")
        #Pufferzeit
        time.sleep(self.configHandler.getConfigdata("bufferTime"))
        try:
            self.tmpClip = pyperclip.paste()
        except:
            print("*** ERROR: Fehler beim lesen aus der Zwischenablage; ID=clipProtocol.wait() ***")
        while True:
            if self.goSleep == True:
                print("*** Local receiveFile Function went sleep ***")
                self.sleep()
                print("*** Local receiveFile Function woke up ***")
                try:
                    pyperclip.copy("lootsgnugartrebeuietaD")
                except:
                    print("*** ERROR: Fehler beim schreiben in die Zwischenablage; ID=clipProtocol.wait(initString) ***")
            if self.tmpClip == self.destinationString_Re + self.actionString_StartReceiving and self.sender == False:
                try:
                    pyperclip.copy(self.destinationString_Se + self.actionString_StartSending)
                except:
                    print("*** ERROR: Fehler beim schreiben in die Zwischenablage; ID=clipProtocol.wait(toSe) ***")
                return self.wait()
            elif self.tmpClip == self.destinationString_Se + self.actionString_StartSending and self.sender == True:
                break
            elif self.tmpClip.split(";")[0] == self.destinationString_Re + self.actionString_Proceed and self.sender == False:
                return self.tmpClip.split(";")[1]
            elif self.tmpClip == self.destinationString_Se + self.actionString_Proceed and self.sender == True:
                break
            elif self.tmpClip == self.destinationString_Re + self.actionString_Finish and self.sender == False:
                return "exit"
            else:
                try:
                    self.tmpClip = pyperclip.waitForNewPaste(timeout=1)
                except:
                    self.tmpClip = pyperclip.paste()
                    print("*** pyperclip.waitForNewPaste() Timeout raised in clipProtocol.wait() ***")
        return ""
    
    def sleep(self):
        while True:
            self.sleeps = True
            if self.configHandler.getConfigdata("transmissionRuns") == False:
                self.goSleep = False
                self.sleeps = False
                break
            time.sleep(1)
        return
    
    def finish(self):
        try:
            print("*** Alle Segmente wurden versendet ***")
            pyperclip.copy(self.destinationString_Re + self.actionString_Finish)
        except:
            print("*** ERROR: Fehler beim schreiben in die Zwischenablage; ID=clip.Protocol.finish(toRe) ***")
        return