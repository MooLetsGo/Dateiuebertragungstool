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

    CONFIG_HANDLER_ATTRIBUTES = {
        BLOCK_LENGTH,
        BUFFER_TIME,
        INPUT_FILE,
        OUTPUT_PATH,
        SEGMENTS_TO_SEND,
        SEGMENTS_SENDED,
        TRANSMISSION_RUNS,
    }

    CONFIG_HANDLER_INI_ATTRIBUTES ={
        BLOCK_LENGTH,
        BUFFER_TIME,
        OUTPUT_PATH,
    }

    def __init__(self, default_blockLength: int, default_bufferTime: float, default_outputPath: str ):
        self.blockLength = default_blockLength
        self.bufferTime = default_bufferTime
        self.inputFile = ""
        self.outputPath = default_outputPath
        self.segmentsToSend = 0
        self.segmentsSended = 0
        self.transmissionRuns = False
        self.lock = threading.Lock()
        
    
    def writeConfigToIni(self):
        config = ConfigParser()
        config["SETTINGS"] = {
            "blockLength": self.getConfigdata(self.BLOCK_LENGTH),
            "bufferTime": self.getConfigdata(self.BUFFER_TIME),
            "outputPath": self.getConfigdata(self.OUTPUT_PATH),
        }
        try:
            with open("dateiuebertragungsTool.ini", "w") as file:
                config.write(file)
                return
        except:
            exit(1)

    def setConfigdata(self, configHandlerAttr: str, value):
        if configHandlerAttr not in self.CONFIG_HANDLER_ATTRIBUTES:
            raise ValueError(f"Object doesnt have this attribute: {configHandlerAttr}")
        with self.lock:
            setattr(self,configHandlerAttr,value)
        if configHandlerAttr in self.CONFIG_HANDLER_INI_ATTRIBUTES:
            self.writeConfigToIni()
        return

    def getConfigdata(self, configHandlerAttr: str):
        if configHandlerAttr not in self.CONFIG_HANDLER_ATTRIBUTES:
            raise ValueError(f"Object doesnt have this attribute: {configHandlerAttr}")
        with self.lock:
            return getattr(self,configHandlerAttr)