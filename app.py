import tkinter
from tkinter import ttk
import rmidi
import threading
from time import sleep
import settings
import filechecker
import os
import subprocess

if __name__ == '__main__':
    root = tkinter.Tk()
    root.title('Midi to Keystrokes for Linux')

    Rmidi = rmidi.rmidi()

    SETTINGS_FILE = "settings.json"
    settings.DESKTOP_SESSION = subprocess.check_output("echo $DESKTOP_SESSION", shell=True, text=True).strip()

    if settings.DESKTOP_SESSION in {"hyprland", "sway", "i3"}:
        print("Tiling window manager mode is active.")
        root.overrideredirect(True)

    filechecker.FileChecker().check_dir('./music', True)
    if filechecker.FileChecker().read_settings(SETTINGS_FILE) == False: filechecker.FileChecker().generate_settings(SETTINGS_FILE, {"placeholder": 0})

    

    t = threading.Thread(target=Rmidi.inputPlayback)
    t.start()

    class guiMethods:

        def checksettingsqueue(self):
            global settings
            settingsdict = filechecker.FileChecker().read_settings(SETTINGS_FILE)
            print(os.path.exists(f"./music/{settingsdict['lastsong']}"))
            try:
                if os.path.exists(f"./music/{settingsdict['lastsong']}") == True and os.path.exists(f"./music/{settingsdict['lastsong']}") != '' and settings.queuedSong != '':
                    settings.queuedSong = settingsdict["lastsong"]
                    return f"Queued song: {settings.queuedSong}\nPress F8 to play."
                else:
                    filechecker.FileChecker().write_settings(SETTINGS_FILE, ["lastsong", ""])
                    return f"Not playing. Select a song to play"
            except KeyError:
                return "Not Playing"

        def makeList(self, event):
            cleanlist = []
            lslist = Rmidi.list_midi_files()

            for entry in lslist:
                if '.mid' in entry:
                    cleanlist.append(entry)
            dropdown.config(values=cleanlist)

        def queueSong(self):
            global settings
            settings.queuedSong = dropdown.get()
            filechecker.FileChecker().write_settings(SETTINGS_FILE, ["lastsong", settings.queuedSong])
            currentStatus.config(text=f"Queued song: {settings.queuedSong}\nPress F8 to play.", justify="center")

        def downloadsongwindow(self):
            global settings
            newWindow = tkinter.Toplevel(root)
            newWindow.title("Download song")
            if settings.DESKTOP_SESSION in {"hyprland", "sway", "i3"}:
                newWindow.overrideredirect(True)
                
                frame = ttk.Frame(newWindow)
                frame.pack(side=tkinter.TOP,padx=0, pady=0)

                label = ttk.Label(frame, text="Add your cookie here", justify="center")
                cookieEntry = ttk.Entry(frame, width=25)
                if filechecker.FileChecker().read_settings(SETTINGS_FILE)["cookie"] != '':
                    label.config(text="Cookie already set, you can change it here")
                songlabel = ttk.Label(frame, text="Enter song URL from youtube (Piano covers are best)", justify="center")
                songEntry = ttk.Entry(frame, width=25)
                
                label.grid(row=0, column=0)
                cookieEntry.grid(row=1, column=0)
                songlabel.grid(row=2, column=0)
                songEntry.grid(row=3, column=0)

                commandbuttonframe = ttk.Frame(newWindow)
                commandbuttonframe.pack(side=tkinter.BOTTOM, padx=0, pady=0)
                
                instruction = ttk.Button(commandbuttonframe, text="How to get cookie?", command=lambda: self.instructionwindow())
                downloadSong = ttk.Button(commandbuttonframe, text="Download song")

                instruction.pack(side=tkinter.LEFT, padx=0, pady=0)
                downloadSong.pack(side=tkinter.LEFT, padx=0, pady=0)

        def instructionwindow(self):
            global settings
            newWindow = tkinter.Toplevel(root)
            newWindow.title("Download song")
            if settings.DESKTOP_SESSION in {"hyprland", "sway", "i3"}:
                newWindow.overrideredirect(True)

            frame = ttk.Frame(newWindow)
            frame.pack(side=tkinter.TOP)
            Disclaimer = ttk.Label(frame, text="DISCLAIMER: This will require usage of your session cookie on ai-midi.com.\nThis cookie should be different from your ACTUAL google account cookie (as noted in the README.md).\nThe developer has no access to the cookie you input into the programme.\nYou can check where the cookie is used and sent to (which is only sent to authenticate a request to upload your mp3 file to convert it to a mid file) as the programme is open source.\nIf you are not comfortable with this, do not use this feature. Thanks!", justify="center", foreground="red")
            Disclaimer.grid(row=0, column=0)

    currentStatus = ttk.Label(root, text=guiMethods().checksettingsqueue(), justify="center")
    dropdown = ttk.Combobox(root, values=NotImplemented)
    playSong = ttk.Button(root, text="Play selected song", command=lambda: guiMethods().queueSong())
    downloadSong = ttk.Button(root, text="Download song", command=lambda: guiMethods().downloadsongwindow())
    
    if not settings.queuedSong: dropdown.set("Select a file to play")
    else: dropdown.set(settings.queuedSong)
    dropdown.bind("<Button>", lambda event: guiMethods().makeList(event))
    
    dropdown.grid(row=1, column=0)
    currentStatus.grid(row=0, column=0)
    playSong.grid(row=2, column=0)
    downloadSong.grid(row=3, column=0)

    
    root.mainloop()