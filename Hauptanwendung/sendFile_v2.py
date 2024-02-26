import base64
import os.path
import sys
import hashlib
import filetype
from clipProtocol_v0 import clipProtocol



             
          


def sendFile(inputFile:str, blockLength:int, bufferTime:float):
    #inputFile = "C:/Users/morit/OneDrive/Studium/6_Semester/Studienarbeit 2/Umsetzung/VSCode/Testen/Testen/InputFiles/Cinebench2024_win_x86_64.zip"
    #inputFile = "C:/Users/morit/OneDrive/Studium/6_Semester/Studienarbeit 2/Umsetzung/VSCode/Testen/Testen/InputFiles/VSCode-win32-x64-1.85.1.zip"
    #inputFile = "C:/Users/morit/OneDrive/Studium/6_Semester/Studienarbeit 2/Umsetzung/VSCode/Testen/Testen/InputFiles/Konrad_Moritz_2023-10-10_11-47.xlsx" #Hartkodiert!!

    #blockLength = 1048576 #1MB #Hartkodiert!!
    segmentNumber = 0
    nextBlockPos = 0

    #Input Pfad auf Existenz überprüfen
    if not(os.path.exists(inputFile)):
        print('*** Warning:  Input file ' +inputFile+' does not exist! ***')
        sys.exit(2)
    
    #Prüfsummenberechnung Inputfile
    with open(inputFile, 'rb') as binary_inputFile:
        binaryData = binary_inputFile.read()
        checksum = hashlib.sha256(binaryData).hexdigest()

    #-----------------------Übertragung Startvorgang---------------------# 
    protocol1 = clipProtocol(bufferTime)
    protocol1.sender = True
    #Protokoll - Vorgang abgestimmt mit der Receive Funktion starten
    protocol1.start()
    

    #-------------------Übertragung Datei Informationen------------------#
    #Ermittlung und Prüfung des Dateityps
    kind = filetype.guess(inputFile)
    if kind is None:
        print('*** ERROR Invalid filetype ! ***')
        sys.exit(2)     
    else:
        inputfileType = kind.extension 
    #Ermittlung des Dateinamens
    pathList = inputFile.split('.')[0].split('/')
    inputfileName = pathList[len(pathList)-1]

    outputFileName = inputfileName + "." + inputfileType
    protocol1.proceed(outputFileName)

    #InputFile blockweise Einlesen und aus den Datenblöcken B64 kodierten Text generieren
    while True:
        #Binärdatenblock des InputFiles generieren 
        segmentNumber += 1
        with open(inputFile, 'rb') as binary_inputFile:
            binary_inputFile.seek(nextBlockPos,0)
            binary_blockData = binary_inputFile.read(blockLength)
            if not binary_blockData:
                protocol1.finish()
                break
        #Laufvariablen neu berechnen
        nextBlockPos = nextBlockPos + blockLength
        #Prüfsummenberechnung des Binärdatenblocks
        checksum1 = hashlib.sha256(binary_blockData).hexdigest()
        #Binärdatenblock B64 kodieren
        binaryB64_blockData = base64.b64encode(binary_blockData)
        #B64 kodierten Binärdatenblock in Text umwandeln 
        utf8B64_blockData = binaryB64_blockData.decode('utf-8')
        #B64 kodierten Textblock in die Zwischenablage schreiben
        protocol1.proceed(utf8B64_blockData)