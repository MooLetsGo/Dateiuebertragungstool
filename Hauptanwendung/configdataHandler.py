from configparser import ConfigParser
import threading

#blockLength = Index 0
#bufferTimer = Index 1
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
        self.stopEvent = threading.Event()
    
    def writeConfig(self):
        config = ConfigParser()
        config["SETTINGS"] = {
            "blockLength": self.blockLength,
            "bufferTime": self.bufferTime,
            "outputPath": self.outputPath,
        }
        try:
            with open("dateiuebertragungsTool.ini", "w") as file:
                config.write(file)
                return
        except:
            exit(1)
    
    #Errorhandlich noch machen, wenn value Typ und Index nicht zusammenpassen
    def setConfigdata(self, index: int, value):
        if index == 0:
            with self.lock:
                self.blockLength = value
            self.writeConfig()
        elif index == 1:
            with self.lock:
                self.bufferTime = value
            self.writeConfig()
        elif index == 2:
            with self.lock:
                self.outputPath = value
            self.writeConfig()
        elif index == 3:
            with self.lock:
                self.inputFile = value
        elif index == 4:
            with self.lock:
                self.segmentsToSend = value
        elif index == 5:
            with self.lock:
                self.segmentsSended = value
        return

    def getConfigdata(self, index: int):
        if index == 0:
            with self.lock:
                return self.blockLength
        elif index == 1:
            with self.lock:
                return self.bufferTime
        elif index == 2:
            with self.lock:
                return self.outputPath
        elif index == 3:
            with self.lock:
                return self.inputFile
        elif index == 4:
            with self.lock:
                return self.segmentsToSend
        elif index == 5:
            with self.lock:
                return self.segmentsSended
        return