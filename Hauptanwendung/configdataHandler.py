from configparser import ConfigParser
import threading

#blockLength = Index 0
#bufferTime = Index 1
#outputPath = Index 2
#inputFile = Index 3
#segmentsToSend = Index 4
#segmentsSended = Index 5


class configdataHandler:
    def __init__(self, default_blockLength: int, default_bufferTime: float, default_outputPath: str ):
        self.blockLength = default_blockLength
        self.bufferTime = default_bufferTime
        self.inputFile = ""
        self.outputPath = default_outputPath
        self.segmentsToSend = 0
        self.segmentsSended = 0
        self.lock = threading.Lock()
        self.transmissionRuns = False
    
    def writeConfigToIni(self):
        config = ConfigParser()
        config["SETTINGS"] = {
            "blockLength": self.getConfigdata("blockLength"),
            "bufferTime": self.getConfigdata("bufferTime"),
            "outputPath": self.getConfigdata("outputPath"),
        }
        try:
            with open("dateiuebertragungsTool.ini", "w") as file:
                config.write(file)
                return
        except:
            exit(1)

    def setConfigdata(self, configAttr: str, value):
        with self.lock:
            setattr(self,configAttr,value)
        if configAttr == "blockLength" or configAttr == "bufferTime" or configAttr == "outputPath":
            self.writeConfigToIni()
        return

    def getConfigdata(self, configAttr: str):
        with self.lock:
            return getattr(self,configAttr)