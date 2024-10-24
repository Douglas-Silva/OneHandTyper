from itertools import groupby
import sys
import time
import keyboard
from tkinter import Tk

import subprocess

def copy_to_clipboard(text: str) -> None:
    sp = subprocess.Popen(["clip"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    sp.communicate(text.encode("utf16"))

entries = []
keys_to_ignore = {'alt', 'right alt', 'alt gr', 'shift', 'right shift', 'ctrl', 'right ctrl', 'caps lock'}

def process_non_watched_key_event(ev: keyboard.KeyboardEvent):
    global entries
    global keys_to_ignore

    if str(ev.name).lower() == 'esc': sys.exit(0)
    
    if ev.event_type == 'up': return
    if str(ev.name).lower() in keys_to_ignore: return

    if str(ev.name).lower() == 'a':

        if entries:
            user_key_representation = entries[0][1]
            if user_key_representation == "None":
                user_key_representation = f"'(scan_code={entries[0][0]}, is_keypad={entries[0][2]})'"
            text = f"\n    KeyAliases({user_key_representation}, [" + "\n        " + '\n        '.join(
                [f"KeyEventData(scan_code={entry[0]}, name={entry[1]}, is_keypad={entry[2]})," for entry in entries]
            ) + "\n    ]),"
            print(text)
            copy_to_clipboard(text)
            entries.clear()
        else:
            print('No entries to show.')

        return

    # ev is not for key 'a':

    name = f"'{ev.name}'"
    if ev.name == None: name = "None" 
    elif ev.name == '': name = "''" 
    elif ev.name == '"': name = '\'"\''
    elif ev.name == "'": name = "\"'\""
    elif ev.name == "\\": name = "'\\\\'"
    is_keypad = str(ev.is_keypad)

    entry = (ev.scan_code, name, is_keypad)
    if not entry in entries: entries.append(entry)


keyboard.hook(process_non_watched_key_event)

print('Press "esc" to quit, press "a" go generate a KeyAliases text that you can copy. Keys being ignored: ', keys_to_ignore)

keyboard.wait('esc')