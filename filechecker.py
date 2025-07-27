import os
import json


if __name__ == 'main':
    print("This is a module silly")
else:
    class FileChecker:
        def check_dir(self, folder, mkdir):
            dir = os.path.abspath(folder)
            if not os.path.exists(dir):
                if mkdir:
                    os.makedirs(dir)
                else:
                    return [False, "Directory does not exist"]
                return ["True", "Directory created"]
            return ["True", "Directory exists"]
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
            

