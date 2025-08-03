import subprocess

queuedSongList = []
queuedSong = ''
finishedLoading = False
toggleplay = 0
DESKTOP_SESSION = ''
LOGFILE = './logs/latest.log'
APP_VER = str(subprocess.check_output(["git", "rev-parse", "--short", 'HEAD']).strip())[2:-1]