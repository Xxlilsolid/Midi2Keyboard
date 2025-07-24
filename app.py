import tkinter
from tkinter import ttk
import rmidi
import threading
from time import sleep
import settings
import filechecker

if __name__ == '__main__':
    root = tkinter.Tk()
    root.title = 'Midi to Keystrokes for Linux'
    root.overrideredirect(True)

    Rmidi = rmidi.rmidi()

    filechecker.FileChecker().check_dir('./music', True)

    

    t = threading.Thread(target=Rmidi.inputPlayback)
    t.start()

    class guiMethods:
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
            currentStatus.config(text=f"Queued song: {settings.queuedSong}\nPress F8 to play.", justify="center")



    currentStatus = ttk.Label(root, text="Not playing", justify="center")
    dropdown = ttk.Combobox(root, values=NotImplemented)
    playSong = ttk.Button(root, text="Play selected song", command=lambda: guiMethods().queueSong())
    
    dropdown.set("Select a file to play")
    dropdown.bind("<Button>", lambda event: guiMethods().makeList(event))
    
    dropdown.grid(row=1, column=0)
    currentStatus.grid(row=0, column=0)
    playSong.grid(row=2, column=0)

    
    root.mainloop()