import base64
import hashlib
import filetype
import logging
from clipProtocol import clipProtocol
from configdataHandler import configdataHandler


def sendFile(configHandler: configdataHandler, protocol: clipProtocol):
    #----------------------------Init Variablen--------------------------#
    inputFile = configHandler.getConfigdata(configdataHandler.INPUT_FILE)
    blockLength = configHandler.getConfigdata(configdataHandler.BLOCK_LENGTH)
    segmentsToSend = configHandler.getConfigdata(configdataHandler.SEGMENTS_TO_SEND)
    nextBlockPos = 0
    segmentNumber = 0
    inputfileName = ""

    #-----------------------Übertragung Startvorgang---------------------#
    protocol.start()
    
    #-------------------Übertragung Datei Informationen------------------#
    #Vorgabe der Segmentgröße
    protocol.proceed(str(blockLength))
    #Ermittlung und Prüfung des Dateityps
    kind = filetype.guess(inputFile)
    if kind is None:
        print('*** ERROR Invalid filetype ! ***')
        exit(1)     
    else:
        inputfileType = kind.extension 
    #Ermittlung des Dateinamens
    inputFilePointSplitted = inputFile.split('.')
    for v in inputFilePointSplitted[0:len(inputFilePointSplitted)-1]:
        inputfileName += (v + ".")
    pathList = inputfileName.split('/')
    inputfileName = pathList[len(pathList)-1]
    outputFileName = inputfileName + inputfileType
    protocol.proceed(outputFileName)
    #Prüfsummenberechnung Inputfile
    with open(inputFile, 'rb') as binary_inputFile:
        binaryData = binary_inputFile.read()
        checksumInput = hashlib.sha256(binaryData).hexdigest()
    protocol.proceed(checksumInput)
    protocol.proceed(str(segmentsToSend))

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
        #Zuweisung von segmentNumber an configHandler.segmentsSended
        configHandler.setConfigdata(configdataHandler.SEGMENTS_SENDED,segmentNumber)
        #B64 kodierten Textblock in die Zwischenablage schreiben
        print("Segment %s an clipProtocol.proceed() uebergeben", segmentNumber)
        protocol.proceed(utf8B64_blockData)

    print("Senden beendet")
    configHandler.setConfigdata(configdataHandler.TRANSMISSION_RUNS,False)
    return