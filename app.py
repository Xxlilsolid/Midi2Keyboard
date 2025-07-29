import tkinter
from tkinter import ttk
import rmidi
import threading
from time import sleep
import settings
import filechecker
import os
import subprocess
from tkinter import messagebox


if __name__ == '__main__':
    root = tkinter.Tk()
    root.title('Midi to Keystrokes for Linux')

    Rmidi = rmidi.rmidi()

    SETTINGS_FILE = "settings.json"
    settings.DESKTOP_SESSION = subprocess.check_output("echo $DESKTOP_SESSION", shell=True, text=True).strip()

    if settings.DESKTOP_SESSION in {"hyprland", "sway", "i3"}:
        print("Tiling window manager mode is active.")
        root.wm_attributes("-type", "utility")

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

            def downloadsong():
                if songEntry.get() == '':
                    messagebox.showerror("Error", "You must enter a song URL to download!")
                    return
                Rmidi.downloadmid(songEntry.get(), "./tmp", filechecker.FileChecker().read_settings("settings.json")["cookie"], filechecker.FileChecker().read_settings("settings.json")["refresh_token"])
                
            
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