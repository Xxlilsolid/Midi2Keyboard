import os
import datetime
import ast

if "__main__" == __name__:
    print("This is a module silly")
else:
    class Log:
        modulever = 0.1
        digitconvert = {"0": "00",
                        "1": "01",
                        "2": "02",
                        "3": "03",
                        "4": "04",
                        "5": "05",
                        "6": "06",
                        "7": "07",
                        "8": "08",
                        "9": "09",
                        "10": "10",
                        "11": "11",
                        "12": "12",
                        "13": "13",
                        "14": "14",
                        "15": "15",
                        "16": "16",
                        "17": "17",
                        "18": "18",
                        "19": "19",
                        "20": "20",
                        "21": "21",
                        "22": "22",
                        "23": "23",
                        "24": "24",
                        "25": "25",
                        "26": "26",
                        "27": "27",
                        "28": "28",
                        "29": "29",
                        "30": "30",
                        "31": "31",
                        "32": "32",
                        "33": "33",
                        "34": "34",
                        "35": "35",
                        "36": "36",
                        "37": "37",
                        "38": "38",
                        "39": "39",
                        "40": "40",
                        "41": "41",
                        "42": "42",
                        "43": "43",
                        "44": "44",
                        "45": "45",
                        "46": "46",
                        "47": "47",
                        "48": "48",
                        "49": "49",
                        "50": "50",
                        "51": "51",
                        "52": "52",
                        "53": "53",
                        "54": "54",
                        "55": "55",
                        "56": '56',
                        "57": "57",
                        "58": "58",
                        "59": "59",
                        "60": "60"}

        def __init__(self, filedir, editmode=False):
            self.__filedir = filedir
            self.__absfiledir = os.path.abspath(self.__filedir)
            if editmode == True:
                return
            import filechecker
            filechecker.FileChecker().check_dir('./logs', True)
            creationdate = datetime.datetime.now()
            if filechecker.FileChecker().check_file(self.__filedir, False)[0] == "True": # Renames
                dateandtime = self.getheader()
                os.rename(self.__absfiledir, os.path.abspath("./logs/"+f"{self.digitconvert[str(dateandtime[2])]}.{self.digitconvert[str(dateandtime[1])]}.{str(dateandtime[0])} [{self.digitconvert[str(dateandtime[3])]}.{self.digitconvert[str(dateandtime[4])]}.{self.digitconvert[str(dateandtime[5])]}].log")) #Defo needs work
                filechecker.FileChecker().check_file(self.__filedir, True)
            else:  # Creates new file
                filechecker.FileChecker().check_file(self.__filedir, True)
            self.writelog({creationdate}, False)
            self.writelog(f"Loggy {self.modulever} has now been loaded", False)

            
        def writelog(self, contents, doprint=None):
            with open(self.__absfiledir, '+a') as file:
                file.write(f"{contents}\n")
            if doprint == True: print(contents)
            return 0

        def getheader(self): # Im going to sound incredibly stupid if this isnt what its called
            with open(self.__absfiledir, 'r') as file:
                datestring = file.readline()
                datestring = datestring.removeprefix("{datetime.datetime")
                datestring = datestring.removesuffix("}\n")
                datetuple = ast.literal_eval(datestring)
                return datetuple