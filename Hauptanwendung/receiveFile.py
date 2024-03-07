import base64
import os.path
import hashlib
import pyperclip
from clipProtocol import clipProtocol
from configdataHandler import configdataHandler



def receiveFile(configHandler: configdataHandler, protocol: clipProtocol):
    try:
        pyperclip.copy("lootsgnugartrebeuietaD")
    except:
        print("*** ERROR: Fehler beim schreiben in die Zwischenablage; ID=receiveFile(initString) ***")
    while True:
        #----------------------------Init Variablen--------------------------#
        nextBlockPos = 0
        segmentNumber = 0
        value = ""

        #-----------------------Übertragung Startvorgang---------------------#
        value = protocol.wait()
        
        configHandler.setConfigdata("tranmissionRuns",True)
        #----------------Init Variablen für configdata Werte-----------------#
        outputPath = configHandler.getConfigdata("outputPath")
        blockLength = int(value)
        if configHandler.getConfigdata("blockLength") != blockLength:
            configHandler.setConfigdata("blockLength",blockLength)
        value = protocol.proceed(None)

        #-------------------Übertragung Datei Informationen------------------#
        outputFileName = value
        value = protocol.proceed(None)
        checksumInput = value
        value = protocol.proceed(None)
        configHandler.setConfigdata("segmentsToSend",int(value))
        value = protocol.proceed(None)

        #--------------------Übertragung Inputfile Daten---------------------#
        while True:
            if value == "exit":
                break
            segmentNumber += 1
            utf8B64_blockData = value
            #Text in B64 kodierten Binärdatenblock umwandeln
            binaryB64_blockData = utf8B64_blockData.encode('utf-8')
            #B64 kodierten Binärdatenblock B64 dekodieren
            binary_blockData = base64.b64decode(binaryB64_blockData)
            #Neue leere Datei mit richtigem Namen und Typ Erzeugen
            if not os.path.exists(outputPath + '/' + outputFileName): 
                with open(outputPath + '/' + outputFileName, 'wb'): 
                    pass
            #Binärdatenblock an passender Stelle in Neuer Datei einfügen 
            #Datei im Modus 'r+b' öffnen, sodass sowohl aus der Datei gelesen als auch in die Datei geschrieben werden kann.
            #Das lesen ist wichtig, damit die seek() Funktion funktioniert 
            with open(outputPath + '/' + outputFileName, 'r+b') as outputFile: 
                outputFile.seek(nextBlockPos,0)
                outputFile.write(binary_blockData)
            print("*** Datenblock in neue Datei geschrieben ***")
            #Laufvariablen neu berechnen
            nextBlockPos = nextBlockPos + blockLength
            #Zuweisung von segmentNumber an configHandler.segmentsSended
            configHandler.setConfigdata("segmentsSended",segmentNumber)
            #Warten auf nächstes Segment
            value = protocol.proceed(None)
            
        #Prüfsummenberechnung OutputFile
        with open(outputPath + '/' + outputFileName, 'rb') as binary_outputFile: 
                binaryData = binary_outputFile.read()
                checksumOutput = hashlib.sha256(binaryData).hexdigest()
        if checksumInput == checksumOutput:
            print("*** Dateiuebertragung erfolgreich beendet ***")
        else:
            print("*** ERROR: Uebertragene Datei ungleich Originaldatei ***")

        configHandler.setConfigdata("transmissionRuns",False)