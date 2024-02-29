import pyperclip
import time

class clipProtocol:
    def __init__(self, bufferTime:float):
        self.sender = False

        self.actionString_StartSending = "StartSending"
        self.actionString_StartReceiving = "StartReceiving"
        self.actionString_Proceed = "Proceed"
        self.actionString_Finish = "finish"

        self.destinationString_Re = "toRe_"
        self.destinationString_Se = "toSe_"

        self.bufferTime = bufferTime


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
        time.sleep(self.bufferTime)
        try:
            tmpClip = pyperclip.paste()
        except:
            print("*** ERROR: Fehler beim lesen aus der Zwischenablage; ID=clipProtocol.wait() ***")
        while True:
            if tmpClip == self.destinationString_Re + self.actionString_StartReceiving and self.sender == False:
                try:
                    pyperclip.copy(self.destinationString_Se + self.actionString_StartSending)
                except:
                    print("*** ERROR: Fehler beim schreiben in die Zwischenablage; ID=clipProtocol.wait(toSe) ***")
                return self.wait()
            elif tmpClip == self.destinationString_Se + self.actionString_StartSending and self.sender == True:
                break
            elif tmpClip.split(";")[0] == self.destinationString_Re + self.actionString_Proceed and self.sender == False:
                return tmpClip.split(";")[1]
            elif tmpClip == self.destinationString_Se + self.actionString_Proceed and self.sender == True:
                break
            elif tmpClip == self.destinationString_Re + self.actionString_Finish and self.sender == False:
                #evtl geeigneterer Text
                return "exit"
            else:
                try:
                    tmpClip = pyperclip.waitForNewPaste(timeout=1)
                except:
                    tmpClip = pyperclip.paste()
                    print("*** pyperclip.waitForNewPaste() Timeout raised in clipProtocol.wait() ***")      
        #Evtl. schöner lösen
        return ""
    
    def finish(self):
        try:
            pyperclip.copy(self.destinationString_Re + self.actionString_Finish)
        except:
            print("*** ERROR: Fehler beim schreiben in die Zwischenablage; ID=clip.Protocol.finish(toRe) ***")
        return