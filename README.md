# A MIRP Alternative for Linux!

> [!CAUTION]
> The feature "Download song" utilises ai-midi.com to convert a downloaded youtube song into a .mid to use with the programme.  
>
>The feature requires inserting your ai-midi.com cookie to work properly. The cookie shouldnt correspond to your actual google account cookie (emphasis on the shouldn't, did slight testing to confrim that the cookie value didnt pop up on two sites). With that being said, the cookie is only used to authenticate conversions between .mp3 to .mid. Nothing more. Don't feel like you need to use the feature. You dont. If you have python knowledge but dont trust the programme, check the source code yourself. Nothing besides horribly edited code will be in there :).  

## Why this when there is others like this?:

Yes I know that there is other projects like this that performs a similar task, but I wanted to create my own because:

A) Why not  
B) To gain experience with Git and Python

## System Requirements

- X11 (XWayland will do just fine though, make sure Sober and the program is under XWayland)
- Linux (You can use Mac and Windows for this though, but it is mainly targetted for Linux users)
- The computer boots

## Dependencies

Ubuntu/Debian:  
```sudo apt install python3-dev libevdev-dev libudev-dev build-essential python3-tk```  

Fedora:  
```sudo dnf install python3-devel python3-tkinter systemd-devel libevdev-devel gcc```  

Arch Linux:  
```sudo pacman -S python tk libevdev systemd base-devel```



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

Run the python script or executable  
Put your glorious .mid files in the newly created "music" file.  
Follow the steps on the GUI.

## Future plans

Once I get the project to where I am satisfied, I will probably stop maintaining the project. Anyways, here is my todo on the project thus far (in no particular order btw)!

- [x] Get project working!
- [x] Automagically create a music directory
- [x] Persistent settings capabilities
- [ ] More transpostion options? (Idk if ive implemented it correctly)
- [ ] GUI Overhaul
- [ ] Build pre-built binaries. 
- [ ] Comment and/or make docstrings in methods
- [ ] Auto updater for releases (and git)
- [ ] Abide by the naming conventions
- [ ] Ability to pause and unpause songs w/o stopping the whole song
- [ ] Kind of far fetched, but able to download .mid files to use with the programme
- [ ] PKGBUILD would be cool ig
- [ ] Project logo for README and icon in bar
- [ ] Exception handling (because its basically non existent lol)

List subject to change
