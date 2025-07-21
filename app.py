import tkinter
from tkinter import ttk
import rmidi
from pynput import keyboard
import pynput
from pynput.keyboard import Key, Controller
import threading
from time import sleep
import mido

if __name__ == '__main__':
    root = tkinter.Tk()
    Rmidi = rmidi.rmidi()

    root.title = 'Midi to Keystrokes for Linux'
    root.overrideredirect(True)

    queuedSongList = []
    queuedSong = ''

    finishedLoading = False

    toggleplay = 0

    def inputPlayback():
        global queuedSong
        global queuedSongList
        global toggleplay
        ckeyboard = Controller()
        currentsong = ''
        def on_press(key):
            global toggleplay
            if key == Key.f8:
                if toggleplay == 1:
                    toggleplay = 0
                elif toggleplay == 0:
                    toggleplay = 1
        listner = keyboard.Listener(on_press=on_press)
        listner.start()
        while True:
            if queuedSong != '':
                if currentsong == queuedSong:
                    currentsong = queuedSong
                    if toggleplay == 1:
                        while toggleplay == 1:
                            if currentsong != queuedSong: # Checks if user hasnt changed selection
                                toggleplay = 0
                                currentsong = queuedSong
                                break
                            for msg in mido.MidiFile(f"./music/{currentsong}").play():
                                if toggleplay == 0:
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
                        toggleplay = 0
                    else:
                        pass
                elif currentsong != queuedSong: # Another check, idk if its redundant or anything, icba to check.
                    currentsong = queuedSong
                    toggleplay = 0
            elif queuedSong == '':
                pass

    t = threading.Thread(target=inputPlayback)
    t.start()

    def makeList(event):
        global Rmidi
        cleanlist = []
        lslist = Rmidi.list_midi_files()

        for entry in lslist:
            if '.mid' in entry:
                cleanlist.append(entry)
        dropdown.config(values=cleanlist)

    def queueSong():
        global Rmidi
        global queuedSongList
        global queuedSong
        queuedSong = dropdown.get()
        queuedSongList = Rmidi.midToList(queuedSong)
        currentStatus.config(text=f"Queued song: {queuedSong}\nPress F8 to play.", justify="center")



    currentStatus = ttk.Label(root, text="Not playing", justify="center")
    dropdown = ttk.Combobox(root, values=NotImplemented)
    playSong = ttk.Button(root, text="Play selected song", command=queueSong)
    
    dropdown.set("Select a file to play")
    dropdown.bind("<Button>", makeList)
    
    dropdown.grid(row=1, column=0)
    currentStatus.grid(row=0, column=0)
    playSong.grid(row=2, column=0)

    
    root.mainloop()


