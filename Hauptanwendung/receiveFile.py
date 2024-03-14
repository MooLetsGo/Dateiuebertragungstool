import base64
import os.path
import hashlib
import pyperclip
from clipProtocol import clipProtocol
from configdataHandler import configdataHandler
import logging



def receiveFile(configHandler: configdataHandler, protocol: clipProtocol):
    logger = logging.getLogger("receiveEvents_logger")
    try:
        pyperclip.copy("Dateiuebertragungstool")
    except pyperclip.PyperclipException:
        logger.exception("Fehler beim schreiben in die Zwischenablage")
        raise
    logger.info("Initialisierungsstring 'Dateiuebertragungstool' in die Zwischenablage kopiert")
    while True:
        logger.info("Empfangen gestartet")
        #----------------------------Init Variablen--------------------------#
        nextBlockPos = 0
        segmentNumber = 0
        value = ""

        #-----------------------Übertragung Startvorgang---------------------#
        value = protocol.wait()
        logger.info("clipProtocol.wait() verlassen")
        
        configHandler.setConfigdata( configdataHandler.TRANSMISSION_RUNS,True)
        #----------------Init Variablen für configdata Werte-----------------#
        outputPath = configHandler.getConfigdata(configdataHandler.OUTPUT_PATH)
        blockLength = int(value)
        if configHandler.getConfigdata(configdataHandler.BLOCK_LENGTH) != blockLength:
            configHandler.setConfigdata(configdataHandler.BLOCK_LENGTH,blockLength)
        logger.info("Segmentgroesse: %s empfangen", blockLength)
        value = protocol.proceed(None)
        logger.info("clipProtocol.wait() verlassen")
        #-------------------Übertragung Datei Informationen------------------#
        outputFileName = value
        logger.info("Outputfile Name: %s empfangen", value)
        value = protocol.proceed(None)
        logger.info("clipProtocol.wait() verlassen")
        checksumInput = value
        logger.info("Prüfsumme der Originaldatei: %s empfangen", value)
        value = protocol.proceed(None)
        logger.info("clipProtocol.wait() verlassen")
        configHandler.setConfigdata(configdataHandler.SEGMENTS_TO_SEND,int(value))
        logger.info("Segmentanzahl gesamt: %s empfangen", value)
        value = protocol.proceed(None)
        logger.info("clipProtocol.wait() verlassen")
        #--------------------Übertragung Inputfile Daten---------------------#
        while True:
            if value == "exit":
                logger.info("Empfangen beendet")
                break
            segmentNumber += 1
            utf8B64_blockData = value
            logger.info("Segment %s empfangen: ", value[:25])
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
            logger.info("Segment %s in neue Datei geschrieben", segmentNumber)
            #Laufvariablen neu berechnen
            nextBlockPos = nextBlockPos + blockLength
            #Zuweisung von segmentNumber an configHandler.segmentsSended
            configHandler.setConfigdata(configdataHandler.SEGMENTS_SENDED,segmentNumber)
            #Warten auf nächstes Segment
            value = protocol.proceed(None)
            logger.info("clipProtocol.wait() verlassen")
            
        #Prüfsummenberechnung OutputFile
        with open(outputPath + '/' + outputFileName, 'rb') as binary_outputFile: 
                binaryData = binary_outputFile.read()
                checksumOutput = hashlib.sha256(binaryData).hexdigest()
        if checksumInput == checksumOutput:
            logger.info("Dateiuebertragung war erfolgreich")
            print("*** Dateiuebertragung erfolgreich beendet ***")
        else:
            logger.info("Uebertragene Datei ungleich Originaldatei")
            print("*** ERROR: Uebertragene Datei ungleich Originaldatei ***")

        configHandler.setConfigdata(configdataHandler.TRANSMISSION_RUNS,False)