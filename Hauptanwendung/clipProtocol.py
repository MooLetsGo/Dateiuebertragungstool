import pyperclip
import time
from configdataHandler import configdataHandler

class clipProtocol:
    def __init__(self, configHandler: configdataHandler):
        self.sender = False

        self.tmpClip = ""

        self.actionString_StartSending = "StartSending"
        self.actionString_StartReceiving = "StartReceiving"
        self.actionString_Proceed = "Proceed"
        self.actionString_Finish = "finish"

        self.destinationString_Re = "toRe_"
        self.destinationString_Se = "toSe_"

        self.configHandler = configHandler


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
        if self.configHandler.stopEvent.is_set() and self.sender == False:
            return
        #Pufferzeit
        time.sleep(self.configHandler.getConfigdata(1))
        try:
            self.tmpClip = pyperclip.paste()
        except:
            print("*** ERROR: Fehler beim lesen aus der Zwischenablage; ID=clipProtocol.wait() ***")
        while True:
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
                #evtl geeigneterer Text
                return "exit"
            else:
                try:
                    self.tmpClip = pyperclip.waitForNewPaste(timeout=1)
                except:
                    self.tmpClip = pyperclip.paste()
                    print("*** pyperclip.waitForNewPaste() Timeout raised in clipProtocol.wait() ***")      
        #Evtl. schöner lösen
        return ""
    
    def finish(self):
        try:
            pyperclip.copy(self.destinationString_Re + self.actionString_Finish)
        except:
            print("*** ERROR: Fehler beim schreiben in die Zwischenablage; ID=clip.Protocol.finish(toRe) ***")
        return