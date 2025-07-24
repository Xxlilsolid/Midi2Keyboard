import tkinter
from tkinter import ttk
import rmidi
from pynput import keyboard
import pynput
from pynput.keyboard import Key, Controller
import threading
from time import sleep
import mido
import settings

if __name__ == '__main__':
    root = tkinter.Tk()
    root.title = 'Midi to Keystrokes for Linux'
    root.overrideredirect(True)

    Rmidi = rmidi.rmidi()

    def inputPlayback():
        global settings
        ckeyboard = Controller()
        settings.currentsong = ''
        def on_press(key):
            if key == Key.f8:
                if settings.toggleplay == 1:
                    settings.toggleplay = 0
                elif settings.toggleplay == 0:
                    settings.toggleplay = 1
        listner = keyboard.Listener(on_press=on_press)
        listner.start()
        while True:
            if settings.queuedSong != '':
                if settings.currentsong == settings.queuedSong:
                    settings.currentsong = settings.queuedSong
                    if settings.toggleplay == 1:
                        while settings.toggleplay == 1:
                            if settings.currentsong != settings.queuedSong: # Checks if user hasnt changed selection
                                settings.toggleplay = 0
                                settings.currentsong = settings.queuedSong
                                break
                            for msg in mido.MidiFile(f"./music/{settings.currentsong}").play():
                                if settings.toggleplay == 0:
                                    break
                                try:
                                    note = msg.note
                                    time = msg.time
                                except:
                                    pass
                                if msg.type == 'note_on':
                                    if 96 < note <= 109:
                                        print("transposed")
                                        note = note - 12
                                    elif 36 > note >= 24:
                                        print("transposed")
                                        note = note + 12
                                    elif note > 109:
                                        print("transposed")
                                        note = 96
                                    elif note < 24:
                                        print("transposed")
                                        note = 36
                                    if Rmidi.keymap[note].isupper():
                                        with ckeyboard.pressed(Key.shift):
                                            ckeyboard.press(Rmidi.keymap[note]) # For uppercase
                                            ckeyboard.release(Rmidi.keymap[note])
                                    elif Rmidi.keymap[note] in Rmidi.specchar:
                                        with ckeyboard.pressed(Key.shift):
                                            ckeyboard.press(Rmidi.speccharkeymap[Rmidi.keymap[note]]) # For special characters i.e %,! etc
                                            ckeyboard.release(Rmidi.speccharkeymap[Rmidi.keymap[note]])
                                    else:
                                        ckeyboard.press(Rmidi.keymap[note]) # For lowercase
                                        ckeyboard.release(Rmidi.keymap[note])
                            break
                        settings.toggleplay = 0
                    else:
                        pass
                elif settings.currentsong != settings.queuedSong: # Another check, idk if its redundant or anything, icba to check.
                    settings.currentsong = settings.queuedSong
                    settings.toggleplay = 0
            elif settings.queuedSong == '':
                pass

    t = threading.Thread(target=inputPlayback)
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
            currentStatus.config(text=f"Queued song: {settings.settings.queuedSong}\nPress F8 to play.", justify="center")



    currentStatus = ttk.Label(root, text="Not playing", justify="center")
    dropdown = ttk.Combobox(root, values=NotImplemented)
    playSong = ttk.Button(root, text="Play selected song", command=lambda: guiMethods().queueSong())
    
    dropdown.set("Select a file to play")
    dropdown.bind("<Button>", lambda event: guiMethods().makeList(event))
    
    dropdown.grid(row=1, column=0)
    currentStatus.grid(row=0, column=0)
    playSong.grid(row=2, column=0)

    
    root.mainloop()