# A MIRP Alternative for Linux!

## Why this when there is others like this?:

Yes I know that there is other projects like this that performs a similar task, but I wanted to create my own because:

A) Why not  
B) To gain experience with Git and Python

## System Requirements

- X11 (XWayland will do just fine though, make sure Sober and the program is under XWayland)
- Linux (You can use Mac and Windows for this though, but it is mainly targetted for Linux users)
- The computer boots

## Installation

Quickest:  
> Download the latest release from the main branch (not currently available yet)
```
chmod u+x app  
./app
```

Build from source:
> Slowest but the safest  
```
git clone https://github.com/Xxlilsolid/Midi2KeyboardLinux.git
cd Midi2KeyboardLinux
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
main.py (when venv is active, if not do .venv/bin/python main.py)
```

## Instructions

Create the folder "music" relative to where the executable is.  
Put your glorious .mid files in there.  
Profit.

## Future plans

Once I get the project to where I am satisfied, I will probably stop maintaining the project. Anyways, here is my todo on the project thus far (in no particular order btw)!

- [x] Get project working!
- [ ] Automagically create a music directory
- [ ] More transpostion options? (Idk if ive implemented it correctly)
- [ ] GUI Overhaul
- [ ] Build pre-built binaries. 
- [ ] Comment and/or make docstrings in methods
- [ ] Auto updater for releases (and git)

List subject to change
