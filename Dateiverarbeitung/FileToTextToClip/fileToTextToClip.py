import filetype
import base64
import sys
import os.path

import pyperclip

#----------------------------------------------------------------------------------------

class bcolors:
    HEADER     = '\033[95m'
    OKBLUE     = '\033[94m'
    OKCYAN     = '\033[96m'
    OKGREEN    = '\033[92m'
    WARNING    = '\033[93m'
    FAIL       = '\033[91m'
    ENDC       = '\033[0m'
    BOLD       = '\033[1m'
    UNDERLINE  = '\033[4m'
    CEND       = '\33[0m'

    CBOLD      = '\33[1m'
    CITALIC    = '\33[3m'
    CURL       = '\33[4m'
    CBLINK     = '\33[5m'
    CBLINK2    = '\33[6m'
    CSELECTED  = '\33[7m'

    CBLACK     = '\33[30m'
    CRED       = '\33[31m'
    CGREEN     = '\33[32m'
    CYELLOW    = '\33[33m'
    CBLUE      = '\33[34m'
    CVIOLET    = '\33[35m'
    CBEIGE     = '\33[36m'
    CWHITE     = '\33[37m'

    CBLACKBG   = '\33[40m'
    CREDBG     = '\33[41m'
    CGREENBG   = '\33[42m'
    CYELLOWBG  = '\33[43m'
    CBLUEBG    = '\33[44m'
    CVIOLETBG  = '\33[45m'
    CBEIGEBG   = '\33[46m'
    CWHITEBG   = '\33[47m'

    CGREY      = '\33[90m'
    CRED2      = '\33[91m'
    CGREEN2    = '\33[92m'
    CYELLOW2   = '\33[93m'
    CBLUE2     = '\33[94m'
    CVIOLET2   = '\33[95m'
    CBEIGE2    = '\33[96m'
    CWHITE2    = '\33[97m'

    CGREYBG    = '\33[100m'
    CREDBG2    = '\33[101m'
    CGREENBG2  = '\33[102m'
    CYELLOWBG2 = '\33[103m'
    CBLUEBG2   = '\33[104m'
    CVIOLETBG2 = '\33[105m'
    CBEIGEBG2  = '\33[106m'
    CWHITEBG2  = '\33[107m'

#----------------------------------------------------------------------------------------

#Init Variablen
inputfile_name = 'C:\\Users\\morit\\OneDrive\\Studium\\6. Semester\\Studienarbeit 2\\Umsetzung\\VSCode\\Dateiuebertragungstool\\Dateiverarbeitung\\Testdateien\\excelTest.xlsx'

data_url = ''
prefix = ''
postfix_1 = '"'
postfix_2 = '>'

#----------------------------------------------------------------------------------------

#Pfad von "inputfile" wird auf Existenz überprüft
if not(os.path.exists(inputfile_name)):
    print(f"{bcolors.WARNING}")
    print('Warning:  Input file ' + '\''+inputfile_name + '\''+' does not exist!')
    print(f"{bcolors.ENDC}")
    sys.exit(2)
   
#----------------------------------------------------------------------------------------

#Ermittlung und Prüfung des Dateityps --> HTML-Präfix generieren (DateiEndung/MIMEType)
kind = filetype.guess(inputfile_name)
if kind is None:
    print(f"{bcolors.WARNING}\r\n*** ERROR Invalid filetype ! ***\r\n{bcolors.ENDC}")
    sys.exit(2)     
else:
    prefix = '<src="data:' + kind.extension + ';charset=utf-8;base64,' #DateiEndung wird angehängt (nicht der MIMEType)

#----------------------------------------------------------------------------------------

#Datei mit B64-Verfahren in Text konvertieren, Prä- und Postfixe anhängen --> data_url
with open(inputfile_name, 'rb') as binary_file:
    binary_file_data = binary_file.read()
    base64_encoded_data = base64.b64encode(binary_file_data)
    
    data_url = prefix + base64_encoded_data.decode('utf-8')+postfix_1+postfix_2

#B64 kodierten Text der Datei in die Zwischenablage speichern
pyperclip.copy(data_url)
print(f"{bcolors.OKGREEN}\r\n*** B64 block successfully copied to clipboard !!! ***\r\n{bcolors.ENDC}")

#Kodierte Datei wird zu Testzwecken als Textdatei im Ordner "Textdateien" erzeugt
outputfile_name = 'C:\\Users\\morit\\OneDrive\\Studium\\6. Semester\\Studienarbeit 2\\Umsetzung\\VSCode\\Dateiuebertragungstool\\Dateiverarbeitung\\Testdateien\\encodedFile.txt'
with open(outputfile_name, "w") as text_file:
        text_file.write(data_url)
        print(f"{bcolors.OKGREEN}\r\n*** Output filename successfully written !!! ***\r\n{bcolors.ENDC}")