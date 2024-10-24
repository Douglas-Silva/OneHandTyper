from typing import Callable, List, Tuple
from abc import ABC, abstractmethod

import keyboard

from util import find, format_function

class KeyEventData():

    def __init__(self, *, scan_code: int, name: str | None, is_keypad: bool | None):
        if not isinstance(scan_code, int):
            raise ValueError(f'The "scan_code" of {self.__class__.__name__} should be an int, but received {str(scan_code)} that is of type {type(scan_code)}!')
        if name != None and not isinstance(name, str):
            raise ValueError(f'The "name" of {self.__class__.__name__} should be a string or None, but received {str(name)} that is of type {type(name)}!')
        if is_keypad != None and not isinstance(is_keypad, bool):
            raise ValueError(f'The "is_keypad" property of {self.__class__.__name__} should be a bool or None, but received {str(is_keypad)} that is of type {type(is_keypad)}!')
        self.scan_code = scan_code
        self.name = name
        self.is_keypad = is_keypad

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, KeyEventData): return False
        return (self.scan_code, self.name, self.is_keypad) == (other.scan_code, other.name, other.is_keypad)
    
    @staticmethod
    def fromKeyboardEvent(ev: keyboard.KeyboardEvent):
        return KeyEventData(scan_code=ev.scan_code, name=ev.name, is_keypad=ev.is_keypad)

class KeyAliases():

    def __init__(self, user_key_representation: str, aliases: list[KeyEventData]):
        if not isinstance(user_key_representation, str):
            raise ValueError(f'The "user_key_representation" of {self.__class__.__name__} should be a string or None, but received {str(user_key_representation)} that is of type {type(user_key_representation)}!')
        if not is_list_of_type(KeyEventData, aliases):
            raise ValueError(f'The "aliases" of {self.__class__.__name__} should be a list of KeyEventData, but received {str(aliases)} that is of type {type(aliases)}!')
        self.user_key_representation = user_key_representation
        self.aliases = aliases

class NonSuppressedHotkey():

    def __init__(self, hotkey: str):
        if not isinstance(hotkey, str):
            raise ValueError(f'The value passed to a {self.__class__.__name__} should be a string, but received {str(hotkey)} that is of type {type(hotkey)}!')
        self.hotkey = hotkey

class ChordDictEntry(ABC):

    def __init__(self, simple_chord: str):
        if not isinstance(simple_chord, str):
            raise ValueError(f'The first value passed to a {self.__class__.__name__} should be a string, but received {str(simple_chord)} that is of type {type(simple_chord)}!')
        self.chord = simple_chord
        self.mirrored_chord: str | None = None

    @abstractmethod
    def action_to_str(self):
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    def chord_keys(self):
        return set(self.chord_keys_list())
    
    def chord_keys_list(self):
        return self.chord.split('+')

    def mirrored_chord_keys(self):
        return set(self.mirrored_chord_keys_list())
    
    def mirrored_chord_keys_list(self):
        if not self.mirrored_chord: return []
        return self.mirrored_chord.split('+')

def is_list_of_type(item_type, maybe_list) -> bool:
    return isinstance(maybe_list, list) and all(isinstance(item, item_type) for item in maybe_list)

class ChordDict:

    def __init__(self, *, name: str, mirrorChords: bool, entries: list[ChordDictEntry]):
        if not isinstance(name, str):
            raise ValueError(f'The "name" of a {self.__class__.__name__} should be a string, but received {str(name)} that is of type {type(name)}!')
        if not isinstance(mirrorChords, bool):
            raise ValueError(f'The "mirrorChords" property of a {self.__class__.__name__} should be a bool, but received {str(mirrorChords)} that is of type {type(mirrorChords)}!')
        if not is_list_of_type(ChordDictEntry, entries):
            raise ValueError(f'The "entries" property of a {self.__class__.__name__} should be a list of objects ChordDictEntry, but received {str(entries)} that is of type {type(entries)}!')
        self.name = name
        self.entries = entries
        self.mirrorChords = mirrorChords
        self.all_watched_keys: set[str | int] = set()
        """ set that contains key names or scan codes that could be passed as first argument to `keyboard.hook_key(key_name_or_scan_code, ...)` """

    def initialize(self, MIRROR: List[Tuple[str, str]], KEY_ALIASES: list[KeyAliases]):
        self._normalize()
        if self.mirrorChords:
            self._generate_mirrored_chords(MIRROR) 
        self._update_all_watched_keys(KEY_ALIASES)

    def _update_all_watched_keys(self, KEY_ALIASES: list[KeyAliases]):

        def get_scan_codes(key: str):
            key_aliases = find(KEY_ALIASES, lambda keyals: keyals.user_key_representation == key, None)
            if key_aliases: return {keyEventData.scan_code for keyEventData in key_aliases.aliases}
            return {key}
        
        all_keys = {key for entry in self.entries for key in (entry.chord_keys() | entry.mirrored_chord_keys())}
        self.all_watched_keys.clear()
        for key in all_keys:
            self.all_watched_keys.update(get_scan_codes(key))

    def _normalize(self):
        """ Makes all `target_key`s and `chord`s of `entries` lowercase. """
        for entry in self.entries:
            entry.chord = entry.chord.lower()
            if hasattr(entry, 'target_key'):
                if isinstance(entry.target_key, str):
                    entry.target_key = entry.target_key.lower()

    def _generate_mirrored_chords(self, mirror: List[Tuple[str, str]]):

        mirror = [(left.lower(), right.lower()) for left, right in mirror] # normalize to lower case
        
        def mirror_key(key: str):
            key = key.lower() # normalize to lower case
            for left, right in mirror:
                if key==left: return right
                if key==right: return left
            return key
            
        for entry in self.entries:
            mirrored_chord_keys_list = [
                mirror_key(key)
                for key in entry.chord_keys_list()
            ]
            entry.mirrored_chord = '+'.join(mirrored_chord_keys_list) 

    def search_for_problems(self, all_dictionaries) -> list[str]:

        problems: list[str] = []

        # search for repeated chords across entries:
        entries_with_repeated_chord_reported: set[ChordDictEntry] = set()
        for entry in self.entries:
            if entry in entries_with_repeated_chord_reported:
                continue # do not report repeated chord problem again
            entries_with_equivalent_chord = [other_entry for other_entry in self.entries if ChordDict.haveEquivalentChords(entry, other_entry)]
            if len(entries_with_equivalent_chord) > 1:
                problems.append(f'> In the Dictionary "{self.name}" there are {len(entries_with_equivalent_chord)} entries with equivalent chords:'+'\n    > '+'\n    > '.join([str(other_entry)+';' for other_entry in entries_with_equivalent_chord])) # report problem of repeated chord
                entries_with_repeated_chord_reported.update(entries_with_equivalent_chord)

        # The user should be warned if there is an ActivateChordDict entry with a target ChordDict name inexistent or not found:
        for activateChordDict in [entry for entry in self.entries if isinstance(entry, ActivateChordDict)]:
            if not activateChordDict.target_chord_dict_name in [cdict.name for cdict in all_dictionaries]:
                problems.append(f'> In the dictionary "{self.name}", there is an entry ActivateChordDict to activate the dictionary "{activateChordDict.target_chord_dict_name}". However, no dictionary with that name was found. Please check for typos, and keep in mind that the search is case-sensitive and considers trailing and leading spaces.')

        return problems
    
    @staticmethod
    def haveEquivalentChords(entry1: ChordDictEntry, entry2: ChordDictEntry) -> bool:
        c1 = {key.lower() for key in entry1.chord_keys()}
        c1m = {key.lower() for key in entry1.mirrored_chord_keys()}
        c2 = {key.lower() for key in entry2.chord_keys()}
        c2m = {key.lower() for key in entry2.mirrored_chord_keys()}
        if c1 == c2: return True
        if c1 == c2m and c2m: return True
        if c1m == c2 and c1m: return True
        if c1m == c2m and c1m and c2m: return True
        return False
        
class Tap(ChordDictEntry):
    """ Tap a key or hotkey. 
    
        Use `tap_with_num_lock_disabled=True` to ensure that the key/hotkey will be pressed and released with 'num lock' disabled (the program will disable 'num lock', tap the key/hotkey, and then re-enable 'num lock'). This is useful for tapping the arrow keys when Shift is being held; otherwise, the program may not work as expected. (see https://github.com/boppreh/keyboard/issues/496).
    """

    def __init__(self, simple_chord: str, key_to_tap: str, description: str = '', *, tap_with_num_lock_disabled=False):
        super().__init__(simple_chord)
        if not isinstance(key_to_tap, str):
            raise ValueError(f'The "target_key" (the "key_to_tap") property of a {self.__class__.__name__} should be a string, but received {str(key_to_tap)} that is of type {type(key_to_tap)}!')
        if not isinstance(description, str):
            raise ValueError(f'The "description" property of a {self.__class__.__name__} should be a string, but received {str(description)} that is of type {type(description)}!')
        if not isinstance(tap_with_num_lock_disabled, bool):
            raise ValueError(f'The "tap_with_num_lock_disabled" property of a {self.__class__.__name__} should be a bool, but received {str(tap_with_num_lock_disabled)} that is of type {type(tap_with_num_lock_disabled)}!')
        self.target_key = key_to_tap
        self.description = description
        self.tap_with_num_lock_disabled = tap_with_num_lock_disabled

    def action_to_str(self):
        return f'Tap (press and release) {self.target_key}{ ', "'+self.description+'"' if self.description else ''}'
    
    def __str__(self) -> str:
        return f'Tap("{self.chord}", "{self.target_key}"{ ', "'+self.description+'"' if self.description else ''}{ f', tap_with_num_lock_disabled={str(self.tap_with_num_lock_disabled)}' if self.tap_with_num_lock_disabled else ''})'

class Hold(ChordDictEntry):
    def __init__(self, simple_chord: str, key_to_hold: str, description: str = ''):
        super().__init__(simple_chord)
        if not isinstance(key_to_hold, str):
            raise ValueError(f'The "target_key" (the "key_to_hold") property of a {self.__class__.__name__} should be a string, but received {str(key_to_hold)} that is of type {type(key_to_hold)}!')
        if not isinstance(description, str):
            raise ValueError(f'The "description" property of a {self.__class__.__name__} should be a string, but received {str(description)} that is of type {type(description)}!')
        self.target_key = key_to_hold
        self.description = description

    def action_to_str(self):
        return f'Hold {self.target_key}{ ', "'+self.description+'"' if self.description else ''}'
    
    def __str__(self) -> str:
        return f'Hold("{self.chord}", "{self.target_key}"{ ', "'+self.description+'"' if self.description else ''})'

class Write(ChordDictEntry):
    def __init__(self, simple_chord: str, text_to_write: str, description: str = ''):
        super().__init__(simple_chord)
        if not isinstance(text_to_write, str):
            raise ValueError(f'The "text_to_write" property of a {self.__class__.__name__} object should be a string, but received {str(text_to_write)} that is of type {type(text_to_write)}!')
        if not isinstance(description, str):
            raise ValueError(f'The "description" property of a {self.__class__.__name__} object should be a string, but received {str(description)} that is of type {type(description)}!')
        self.text_to_write = text_to_write
        self.description = description

    def action_to_str(self):
        return f'Write "{self.text_to_write}"{ ', ('+self.description+')' if self.description else ''}'
    
    def __str__(self) -> str:
        return f'Write("{self.chord}", "{self.text_to_write}"{ ', "'+self.description+'"' if self.description else ''})'

class ActivateChordDict(ChordDictEntry):
    def __init__(self, simple_chord: str, chord_dict_name: str):
        super().__init__(simple_chord)
        if not isinstance(chord_dict_name, str):
            raise ValueError(f'The "chord_dict_name" property of a {self.__class__.__name__} object should be a string, but received {str(chord_dict_name)} that is of type {type(chord_dict_name)}!')
        self.target_chord_dict_name = chord_dict_name

    def action_to_str(self):
        return f'Activate (switch to) Chord Dictionary "{self.target_chord_dict_name}"'
        
    def __str__(self) -> str:
        return f'ActivateChordDict("{self.chord}", "{self.target_chord_dict_name}")'
    

class ToggleActiveChordDictWindow(ChordDictEntry):

    def action_to_str(self):
        return f'Show/Hide Active Chord Dictionary'
    
    def __str__(self) -> str:
        return f'ToggleActiveChordDictWindow("{self.chord}")'

class Quit(ChordDictEntry):

    def action_to_str(self):
        return f'Quit'
            
    def __str__(self) -> str:
        return f'Quit("{self.chord}")'

class Sleep(ChordDictEntry):

    def action_to_str(self):
        return f'Sleep'
            
    def __str__(self) -> str:
        return f'Sleep("{self.chord}")'

class Restart(ChordDictEntry):

    def action_to_str(self):
        return f'Restart'
            
    def __str__(self) -> str:
        return f'Restart("{self.chord}")'

class FunctionCall(ChordDictEntry):

    def __init__(self, simple_chord: str, function: Callable[[], None], description: str = ''):
        super().__init__(simple_chord)
        if not isinstance(function, Callable):
            raise ValueError(f'The "function" property of a {self.__class__.__name__} object should be a Function (a Callable), but received {str(function)} that is of type {type(function)}!')
        if not isinstance(description, str):
            raise ValueError(f'The "description" property of a {self.__class__.__name__} object should be a string, but received {str(description)} that is of type {type(description)}!')
        FUNCTION_CALL_CALLABLES[self] = function
        self.function_as_str = format_function(function)
        self.description = description

    def action_to_str(self):
        return f'{self.description+' ' if self.description else ''}`{self.function_as_str}`'
                
    def __str__(self) -> str:
        return f'FunctionCall("{self.chord}", ({self.function_as_str}))'
    
FUNCTION_CALL_CALLABLES: dict[FunctionCall, Callable[[], None]] = {}
