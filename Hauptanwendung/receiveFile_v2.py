import base64
import os.path
import sys
import hashlib
import pyperclip
from clipProtocol_v0 import clipProtocol



def receiveFile():
    outputPath = "C:/Users/morit/OneDrive/Studium/6_Semester/Studienarbeit 2/Umsetzung/VSCode/Dateiuebertragungstool/Outputfile" #Hartkodiert!!

    blockLength = 1048576 #1MB #Hartkodiert
    nextBlockPos = 0
    segmentNumber = 0

    #Input Pfad auf Existenz überprüfen
    if not(os.path.exists(outputPath)):
        print('*** Warning:  Input file ' +outputPath+' does not exist! ***')
        sys.exit(2)
    
    #-----------------------Übertragung Startvorgang---------------------#
    #Protokoll - Vorgang abgestimmt mit der Receive Funktion starten
    try:
        pyperclip.copy("")
    except:
        print("Fehler beim schreiben in die Zwischenablage; ID=receiveFile("")")
    protocol2 = clipProtocol()
    v = protocol2.wait()

    #-------------------Übertragung Datei Informationen------------------#
    outputFileName = v
    v= protocol2.proceed(None)

    while True:
        if v == "exit":
            break
        segmentNumber += 1
        
        utf8B64_blockData = v
        binaryB64_blockData = utf8B64_blockData.encode('utf-8')
        
        #B64 kodierten Binärdatenblock B64 dekodieren
        binary_blockData = base64.b64decode(binaryB64_blockData)

        #Prüfsummenberechnung des Binärdatenblocks
        checksum1 = hashlib.sha256(binary_blockData).hexdigest()
        
        #Wenn schon eine (kaputte) Datei da ist, diese löschen und eine neue leere erstellen
        #Neue Datei Erzeugen
        if not os.path.exists(outputPath+'/'+outputFileName): 
            with open(outputPath+'/'+outputFileName, 'wb'): 
                pass
        #Binärdatenblock an passender Stelle in Neuer Datei einfügen 
        #Datei im Modus 'r+b' öffnen, sodass sowohl aus der Datei gelesen als auch in die Datei geschrieben werden kann.
        #Das lesen ist wichtig, damit die seek() Funktion funktioniert 
        with open(outputPath+'/'+outputFileName, 'r+b') as outputFile: 
            outputFile.seek(nextBlockPos,0)
            outputFile.write(binary_blockData)
        
        print("Datenblock in neue Datei geschrieben")

        #Laufvariablen neu berechnen
        nextBlockPos = nextBlockPos + blockLength

        v = protocol2.proceed(None)
        

    #Prüfsummenberechnung OutputFile
    with open(outputPath+'/'+outputFileName, 'rb') as binary_outputFile: 
            binaryData = binary_outputFile.read()
            checksum = hashlib.sha256(binaryData).hexdigest()