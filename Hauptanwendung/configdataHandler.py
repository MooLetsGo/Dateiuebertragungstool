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
    
    def writeConfigToIni(self):
        config = ConfigParser()
        config["SETTINGS"] = {
            "blockLength": self.getConfigdata(0),
            "bufferTime": self.getConfigdata(1),
            "outputPath": self.getConfigdata(2),
        }
        try:
            with open("dateiuebertragungsTool.ini", "w") as file:
                config.write(file)
                return
        except:
            exit(1)
    
    #Errorhandlich noch machen, wenn value Typ und Index nicht zusammenpassen
    def setConfigdata(self, index: int, value):
        configAttributes = {
            0: "blockLength",
            1: "bufferTime",
            2: "outputPath",
            3: "inputFile",
            4: "segmentsToSend",
            5: "segmentsSended",
        }
        with self.lock:
            if index in configAttributes:
                setattr(self,configAttributes[index],value)
                if index in [0,1,2]:
                    self.writeConfigToIni()
        return

    def getConfigdata(self, index: int):
        configAttributes = {
            0: self.blockLength,
            1: self.bufferTime,
            2: self.outputPath,
            3: self.inputFile,
            4: self.segmentsToSend,
            5: self.segmentsSended,
        }
        with self.lock:
            print(configAttributes.get(index,None))
            return configAttributes.get(index,None)