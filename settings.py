import subprocess

queuedSongList = []
queuedSong = ''
finishedLoading = False
toggleplay = 0
desktop_session = ''
LOGFILE = './logs/latest.log'
try: 
    APP_VER = str(subprocess.check_output(["git", "rev-parse", "--short", 'HEAD']).strip())[2:-1]
except Exception as e:
    APP_VER = "Frozen"