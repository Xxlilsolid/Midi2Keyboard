import os
import mido
from mido import MidiFile
import settings
from pynput import keyboard
from pynput.keyboard import Key, Controller 
import requests
import yt_dlp
from time import sleep
import shutil
import filechecker
import loggy

if __name__ == "__main__":
    print("This is a module silly")
else:        
    class rmidi:
        downloadprogress = ""
        Log = loggy.Log(settings.LOGFILE, True)
        def __init__(self):
            self.dir = os.path.abspath("./music")
            self.specchar = {'!','@','$','%','^','*','('}
            self.speccharkeymap = {'!': '1',
                                    '@': '2',
                                    '$': '4',
                                    '%': '5',
                                    '^': '6',
                                    '*': '8',
                                    '(': '9'}
            self.keymap = {36 : '1',
                            37 : '!',
                            38 : '2',
                            39 : '@',
                            40 : '3',
                            41 : '4',
                            42 : '$',
                            43 : '5',
                            44 : '%',
                            45 : '6',
                            46 : '^',
                            47: '7',
                            48: '8',
                            49: '*',
                            50: '9',
                            51: '(',
                            52: '0',
                            53: 'q',
                            54: 'Q',
                            55: 'w',
                            56: 'W',
                            57: 'e',
                            58: 'E',
                            59: 'r',
                            60: 't',
                            61: 'T',
                            62: 'y',
                            63: 'Y',
                            64: 'u',
                            65: 'i',
                            66: 'I',
                            67: 'o',
                            68: 'O',
                            69: 'p',
                            70: 'P',
                            71: 'a',
                            72: 's',
                            73: 'S',
                            74: 'd',
                            75: 'D',
                            76: 'f',
                            77: 'g',
                            78: 'G',
                            79: 'h',
                            80: 'H',
                            81: 'j',
                            82: 'J',
                            83: 'k',
                            84: 'l',
                            85: 'L',
                            86: 'z',
                            87: 'Z',
                            88: 'x',
                            89: 'c',
                            90: 'C',
                            91: 'v',
                            92: 'V',
                            93: 'b',
                            94: 'B',
                            95: 'n',
                            96: 'm'}       

        def list_midi_files(self):
            return os.listdir(self.dir)
        def inputPlayback(self):
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
                                        if self.keymap[note].isupper():
                                            with ckeyboard.pressed(Key.shift):
                                                ckeyboard.press(self.keymap[note]) # For uppercase
                                                ckeyboard.release(self.keymap[note])
                                        elif self.keymap[note] in self.specchar:
                                            with ckeyboard.pressed(Key.shift):
                                                ckeyboard.press(self.speccharkeymap[self.keymap[note]]) # For special characters i.e %,! etc
                                                ckeyboard.release(self.speccharkeymap[self.keymap[note]])
                                        else:
                                            ckeyboard.press(self.keymap[note]) # For lowercase
                                            ckeyboard.release(self.keymap[note])
                                break
                            settings.toggleplay = 0
                        else:
                            pass
                    elif settings.currentsong != settings.queuedSong: # Another check, idk if its redundant or anything, icba to check.
                        settings.currentsong = settings.queuedSong
                        settings.toggleplay = 0
                elif settings.queuedSong == '':
                    pass

        
        def downloadmid(self, url, tmplocation, cookie, refreshtoken):
            self.downloadprogress = "Preparing download...\n"
            ydl_opts = {
                'format': 'mp3/bestaudio/best',
                'outtmpl': f"{os.path.abspath(tmplocation)}/%(title)s.%(ext)s",  # Save to the specified location with the title as filename
                # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
                'postprocessors': [{  # Extract audio using ffmpeg
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                }]
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                for file in os.listdir(tmplocation): os.remove(os.path.join(tmplocation, file))
                self.downloadprogress = "Downloading song...\n"
                try:
                    error_code = ydl.download(url)
                except Exception as e:
                    self.downloadprogress = f"[ERROR: {type(e).__name__}] An error has occured and the process can not continue."
                    self.Log.writelog(f"[ERROR: {type(e).__name__}] An error has occured and the process can not continue.", True)
                    self.Log.writelog(f"{e}", True)
                    return 1
                self.downloadprogress = "Song downloaded\n"

            cookiesdict = {"accessToken": cookie}
            refreshdict = {"refreshToken": refreshtoken}

            URL = "https://api.ai-midi.com/api/v1/transcribe?bpm=120&beat=4&bar=4&input_method=upload"
            self.downloadprogress = "Uploading song to ai-midi.com...\n"
            try:
                x = requests.post(URL, files={'input_audio': open(f'{tmplocation}/{os.listdir(tmplocation)[0]}', 'rb')}, cookies=cookiesdict)
            except Exception as e:
                self.downloadprogress = f"[ERROR: {type(e).__name__}] An error has occured and the proccess can not continue."
                self.Log.writelog(f"[ERROR: {type(e).__name__}] An error has occured and the process can not continue.", True)
                self.Log.writelog(f"{e}", True)
                return 1
            try:
                request_id = x.json()['request_id']
            except Exception as e:
                if x.json()["detail"] == "Token expired":
                    self.downloadprogress = "Token expired, refreshing...\n"
                    print("Token expired, refreshing...")
                    try:
                        refreshrequest = requests.post("https://api.ai-midi.com/api/v1/auth/refresh", cookies=refreshdict)
                    except Exception as e:
                        self.downloadprogress = f"[ERROR]\nAn undocumented error has occured. Make sure that your refresh token is correct and try again. If it is still failing, upload latest.log and make a bug report."
                        self.Log.writelog(f"[ERROR: {type(e).__name__}] An undocumented error has occured. Make sure that your refresh token is correct and try again. If it is still failing, upload latest.log and make a bug report.", True)
                        self.Log.writelog(f"{e}", True)
                        return 1
                    filechecker.FileChecker().write_settings("settings.json", ["cookie", refreshrequest.json()["access_token"]])
                    print("Refreshed token and writen new token to settings.json")
                    self.downloadprogress = "Refreshed token, retrying upload...\n"
                    x = requests.post(URL, files={'input_audio': open(f'{tmplocation}/{os.listdir(tmplocation)[0]}', 'rb')}, cookies={"accessToken": refreshrequest.json()["access_token"]})
                    request_id = x.json()['request_id']
                
                elif x.json()["detail"] == "Unauthorized":
                    self.downloadprogress = f"[ERROR: {type(e).__name__}] No cookie was found. Please enter your cookie."
                    self.Log.writelog(f"[ERROR: {type(e).__name__}] No cookie was found. Please enter your cookie.", True)
                    self.Log.writelog(f"{e}", True)
                    return 1
                
                elif x.json()["detail"] == "Invalid token format":
                    self.downloadprogress = f"[ERROR: {type(e).__name__}] Your cookie format is incorrect, please enter your cookie again."
                    self.Log.writelog(f"[ERROR: {type(e).__name__}] Your cookie format is incorrect, Please enter your cookie again.", True)
                    self.Log.writelog(f"{e}", True)
                    return 1
                
                elif x.json()["detail"] == "Internal Server Error":
                    os.remove(f"{tmplocation}/*")
                    self.downloadprogress = f"[ERROR: {type(e).__name__}] The programme tried sending multiple files to ai-midi.com in one request. Please restart the conversion again."
                    self.Log.writelog(f"[ERROR: {type(e).__name__}] The programme tried sending multiple files to ai-midi.com in one request. Please restart the conversion again.", True)
                    self.Log.writelog(f"{e}", True)
                    return 1
                
                else:
                    self.downloadprogress = f"[ERROR: {e}]\nAn undocumented error has occured. Please open a bug report and wait for the developer to fix it."
                    self.Log.writelog(f"[ERROR: {type(e).__name__}] An undocumented error has occured. Please open a bug report and wait for the developer to fix it.", True)
                    self.Log.writelog(f"{e}", True)
                    return 1
            
            while True:
                self.downloadprogress = "Waiting for transcription to complete...\n"
                y = requests.get(f'https://api.ai-midi.com/api/v1/transcribe/status/{request_id}')
                if y.json()['status'] == "completed":
                    self.downloadprogress = "Transcription completed, downloading MIDI file...\n"
                    print("Transcription completed, downloading MIDI file...")
                    download_url = f"https://api.ai-midi.com/api/v1/transcribe/download/{request_id}"
                    z = requests.get(download_url)
                    with open(f"{tmplocation}/{os.listdir(tmplocation)[0][:-4]}.mid", 'wb') as f:
                        f.write(z.content)
                        shutil.move(f"{tmplocation}/{os.listdir(tmplocation)[0][:-4]}.mid", f"{os.path.abspath("./music")}/{os.listdir(tmplocation)[0][:-4]}.mid")
                        self.downloadprogress = "MIDI file downloaded successfully!\n"
                        print("MIDI file downloaded successfully!")
                        break
                sleep(5)