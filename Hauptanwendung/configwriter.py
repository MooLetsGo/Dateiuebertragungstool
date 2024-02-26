from configparser import ConfigParser


def configwriter():

    config = ConfigParser()

    config["DEFAULT"] = {
        "blockLength": 1048576,
        "outputPath":  "C:/Users/morit/OneDrive/Studium/6_Semester/Studienarbeit 2/Umsetzung/VSCode/Dateiuebertragungstool/Outputfile",
        "bufferTime": 0.8,
    }

    try:
        with open("dateiuebertragungsTool.ini", "w") as file:
            config.write(file)
    except:
        exit(1)

def modifyConfig():
    #ToDo#
    return