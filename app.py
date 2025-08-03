import tkinter
from tkinter import ttk
import threading
from time import sleep
import settings
import os
import subprocess
from tkinter import messagebox
from tkinter import font
import loggy
import rmidi
import filechecker

if __name__ == '__main__':
    root = tkinter.Tk()
    root.title('M2K4L')


    Log = loggy.Log(settings.LOGFILE)
    Rmidi = rmidi.rmidi()
    root.resizable(False, False)

    SETTINGS_FILE = "settings.json"
    settings.DESKTOP_SESSION = subprocess.check_output("echo $DESKTOP_SESSION", shell=True, text=True).strip()

    if settings.DESKTOP_SESSION in {"hyprland", "sway", "i3"}:
        Log.writelog("[INFO] Tiling window manager mode is active.", True)
        root.wm_attributes("-type", "utility")

    Log.writelog("[INFO] " + filechecker.FileChecker().check_dir('./music', True)[1], True)
    if filechecker.FileChecker().read_settings(SETTINGS_FILE) == False: filechecker.FileChecker().generate_settings(SETTINGS_FILE, {"lastsong": "", "cookie": "", "refresh_token": "", "transposition_mode": 1})
    Log.writelog("[INFO] " + filechecker.FileChecker().check_dir("./tmp", True)[1], True)
    Log.writelog(f"[INFO] M2K4L is on version {settings.APP_VER}", True)
    

    t = threading.Thread(target=Rmidi.inputPlayback, daemon=True)
    t.start()

    class guiMethods:
        def settingsmenu(self): # Transposition mode: 0 = Legacy 1 = Modern
            newWindow = tkinter.Toplevel(root)
            frame = ttk.Frame(newWindow)
            buttonFrame = ttk.Frame(newWindow)

            newWindow.resizable(False, False)
            if settings.DESKTOP_SESSION in {"hyprland", "sway", "i3"}:
                newWindow.wm_attributes("-type", "utility")

            def checklabeloption(dropdown):
                settings = filechecker.FileChecker().read_settings("settings.json")
                transpositionDropdownConvert = {0: "Nearest octave transposition with note clamping",
                                                1: "Octave clamped Transposition"}
                if dropdown == "transpositionDropdown":
                    try:
                        return transpositionDropdownConvert[settings["transposition_mode"]]
                    except:
                        filechecker.FileChecker().write_settings("settings.json", ["transposition_mode", 0])
                        return "Nearest octave transposition with note clamping"

            transpositionLabel = ttk.Label(frame, text="Choose transposition mode")
            transpositionDropdown = ttk.Combobox(frame, values=["Nearest octave transposition with note clamping", "Octave clamped Transposition"], state="readonly", width=40)
            transpositionDropdown.set(checklabeloption("transpositionDropdown"))
            appVer = ttk.Label(newWindow, text=f"M2K4L: {settings.APP_VER}", foreground='grey', font=font.Font(size=8))
            apply = ttk.Button(buttonFrame, text="Apply", command=lambda: writetooptions())
            close = ttk.Button(buttonFrame, text="Ok", command=lambda: newWindow.destroy())

            def writetooptions():
                transpositionDropdownConvert = {"Nearest octave transposition with note clamping": 0,
                                                "Octave clamped Transposition": 1}
                if transpositionDropdown.get() == "Placeholder":
                    pass
                filechecker.FileChecker().write_settings("settings.json", ["transposition_mode", transpositionDropdownConvert[transpositionDropdown.get()]])
                Log.writelog(f"[INFO] Saved transposition mode: {transpositionDropdown.get()}")
            
            transpositionLabel.grid(row=0, column=0) # frame 
            transpositionDropdown.grid(row=1, column=0)

            apply.grid(row=0, column=0) # buttonFrame
            close.grid(row=0, column=1)
            
            frame.pack(side=tkinter.TOP) # Everything else
            buttonFrame.pack(side=tkinter.TOP)
            appVer.pack(side=tkinter.TOP)

        def checksettingsqueue(self):
            global settings
            settingsdict = filechecker.FileChecker().read_settings(SETTINGS_FILE)
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
            if any(dropdown.get() == x for x in {"", "Select a file to play"}):
                messagebox.showerror("Error", "You must select a valid .mid file to play")
                return 1
            settings.queuedSong = dropdown.get()
            filechecker.FileChecker().write_settings(SETTINGS_FILE, ["lastsong", settings.queuedSong])
            currentStatus.config(text=f"Queued song: {settings.queuedSong}\nPress F8 to play.", justify="center")

        def downloadsongwindow(self):
            global settings
            newWindow = tkinter.Toplevel(root)
            newWindow.title("Song download options")
            newWindow.resizable(False, False)
            if settings.DESKTOP_SESSION in {"hyprland", "sway", "i3"}:
                newWindow.wm_attributes("-type", "utility")
        
            frame = ttk.Frame(newWindow)
            frame.pack(side=tkinter.TOP,padx=0, pady=0)

            accessLabel = ttk.Label(frame, text="Add your access token here", justify="center")
            accessCookieEntry = ttk.Entry(frame, width=25)
            if filechecker.FileChecker().read_settings(SETTINGS_FILE)["cookie"] != '':
                accessLabel.config(text="Access token already set, you can change it here")
            refreshLabel = ttk.Label(frame, text="Add your refresh token here", justify="center")
            refreshCookieEntry = ttk.Entry(frame, width=25)
            if filechecker.FileChecker().read_settings(SETTINGS_FILE)["refresh_token"] != '':
                refreshLabel.config(text="Refresh token already set, you can change it here")
            songlabel = ttk.Label(frame, text="Enter song URL from youtube (Piano covers are best)", justify="center")
            songEntry = ttk.Entry(frame, width=25)

            def downloadsong(): # Opens GUI with progress
                if accessCookieEntry.get() != '':
                    filechecker.FileChecker().write_settings("settings.json", ["cookie", accessCookieEntry.get()])
                if refreshCookieEntry.get() != '':
                    filechecker.FileChecker().write_settings("settings.json", ["refresh_token", refreshCookieEntry.get()])
                if songEntry.get() == '':
                    messagebox.showerror("Error", "You must enter a Youtube URL to download!")
                    return
                if all(x not in songEntry.get() for x in {"youtube", "youtu.be"}):
                    messagebox.showerror("Error", "You must enter a Youtube URL to download!")
                    return
                if "radio" in songEntry.get():
                    messagebox.showerror("Error", "Midi2Keyboard doesnt support mix/playlist links yet.")
                    return
                newWindow = tkinter.Toplevel(root)
                newWindow.title("Downloading song")
                newWindow.resizable(False, False)
                if settings.DESKTOP_SESSION in {"hyprland", "sway", "i3"}:
                    newWindow.wm_attributes("-type", "utility")

                progress = ttk.Label(newWindow, text="Starting operation\n", foreground='red')
                button = ttk.Button(newWindow, text="Finished", state="disabled", command=lambda: newWindow.destroy())
                
                def callback():
                    while True:
                        sleep(1)
                        progress.config(text=Rmidi.downloadprogress)
                        if Rmidi.downloadprogress == "MIDI file downloaded successfully!\n":
                            progress.config(foreground="green")
                            button.config(state="normal")
                            break
                        if "ERROR" in Rmidi.downloadprogress:
                            progress.config(foreground="red")
                            button.config(state="normal")
                            messagebox.showerror("Error", f"An error has occured and the process has to stop.\n{Rmidi.downloadprogress}")
                            break
                    
                progress.grid(row=0)
                button.grid(row=1)
                thread = threading.Thread(target=Rmidi.downloadmid, args=(songEntry.get(), "./tmp", filechecker.FileChecker().read_settings("settings.json")["cookie"], filechecker.FileChecker().read_settings("settings.json")["refresh_token"]))
                thread.start()
                
                callbackThread = threading.Thread(target=callback)
                callbackThread.start()
                
            
            accessLabel.grid(row=0, column=0)
            accessCookieEntry.grid(row=1, column=0)
            refreshLabel.grid(row=2, column=0)
            refreshCookieEntry.grid(row=3, column=0)
            songlabel.grid(row=4, column=0)
            songEntry.grid(row=5, column=0)

            commandbuttonframe = ttk.Frame(newWindow)
            commandbuttonframe.pack(side=tkinter.BOTTOM, padx=0, pady=0)
            
            instruction = ttk.Button(commandbuttonframe, text="How to get cookie?", command=lambda: self.instructionwindow())
            downloadSong = ttk.Button(commandbuttonframe, text="Download song", command=downloadsong)

            instruction.pack(side=tkinter.LEFT, padx=0, pady=0)
            downloadSong.pack(side=tkinter.LEFT, padx=0, pady=0)

        def instructionwindow(self):
            global settings
            newWindow = tkinter.Toplevel(root)
            newWindow.title("Download song")
            if settings.DESKTOP_SESSION in {"hyprland", "sway", "i3"}:
                newWindow.wm_attributes("-type", "utility")

            frame = ttk.Frame(newWindow)
            frame.pack(side=tkinter.TOP)
            Disclaimer = ttk.Label(frame, text="DISCLAIMER: PLEASE READ THE README.md DISCLAIMER SECTION.\nIT IS INCREDIBLY IMPORTANT THAT YOU DO SO!", justify="center", foreground="red")
            hyperlink = ttk.Label(frame, text = "1. Open your browser and go to ai-midi.com (click me!)", foreground="blue")
            instructions = ttk.Label(frame, text="2. Log in with your Google account\n3. Once logged in open developer tools (or better known as inspect element)\n4. Head to the applications tab and navigate to Storage/Cookies and click on the only entry: https://ai-midi.com\n5. Copy the values of accessToken and refreshToken (you may need to refresh the site if the keys dont appear).\n6. Insert the values into the corresponding fields of the download window.\n7. Profit.", justify="center")
            closeWindow = ttk.Button(frame, text="I understand, close this window", command=newWindow.destroy)
            blank = ttk.Label(frame, text="")
            
            Disclaimer.grid(row=0, column=0)
            hyperlink.grid(row=1, column=0)
            hyperlink.bind("<Button-1>", lambda e: subprocess.run(["xdg-open", "https://ai-midi.com"]))
            instructions.grid(row=2, column=0)
            blank.grid(row=3, column=0)
            closeWindow.grid(row=4, column=0)

    currentStatus = ttk.Label(root, text=guiMethods().checksettingsqueue(), justify="center")
    dropdown = ttk.Combobox(root, values=NotImplemented, state="readonly")
    playSong = ttk.Button(root, text="Play selected song", command=lambda: guiMethods().queueSong())
    downloadSong = ttk.Button(root, text="Download song", command=lambda: guiMethods().downloadsongwindow())
    options = ttk.Button(root, text="Options", command=lambda: guiMethods().settingsmenu())
    if not settings.queuedSong: dropdown.set("Select a file to play")
    else: dropdown.set(settings.queuedSong)
    dropdown.bind("<Button>", lambda event: guiMethods().makeList(event))
    
    dropdown.grid(row=1, column=0)
    currentStatus.grid(row=0, column=0)
    playSong.grid(row=2, column=0)
    options.grid(row=3, column=0)
    downloadSong.grid(row=4, column=0)

    
    root.mainloop()