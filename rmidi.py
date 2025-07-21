import os
import mido
from mido import MidiFile

if __name__ == "__main__":
    print("This is a module silly")
else:

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


