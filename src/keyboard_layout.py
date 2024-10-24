from classes import KeyAliases, KeyEventData

# for user_key_representation (first argument of KeyAliases):
#   use 'plus' istead of '+'
#   use 'comma' istead of ','
#   use 'space' istead of ' '

# Right-click on the program icon in the system tray -> "Show Pressed Keys Data" -> Press the same key multiple times, while holding different modifiers, such as "shift", "control", and "alt gr", and also without modifiers -> Copy the generated entries of KeyEventData that are different from each other and that correspond to the same physical key on the keyboard -> Paste these entries inside of a `KeyAliases(..., [...])`
# A KeyAliases object represents a physical key on the keyboard. The first argument (called "user_key_representation") is the name you gave to this key on your keyboard (note that you must use this name in your chords inside `src\dictionaries.py`). The second argument is a list of KeyEventData. Each of these KeyEventData is a set of event data that the program can receive when that physical key is pressed with or without modifiers ("shift", "control", "alt gr", "num lock", etc.).
# For example, the physical key "1" - outside the numeric keypad - can send three different types of events, depending on which modifier keys are pressed or not. If there is no modifier key pressed, the event sent is `KeyEventData(scan_code=2, name='1', is_keypad=False)`. If the "shift" key is pressed, the event sent is `KeyEventData(scan_code=2, name='!', is_keypad=False)`. If the "alt gr" key is pressed, the event sent is `KeyEventData(scan_code=2, name='¹', is_keypad=False)`. Based on this, we register this physical key as `KeyAliases('1', [ KeyEventData(scan_code=2, name='1', is_keypad=False), KeyEventData(scan_code=2, name='!', is_keypad=False), KeyEventData(scan_code=2, name='¹', is_keypad=False), ])`.
# These registers allow the program to understand how the events it receives are related to physical keys, because, as already said, different events can correspond to exactly the same physical key.

KEY_ALIASES: list[KeyAliases] = [
    KeyAliases("'", [
        KeyEventData(scan_code=41, name="'", is_keypad=False), 
        KeyEventData(scan_code=41, name='"', is_keypad=False),
    ]),
    KeyAliases('1', [
        KeyEventData(scan_code=2, name='1', is_keypad=False), 
        KeyEventData(scan_code=2, name='!', is_keypad=False), 
        KeyEventData(scan_code=2, name='¹', is_keypad=False),
    ]),
    KeyAliases('2', [
        KeyEventData(scan_code=3, name='2', is_keypad=False),
        KeyEventData(scan_code=3, name='@', is_keypad=False),
        KeyEventData(scan_code=3, name='²', is_keypad=False),
    ]),
    KeyAliases('3', [
        KeyEventData(scan_code=4, name='3', is_keypad=False),
        KeyEventData(scan_code=4, name='#', is_keypad=False),
        KeyEventData(scan_code=4, name='³', is_keypad=False),
    ]),
    KeyAliases('4', [
        KeyEventData(scan_code=5, name='4', is_keypad=False),
        KeyEventData(scan_code=5, name='$', is_keypad=False),
        KeyEventData(scan_code=5, name='£', is_keypad=False),
    ]),
    KeyAliases('5', [
        KeyEventData(scan_code=6, name='5', is_keypad=False),
        KeyEventData(scan_code=6, name='%', is_keypad=False),
        KeyEventData(scan_code=6, name='¢', is_keypad=False),
    ]),
    KeyAliases('6', [
        KeyEventData(scan_code=7, name='6', is_keypad=False),
        KeyEventData(scan_code=7, name='¨', is_keypad=False),
        KeyEventData(scan_code=7, name='¬', is_keypad=False),
    ]),
    KeyAliases('7', [
        KeyEventData(scan_code=8, name='7', is_keypad=False),
        KeyEventData(scan_code=8, name='&', is_keypad=False),
    ]),
    KeyAliases('8', [
        KeyEventData(scan_code=9, name='8', is_keypad=False),
        KeyEventData(scan_code=9, name='*', is_keypad=False),
    ]),
    KeyAliases('9', [
        KeyEventData(scan_code=10, name='9', is_keypad=False),
        KeyEventData(scan_code=10, name='(', is_keypad=False),
    ]),
    KeyAliases('0', [
        KeyEventData(scan_code=11, name='0', is_keypad=False),
        KeyEventData(scan_code=11, name=')', is_keypad=False),
    ]),
    KeyAliases('-', [
        KeyEventData(scan_code=12, name='-', is_keypad=False),
        KeyEventData(scan_code=12, name='_', is_keypad=False),
    ]),
    KeyAliases('=', [
        KeyEventData(scan_code=13, name='=', is_keypad=False),
        KeyEventData(scan_code=13, name='+', is_keypad=False),
        KeyEventData(scan_code=13, name='§', is_keypad=False),
    ]),
    KeyAliases('pause', [
        KeyEventData(scan_code=69, name='pause', is_keypad=False),
        KeyEventData(scan_code=70, name='♥', is_keypad=False),
    ]),
    KeyAliases('scroll lock', [
        KeyEventData(scan_code=70, name='scroll lock', is_keypad=False),
        # KeyEventData(scan_code=70, name='♥', is_keypad=False), # ! repeats with 'pause' above
    ]),
    KeyAliases('print screen', [
        KeyEventData(scan_code=55, name='print screen', is_keypad=False),
        KeyEventData(scan_code=84, name='sys req', is_keypad=False),
    ]),
    KeyAliases('num lock', [
        KeyEventData(scan_code=69, name='num lock', is_keypad=True),
        KeyEventData(scan_code=69, name='num lock', is_keypad=False),
    ]),
    KeyAliases('num /', [
        KeyEventData(scan_code=53, name='/', is_keypad=True),
    ]),
    KeyAliases('num *', [
        KeyEventData(scan_code=55, name='*', is_keypad=True),
    ]),
    KeyAliases('num -', [
        KeyEventData(scan_code=74, name='-', is_keypad=True),
    ]),
    KeyAliases('q', [
        KeyEventData(scan_code=16, name='q', is_keypad=False),
        KeyEventData(scan_code=16, name='/', is_keypad=False),
    ]),
    KeyAliases('w', [
        KeyEventData(scan_code=17, name='w', is_keypad=False),
        KeyEventData(scan_code=17, name='?', is_keypad=False),
    ]),
    KeyAliases('e', [
        KeyEventData(scan_code=18, name='e', is_keypad=False),
        KeyEventData(scan_code=18, name='°', is_keypad=False),
    ]),
    KeyAliases('´', [
        KeyEventData(scan_code=26, name='´', is_keypad=False),
        KeyEventData(scan_code=26, name='`', is_keypad=False),
    ]),
    KeyAliases('[', [
        KeyEventData(scan_code=27, name='[', is_keypad=False),
        KeyEventData(scan_code=27, name='{', is_keypad=False),
        KeyEventData(scan_code=27, name='ª', is_keypad=False),
    ]),
    KeyAliases('num 7', [
        KeyEventData(scan_code=71, name='7', is_keypad=True),
        KeyEventData(scan_code=71, name='home', is_keypad=True),
    ]),
    KeyAliases('num 8', [
        KeyEventData(scan_code=72, name='8', is_keypad=True),
        KeyEventData(scan_code=72, name='up', is_keypad=True),
    ]),
    KeyAliases('num 9', [
        KeyEventData(scan_code=73, name='9', is_keypad=True),
        KeyEventData(scan_code=73, name='page up', is_keypad=True),
    ]),
    KeyAliases('num plus', [
        KeyEventData(scan_code=78, name='+', is_keypad=True),
    ]),
    KeyAliases('~', [
        KeyEventData(scan_code=40, name='~', is_keypad=False),
        KeyEventData(scan_code=40, name='^', is_keypad=False),
    ]),
    KeyAliases(']', [
        KeyEventData(scan_code=43, name=']', is_keypad=False),
        KeyEventData(scan_code=43, name='}', is_keypad=False),
        KeyEventData(scan_code=43, name='º', is_keypad=False),
    ]),
    KeyAliases('num 4', [
        KeyEventData(scan_code=75, name='4', is_keypad=True),
        KeyEventData(scan_code=75, name='left', is_keypad=True),
    ]),
    KeyAliases('num 5', [
        KeyEventData(scan_code=76, name='5', is_keypad=True),
        KeyEventData(scan_code=76, name='clear', is_keypad=True),
    ]),
    KeyAliases('num 6', [
        KeyEventData(scan_code=77, name='6', is_keypad=True),
        KeyEventData(scan_code=77, name='right', is_keypad=True),
    ]),
    KeyAliases('num .', [
        KeyEventData(scan_code=126, name='.', is_keypad=True),
        KeyEventData(scan_code=126, name='f15', is_keypad=True),
    ]),
    KeyAliases('\\', [
        KeyEventData(scan_code=86, name='\\', is_keypad=False),
        KeyEventData(scan_code=86, name='|', is_keypad=False),
    ]),
    KeyAliases('c', [
        KeyEventData(scan_code=46, name='c', is_keypad=False),
        KeyEventData(scan_code=46, name='₢', is_keypad=False),
    ]),
    KeyAliases('comma', [
        KeyEventData(scan_code=51, name=',', is_keypad=False),
        KeyEventData(scan_code=51, name='<', is_keypad=False),
    ]),
    KeyAliases('.', [
        KeyEventData(scan_code=52, name='.', is_keypad=False),
        KeyEventData(scan_code=52, name='>', is_keypad=False),
    ]),
    KeyAliases(';', [
        KeyEventData(scan_code=53, name=';', is_keypad=False),
        KeyEventData(scan_code=53, name=':', is_keypad=False),
    ]),
    KeyAliases('/', [
        KeyEventData(scan_code=115, name='/', is_keypad=False),
        KeyEventData(scan_code=115, name='?', is_keypad=False),
        KeyEventData(scan_code=115, name='°', is_keypad=False),
    ]),
    KeyAliases('num 1', [
        KeyEventData(scan_code=79, name='1', is_keypad=True),
        KeyEventData(scan_code=79, name='end', is_keypad=True),
    ]),
    KeyAliases('num 2', [
        KeyEventData(scan_code=80, name='2', is_keypad=True),
        KeyEventData(scan_code=80, name='down', is_keypad=True),
    ]),
    KeyAliases('num 3', [
        KeyEventData(scan_code=81, name='3', is_keypad=True),
        KeyEventData(scan_code=81, name='page down', is_keypad=True),
    ]),
    KeyAliases('num enter', [
        KeyEventData(scan_code=28, name='enter', is_keypad=True),
    ]),
    KeyAliases('num 0', [
        KeyEventData(scan_code=82, name='0', is_keypad=True),
        KeyEventData(scan_code=82, name='insert', is_keypad=True),
    ]),
    KeyAliases('num delete', [
        KeyEventData(scan_code=83, name='decimal', is_keypad=True),
        KeyEventData(scan_code=83, name='delete', is_keypad=True),
    ]),
]