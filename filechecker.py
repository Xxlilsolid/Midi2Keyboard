import os


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
            pass