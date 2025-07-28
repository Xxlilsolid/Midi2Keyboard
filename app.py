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
            try:
                settings.queuedSong = settingsdict["lastsong"]
                return f"Queued song: {settings.queuedSong}\nPress F8 to play."
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


    currentStatus = ttk.Label(root, text=guiMethods().checksettingsqueue(), justify="center")
    dropdown = ttk.Combobox(root, values=NotImplemented)
    playSong = ttk.Button(root, text="Play selected song", command=lambda: guiMethods().queueSong())
    
    if not settings.queuedSong: dropdown.set("Select a file to play")
    else: dropdown.set(settings.queuedSong)
    dropdown.bind("<Button>", lambda event: guiMethods().makeList(event))
    
    dropdown.grid(row=1, column=0)
    currentStatus.grid(row=0, column=0)
    playSong.grid(row=2, column=0)

    
    root.mainloop()