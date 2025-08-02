import os
import json
import loggy
import settings

if __name__ == 'main':
    print("This is a module silly")
else:
    class FileChecker:
        #Log = loggy.Log(settings.LOGFILE, True)
        def check_dir(self, folder, mkdir):
            dir = os.path.abspath(folder)
            if not os.path.exists(dir):
                if mkdir:
                    os.makedirs(dir)
                else:
                    #self.Log.writelog(f"[INFO] Directory \"{dir}\" does not exist.", True)
                    return (False, "Directory does not exist")
                #self.Log.writelog(f"[INFO] Directory \"{dir}\" created.", True)
                return ("True", "Directory created")
            #self.Log.writelog(f"[INFO] Directory \"{dir}\" exists.", True) 
            return ("True", "Directory exists")
        def check_file(self, file, mkfile):
            dir = os.path.abspath(file)
            if not os.path.exists(dir):
                if mkfile:
                    with open(file, "w") as file:
                        file.write('')
                else:
                    #self.Log.writelog(f"[INFO] File \"{dir}\" does not exist.", True) 
                    return (False, "File does not exist")
                #self.Log.writelog(f"[INFO] File \"{dir}\" created.", True) 
                return ("True", "File created")
            #self.Log.writelog(f"[INFO] File \"{dir}\" exist.", True) 
            return ("True", "File exists")
        def read_settings(self, settings_file):
            try:
                with open(settings_file, 'r') as file:
                    try:
                        return json.load(file)
                    except:
                        return False
            except:
                return False
        def write_settings(self, settings_file, entry: list):
            with open(settings_file, 'r+') as file:
                jsonDict = json.load(file)
                jsonDict[entry[0]] = entry[1]
                file.seek(0)
                json.dump(jsonDict, file, indent=4)
                file.truncate()
        def delete_entry(self, settings_file, key):
            jsonDict = self.read_settings(settings_file)
            with open(settings_file, 'r+') as file:
                del jsonDict[key]
                file.seek(0)
                json.dump(jsonDict, file, indent=4)
                file.truncate()
        def generate_settings(self,settingsName, settingsContent: dict):
            with open(settingsName, "w") as file:
                json.dump(settingsContent, file, indent=4)
            

