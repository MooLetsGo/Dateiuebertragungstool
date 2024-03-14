from configparser import ConfigParser
import threading

class configdataHandler:

    BLOCK_LENGTH = "blockLength"
    BUFFER_TIME = "bufferTime"
    INPUT_FILE = "inputFile"
    OUTPUT_PATH = "outputPath"
    SEGMENTS_TO_SEND = "segmentsToSend"
    SEGMENTS_SENDED = "segmentsSended"
    TRANSMISSION_RUNS = "transmissionRuns"
    INI_FILE_NAME = "dateiuebertragungsTool.ini"
    INI_FILE_CONFIG_NAME = "SETTINGS"

    _CONFIG_HANDLER_ATTRIBUTES = {
        BLOCK_LENGTH,
        BUFFER_TIME,
        INPUT_FILE,
        OUTPUT_PATH,
        SEGMENTS_TO_SEND,
        SEGMENTS_SENDED,
        TRANSMISSION_RUNS,
        INI_FILE_NAME,
        INI_FILE_CONFIG_NAME,
    }

    _CONFIG_HANDLER_INI_ATTRIBUTES ={
        BLOCK_LENGTH,
        BUFFER_TIME,
        OUTPUT_PATH,
    }

    def __init__(self, default_blockLength: int, default_bufferTime: float, default_outputPath: str ):
        self.blockLength = default_blockLength
        self.bufferTime = default_bufferTime
        self.outputPath = default_outputPath
        self.inputFile = ""
        self.segmentsToSend = 0
        self.segmentsSended = 0
        self.transmissionRuns = False
        self.lock = threading.Lock()
        
    
    def writeConfigToIni(self):
        config = ConfigParser()
        config[self.INI_FILE_CONFIG_NAME] = {
            self.BLOCK_LENGTH: self.getConfigdata(self.BLOCK_LENGTH),
            self.BUFFER_TIME: self.getConfigdata(self.BUFFER_TIME),
            self.OUTPUT_PATH: self.getConfigdata(self.OUTPUT_PATH),
        }
        try:
            with open(self.INI_FILE_NAME, "w") as file:
                config.write(file)
                return
        except Exception as e:
            print("*** ERROR: INI-Datei konnte nicht aktualisiert werden ***")
            raise

    def setConfigdata(self, configHandlerAttr: str, value):
        if configHandlerAttr not in self._CONFIG_HANDLER_ATTRIBUTES:
            raise ValueError(f"Configdata Handler Objekt hat kein solches Attribut: {configHandlerAttr}")
        with self.lock:
            setattr(self,configHandlerAttr,value)
        if configHandlerAttr in self._CONFIG_HANDLER_INI_ATTRIBUTES:
            self.writeConfigToIni()
        return

    def getConfigdata(self, configHandlerAttr: str):
        if configHandlerAttr not in self._CONFIG_HANDLER_ATTRIBUTES:
            raise ValueError(f"Configdata Handler Objekt hat kein solches Attribut: {configHandlerAttr}")
        with self.lock:
            return getattr(self,configHandlerAttr)