import sys
import subprocess
import settings

if __name__ == "__main__":

    if sys.argv[1] == "True":
        isStable = True
    else:
        isStable = False
    if sys.argv[2] == "True":
        isCompiled = True
    else:
        isCompiled = False


    remoteCommit = str(subprocess.check_output(["git", "rev-parse", "--short", "origin/main"]).strip())[2:-1]
    if isStable == False and isCompiled == False: # Attempt to replace all python files from remote
        if remoteCommit != settings.APP_VER:
            print("Mismatch has been detected. Prompt user to update")
        else:
            print("No update needed.")
    elif isStable == False and isCompiled == True: # Warn user that a new commit is available
        if remoteCommit != settings.APP_VER:
            print("Mismatch has been detected. Prompt user to update")
        else:
            print("No update needed.")
    elif isStable == True: # Attempts to replace all files
        print(2)
    else:
        print("An error has occured.")

else:
    print("This is to be run as a command.")