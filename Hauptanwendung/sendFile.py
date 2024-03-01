import base64
import hashlib
import filetype
from clipProtocol import clipProtocol
from configdataHandler import configdataHandler


def sendFile(configHandler: configdataHandler):

    inputFile = configHandler.getConfigdata(3)
    blockLength = configHandler.getConfigdata(0)
    nextBlockPos = 0
    segmentNumber = 0

    #-----------------------Übertragung Startvorgang---------------------# 
    protocol = clipProtocol(configHandler)
    protocol.sender = True
    protocol.start()
    
    #-------------------Übertragung Datei Informationen------------------#
    #Ermittlung und Prüfung des Dateityps
    kind = filetype.guess(inputFile)
    if kind is None:
        print('*** ERROR Invalid filetype ! ***')
        exit(1)     
    else:
        inputfileType = kind.extension 
    #Ermittlung des Dateinamens
    pathList = inputFile.split('.')[0].split('/')
    inputfileName = pathList[len(pathList)-1]

    outputFileName = inputfileName + "." + inputfileType
    protocol.proceed(outputFileName)
    #Prüfsummenberechnung Inputfile
    with open(inputFile, 'rb') as binary_inputFile:
        binaryData = binary_inputFile.read()
        checksumInput = hashlib.sha256(binaryData).hexdigest()
    protocol.proceed(checksumInput)

    #-------------------Übertragung Inputfile Daten---------------------#
    #InputFile blockweise Einlesen und aus den Datenblöcken B64 kodierten Text generieren
    while True:
        #Binärdatenblock des InputFiles generieren 
        segmentNumber += 1
        with open(inputFile, 'rb') as binary_inputFile:
            binary_inputFile.seek(nextBlockPos,0)
            binary_blockData = binary_inputFile.read(blockLength)
            if not binary_blockData:
                protocol.finish()
                break
        #Laufvariablen neu berechnen
        nextBlockPos = nextBlockPos + blockLength
        #Binärdatenblock B64 kodieren
        binaryB64_blockData = base64.b64encode(binary_blockData)
        #B64 kodierten Binärdatenblock in Text umwandeln 
        utf8B64_blockData = binaryB64_blockData.decode('utf-8')

        configdataHandler.setConfigdata(configHandler,5,segmentNumber)
        #B64 kodierten Textblock in die Zwischenablage schreiben
        protocol.proceed(utf8B64_blockData)
    
    return