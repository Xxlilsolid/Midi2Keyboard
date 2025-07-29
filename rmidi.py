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

if __name__ == "__main__":
    print("This is a module silly")
else:
    # class ExpireToken(Exception):
    #     def __init__(self, message):
    #         self.message = message
    #         super().__init__(self.message)
    # class TokenNotFound(Exception):
    #     def __init__(self, message):
    #         self.message = message
    #         super().__init__(self.message)
    # class MultipleSongsQueued(Exception):
    #     def __init__(self, message):
    #         self.message = message
    #         super().__init__(self.message)
        
    class rmidi:

        def __init__(self):
            self.dir = os.path.abspath("./music")
            self.specchar = {'!','@','$','%','^','*','('}
            self.speccharkeymap = {
                '!': '1',
                '@': '2',
                '$': '4',
                '%': '5',
                '^': '6',
                '*': '8',
                '(': '9'
            }
            self.keymap = {
    36 : '1',
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
    96: 'm'


}       

        def list_midi_files(self):
            return os.listdir(self.dir)
        def midToList(self, mid):
            self.midilist = []
            for msg in MidiFile(f'./music/{mid}'):
                if "note_on" in str(msg):
                    self.midilist.append(msg)
                elif "note_off" in str(msg):
                    #print(msg)
                    pass
            return self.midilist
        
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
                error_code = ydl.download(url)

            cookiesdict = {"accessToken": cookie}
            refreshdict = {"refreshToken": refreshtoken}

            URL = "https://api.ai-midi.com/api/v1/transcribe?bpm=120&beat=4&bar=4&input_method=upload"
            x = requests.post(URL, files={'input_audio': open(f'{tmplocation}/{os.listdir(tmplocation)[0]}', 'rb')}, cookies=cookiesdict)
            try:
                request_id = x.json()['request_id']
            except:
                if x.json()["detail"] == "Token expired":
                    print("Token expired, refreshing...")
                    refreshrequest = requests.post("https://api.ai-midi.com/api/v1/auth/refresh", cookies=refreshdict)
                    filechecker.FileChecker().write_settings("settings.json", ["cookie", refreshrequest.json()["access_token"]])
                    print("Refreshed token and writen new token to settings.json")
                    x = requests.post(URL, files={'input_audio': open(f'{tmplocation}/{os.listdir(tmplocation)[0]}', 'rb')}, cookies={"accessToken": refreshrequest.json()["access_token"]})
                    request_id = x.json()['request_id']
                elif x.json()["detail"] == "Token not found":
                    pass
                elif x.json()["detail"] == "Internal Server Error":
                    os.remove(f"{tmplocation}/*")
                    pass
            while True:
                y = requests.get(f'https://api.ai-midi.com/api/v1/transcribe/status/{request_id}')
                if y.json()['status'] == "completed":
                    download_url = f"https://api.ai-midi.com/api/v1/transcribe/download/{request_id}"
                    z = requests.get(download_url)
                    with open(f"{tmplocation}/{os.listdir(tmplocation)[0][:-4]}.mid", 'wb') as f:
                        f.write(z.content)
                        shutil.move(f"{tmplocation}/{os.listdir(tmplocation)[0][:-4]}.mid", f"{os.path.abspath("./music")}/{os.listdir(tmplocation)[0][:-4]}.mid")
                        break
                sleep(5)