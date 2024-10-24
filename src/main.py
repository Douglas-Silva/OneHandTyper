import atexit
from multiprocessing import freeze_support
import threading
import tkinter as tk
from tkinter import messagebox
import os
import sys
import ctypes
import traceback
from typing import Any, Dict, Set, Type, TypedDict, Union
from infi.systray import SysTrayIcon # https://github.com/Infinidat/infi.systray
import keyboard # https://github.com/boppreh/keyboard?tab=readme-ov-file#keyboard.hook
from classes import *
from util import find
from GUI.gui_process import *

# Imports so that the dependencies of these files are added to the generated executable:
try:
    import keyboard_layout
    import dictionaries
except: pass

user32 = ctypes.WinDLL('user32', use_last_error = True) # see module 'keyboard' `_winkeyboard.py`

# main process state:
active_chord_dict: list[ChordDict]
systray = None
pressed_keys_repr: list[str] = []
old_pressed_keys_repr: list[str] = []
is_waiting_release_all_pressed_keys = False
GUI_PROCESS_PROXY: GUIProcessProxy | None = None
holding_keys: dict[str, bool] = {}
""" `dict[target_key_being_hold, hold_only_until_the_next_key_tap]` """
problems: list[str] = []
is_terminating = False
""" `dict[target_key_being_hold, hold_only_until_the_next_key_tap]` """
problems: list[str] = []
is_terminating = False
is_sleeping = False

def start(is_it_being_executed_by_the_executable: bool):
    global active_chord_dict
    global DICTIONARIES
    global MIRROR
    global WAKE_UP_HOTKEYS
    global GUI_PROCESS_PROXY
    global KEY_ALIASES
    global systray
    global problems
    global pressed_keys_repr
    global old_pressed_keys_repr
    global is_sleeping

    # Get relative paths to files that can be edited by the user:
    dictionaries_path: str = None
    keyboard_layout_path: str = None
    if is_it_being_executed_by_the_executable:
        dictionaries_path = os.path.join(os.path.dirname(sys.executable), '_internal', 'dictionaries.py')
        keyboard_layout_path = os.path.join(os.path.dirname(sys.executable), '_internal', 'keyboard_layout.py')

    try:
        if is_it_being_executed_by_the_executable:
            dictionaries = import_module_from_path('dictionaries', dictionaries_path)
            DICTIONARIES = dictionaries.DICTIONARIES
            MIRROR = dictionaries.MIRROR
            WAKE_UP_HOTKEYS = dictionaries.WAKE_UP_HOTKEYS
        else:
            from dictionaries import DICTIONARIES, MIRROR, WAKE_UP_HOTKEYS

        if not is_list_of_type(ChordDict, DICTIONARIES):
            raise ValueError(f'The "DICTIONARIES" binding of the file "dictionaries.py" should be a list of objects ChordDict, but received {str(DICTIONARIES)} that is of type {type(DICTIONARIES)}!')
        if not is_list_of_tuples_of_two_strs(MIRROR):
            raise ValueError(f'The "MIRROR" binding of the file "dictionaries.py" should be a list of tuples where each tuple should be a pair of strings, but received {str(MIRROR)} that is of type {type(MIRROR)}!')
        if not is_list_of_union_type([str, NonSuppressedHotkey], WAKE_UP_HOTKEYS):
            raise ValueError(f'The "WAKE_UP_HOTKEYS" binding of the file "dictionaries.py" should be a list of strings or objects NonSuppressedHotkey, but received {str(WAKE_UP_HOTKEYS)} that is of type {type(WAKE_UP_HOTKEYS)}!')
    except Exception as ex:
        trace = '\n    > ' + '\n    > '.join([line for line in traceback.format_exc().splitlines()])
        print("Module not found or import error occurred.", ex, trace)
        show_error("Error in 'dictionaries.py'", f"The file 'dictionaries.py' has an error. Fix it and try opening the program again.\n\n{ex}{trace}")
        return

    try:
        if is_it_being_executed_by_the_executable:
            keyboard_layout = import_module_from_path('keyboard_layout', keyboard_layout_path)
            KEY_ALIASES = keyboard_layout.KEY_ALIASES
        else:
            from keyboard_layout import KEY_ALIASES

        if not is_list_of_type(KeyAliases, KEY_ALIASES):
            raise ValueError(f'The "KEY_ALIASES" binding of the file "dictionaries.py" should be a list of objects KeyAliases, but received {str(KEY_ALIASES)} that is of type {type(KEY_ALIASES)}!')
    except Exception as ex:
        trace = '\n    > ' + '\n    > '.join([line for line in traceback.format_exc().splitlines()])
        print("Module not found or import error occurred.", ex, trace)
        show_error("Error in 'keyboard_layout.py'", f"The file 'keyboard_layout.py' has an error. Fix it and try opening the program again.\n\n{ex}{trace}")
        return

    # atexit.register(cleanup)

    # start up chord dictionaries and get it's problems:
    for cdict in DICTIONARIES:
        cdict.initialize(MIRROR, KEY_ALIASES)
        problems.extend(cdict.search_for_problems(DICTIONARIES))

    # check for problems of cdicts with the same name:
    cdicts_with_repeated_name_reported: set[ChordDict] = set()
    for cdict in DICTIONARIES:
        if cdict in cdicts_with_repeated_name_reported:
            continue # do not report repeated name problem of cdict again
        cdicts_with_the_same_name = [other_cdict for other_cdict in DICTIONARIES if other_cdict.name == cdict.name]
        if len(cdicts_with_the_same_name) > 1:
            problems.insert(0, f'> There are {len(cdicts_with_the_same_name)} Dictionaries with the name "{cdict.name}".')
            cdicts_with_repeated_name_reported.update(cdicts_with_the_same_name)

    # systray
    menu_options = (
        ("Toggle Active Dictionary Window", None, lambda _: GUI_PROCESS_PROXY.send(ToggleChordDict(active_chord_dict))),
        ("Show Problems", None, lambda _: show_problems_window()),
        ("Show Pressed Keys Data", None, lambda _: show_keys_data_window()),
        ("Show WAKE_UP_HOTKEYS", None, lambda _: show_message("WAKE_UP_HOTKEYS", "These hotkeys make the program wake up from sleeping:\n    > " + "\n    > ".join([(x if isinstance(x, str) else x.hotkey) for x in WAKE_UP_HOTKEYS]))),
        ("Restart", None, restart),
    )
    with SysTrayIcon("icon.ico", "OneHandTyper", menu_options, on_quit=cleanup) as st: # TODO add a file "icon.ico" next to "main.py"
        systray = st
        GUI_PROCESS_PROXY = init_GUIProcess()
        activate(DICTIONARIES[0])
        if problems:
            show_problems_window()

        def update_pressed_keys_widget():
            global pressed_keys_repr
            global old_pressed_keys_repr
            global is_sleeping
            global is_terminating
            while not is_terminating:
                time.sleep(1)  # one second
                if not is_sleeping:
                    if pressed_keys_repr and (old_pressed_keys_repr == pressed_keys_repr):
                        GUI_PROCESS_PROXY.send(UpdatePressedKeysWidget(pressed_keys_repr))
                    elif not pressed_keys_repr and old_pressed_keys_repr:
                        GUI_PROCESS_PROXY.send(HidePressedKeysWidget())
                    old_pressed_keys_repr = pressed_keys_repr[:]
            print(f"is terminating={is_terminating}, pressed_keys_widget_updater_thread finished.")

        pressed_keys_widget_updater_thread = threading.Thread(target=update_pressed_keys_widget)
        pressed_keys_widget_updater_thread.start()

        GUI_PROCESS_PROXY.join()
        print(f"is terminating={is_terminating}, with SysTrayIcon finished.")


def import_module_from_path(module_name, module_path):
    import importlib.util
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def show_problems_window():
    global problems
    GUI_PROCESS_PROXY.send(ShowAndUpdateProblemsWindow(problems))

def show_keys_data_window():
    GUI_PROCESS_PROXY.send(ShowKeysDataWindowIfNotVisible())

def update_keys_data_window_if_visible(ev: keyboard.KeyboardEvent):
    GUI_PROCESS_PROXY.send(UpdateKeysDataWindowIfVisible(format_event_to_key_data(ev)))

def format_event_to_key_data(ev: keyboard.KeyboardEvent):

    name = f"'{ev.name}'"
    if ev.name == None: name = "None" 
    elif ev.name == '': name = "''" 
    elif ev.name == '"': name = '\'"\''
    elif ev.name == "'": name = "\"'\""
    elif ev.name == "\\": name = "'\\\\'"
    is_keypad = str(ev.is_keypad)

    return f"    KeyEventData(scan_code={ev.scan_code}, name={name}, is_keypad={is_keypad}),"

def is_list_of_tuples_of_two_strs(value) -> bool:
    return is_list_of(lambda item: isinstance(item, tuple) and len(item) == 2 and all(isinstance(sub_item, str) for sub_item in item), value)

def is_list_of_union_type(types: list[Type], maybe_list) -> bool:
    return is_list_of(lambda item: any(isinstance(item, tp) for tp in types), maybe_list)

def is_list_of(predicate: Callable[[Any], bool], maybe_list) -> bool:
    if not isinstance(maybe_list, list): return False
    return all(predicate(item) for item in maybe_list)

def get_key_representation(x: keyboard.KeyboardEvent | KeyAliases):
    global KEY_ALIASES
    if isinstance(x, KeyAliases): return x.user_key_representation
    key_aliases = find(KEY_ALIASES, lambda keyals: KeyEventData.fromKeyboardEvent(x) in keyals.aliases, None)
    if key_aliases: return key_aliases.user_key_representation
    return x.name.lower() if x.name else f"(scan_code={x.scan_code}, is_keypad={str(x.is_keypad)})"
    
def get_togglable_key_states() -> tuple[str]: # based on code of module 'keyboard' `_winkeyboard.py`
    """ Returns a tuple that may include the strings `'num lock'`, `'caps lock'` and/or `'scroll lock'`. The tuple contains those that are currently active. """
    modifiers = (
            ('num lock',) * (user32.GetKeyState(0x90) & 1) +
            ('caps lock',) * (user32.GetKeyState(0x14) & 1) +
            ('scroll lock',) * (user32.GetKeyState(0x91) & 1)
        )
    return modifiers

def areEquivalentChords(chord_keys_repr1: set[str], chord_keys_repr2: set[str]):
    if not chord_keys_repr1: return False
    if not chord_keys_repr2: return False
    chord_keys_repr1 = {key.lower() for key in chord_keys_repr1}
    chord_keys_repr2 = {key.lower() for key in chord_keys_repr2}
    if chord_keys_repr1 == chord_keys_repr2: return True

class DataOfChordMadeByTheUser(TypedDict):
    keys_repr_of_chord_made_by_the_user: Set[str]
    ev_key_repr: str
    ev_is_key_repeat: bool

def basic_processing_of_key_event(ev: keyboard.KeyboardEvent) -> None | Union[None, DataOfChordMadeByTheUser]:
    global active_chord_dict
    global pressed_keys_repr
    global is_waiting_release_all_pressed_keys
    global holding_keys
    global is_sleeping

    old_pressed_keys_repr = pressed_keys_repr[:]
    key_repr = get_key_representation(ev)
    is_key_repeat = ev.event_type == 'down' and key_repr in pressed_keys_repr
    if ev.event_type == 'down':
        if not key_repr in pressed_keys_repr: pressed_keys_repr.append(key_repr)
        if not is_key_repeat: update_keys_data_window_if_visible(ev)
    else:
        if key_repr in pressed_keys_repr: pressed_keys_repr.remove(key_repr)

    # if not is_sleeping and (old_pressed_keys_repr != pressed_keys_repr):
    #     GUI_PROCESS_PROXY.send(UpdatePressedKeysWidget(pressed_keys_repr)) # key up

    if ev.event_type == 'down':
        is_waiting_release_all_pressed_keys = False # user está fazendo ou segurando um novo chord que deverá ser processado
    print('SLEEPING - ' if is_sleeping else '' + str(ev), key_repr, pressed_keys_repr, f'is_key_repeat={is_key_repeat} holding_keys={holding_keys} active_chord_dict={active_chord_dict.name}')
    if is_waiting_release_all_pressed_keys: return # user está soltando as teclas após ter feito um chord
    if not ev.event_type == 'up' and not is_key_repeat: return # user está ainda pressionando as teclas, ignorar o chord atual em pressed_keys e aguardar até ele soltar uma das teclas ou segurá-las mais tempo (até ocorrer is_key_repeat==True)

    chord_keys_repr: set[str] = {*pressed_keys_repr, key_repr} # chord que o user fez (segurou ou começou a soltar)
    is_waiting_release_all_pressed_keys = True
    return dict(
        keys_repr_of_chord_made_by_the_user = chord_keys_repr,
        key_repr = key_repr,
        is_key_repeat = is_key_repeat,
    )

def process_watched_key_event(ev: keyboard.KeyboardEvent):
    global active_chord_dict
    global is_waiting_release_all_pressed_keys
    global holding_keys

    r = basic_processing_of_key_event(ev)
    if not r: return

    for entry in active_chord_dict.entries: 
        if areEquivalentChords(entry.chord_keys(), r['keys_repr_of_chord_made_by_the_user']) or areEquivalentChords(entry.mirrored_chord_keys(), r['keys_repr_of_chord_made_by_the_user']):
            if isinstance(entry, Tap):
                try:
                    print(entry.__class__.__name__, entry.target_key)
                    if entry.tap_with_num_lock_disabled and 'num lock' in get_togglable_key_states(): # should disable 'num lock'
                        keyboard.press_and_release('num lock') # disable
                        tap(entry)
                        keyboard.press_and_release('num lock') # re-enable
                    else:
                        tap(entry)
                except Exception as ex:
                    # keyboard module stops to work, so we need restart the program
                    keyboard.unhook_all()
                    print(f'Invalid Action to perform: {entry}', ex)
                    show_error(f'Invalid Action to perform: {entry}', f'An error ocurred when trying to perform {entry.__class__.__name__} "{entry.target_key}". To prevent this issue from recurring, update the value "{entry.target_key}" in the entry {entry} of the dictionary "{active_chord_dict.name}" to a valid value (e.g., "a", "num 5", "ctrl+shift+e", etc.).\n\nThe program will RESTART.\n\nThe following error occurred:\n\n{ex}')
                    restart(systray)
                release_all_keys_being_hold_only_until_the_next_key_tap() # press_and_release was a key tap
                keys_released = entry.target_key.split('+')
                for key in keys_released:
                    repress_key_if_needed(key) # Se a key liberada no event deve ficar sendo pressionada pelo OneHandTyper, voltar a segurá-la
            elif isinstance(entry, Hold):
                print(entry.__class__.__name__, entry.target_key)
                if entry.target_key in holding_keys:
                    if not holding_keys[entry.target_key]: # hold_only_until_the_next_key_tap é false significando que está segurando até ser desativado, então desativar
                        print(f'Desativando Holding de {entry.target_key} ...: {holding_keys}')
                        del holding_keys[entry.target_key]
                        GUI_PROCESS_PROXY.send(UpdateHoldindKeysWidget(holding_keys))
                        keyboard.release(entry.target_key)
                        print(f'Desativando Holding de {entry.target_key} done!: {holding_keys}')
                    else: # hold_only_until_the_next_key_tap é true significando que deve-se torná-lo false para segurar até a desativação
                        holding_keys[entry.target_key] = False
                        GUI_PROCESS_PROXY.send(UpdateHoldindKeysWidget(holding_keys))
                else:
                    try:
                        keyboard.press(entry.target_key)
                        holding_keys[entry.target_key] = True
                        GUI_PROCESS_PROXY.send(UpdateHoldindKeysWidget(holding_keys))
                    except Exception as ex:
                        # keyboard module stops to work, so we need restart the program
                        keyboard.unhook_all()
                        print(f'Invalid Action to perform: {entry}', ex)
                        show_error(f'Invalid Action to perform: {entry}', f'An error ocurred when trying to perform {entry.__class__.__name__} "{entry.target_key}". To prevent this issue from recurring, update the value "{entry.target_key}" in the entry {entry} of the dictionary "{active_chord_dict.name}" to a valid value (e.g., "a", "num 5", "ctrl+shift+e", etc.).\n\nThe program will RESTART.\n\nThe following error occurred:\n\n{ex}')
                        restart(systray)
            elif isinstance(entry, Write):
                try:
                    print(entry.__class__.__name__, entry.text_to_write)
                    release_all_keys_being_hold()
                    keyboard.write(entry.text_to_write)
                except Exception as ex:
                    # keyboard module stops to work, so we need restart the program
                    keyboard.unhook_all()
                    print(f'Invalid Action to perform: {entry}', ex)
                    show_error(f'Invalid Action to perform: {entry}', f'An error ocurred when trying to perform {entry.__class__.__name__} "{entry.text_to_write}". To prevent this issue from recurring, update the value "{entry.text_to_write}" in the entry {entry} of the dictionary "{active_chord_dict.name}" to a valid value (e.g., "a", "my_email@email.com", ";", etc.).\n\nThe program will RESTART.\n\nThe following error occurred:\n\n{ex}')
                    restart(systray)
            elif isinstance(entry, ActivateChordDict):
                print(entry.__class__.__name__, entry.target_chord_dict_name)
                target_dict = find(DICTIONARIES, lambda cdict: cdict.name==entry.target_chord_dict_name, None)
                if target_dict:
                    activate(target_dict)
                else:
                    msg = f'> Could not find a Dictionary with the name "{entry.target_chord_dict_name}" to activate it!'
                    print(msg)
                    problems.insert(0, msg)
                    show_problems_window()
            elif isinstance(entry, ToggleActiveChordDictWindow):
                print(entry.__class__.__name__, active_chord_dict.name)
                GUI_PROCESS_PROXY.send(ToggleChordDict(active_chord_dict))
            elif isinstance(entry, Quit):
                print(entry.__class__.__name__)
                systray.shutdown()
            elif isinstance(entry, Restart):
                print(entry.__class__.__name__)
                restart(systray)
            elif isinstance(entry, FunctionCall):
                print(entry.__class__.__name__, entry.function_as_str)
                try:
                    FUNCTION_CALL_CALLABLES[entry]()
                except Exception as ex:
                    trace = '\n    > ' + '\n    > '.join([line for line in traceback.format_exc().splitlines()])
                    msg = f'> An exception occurred while calling the function for {str(entry)}: "{ex}":{trace}'
                    print(msg)
                    problems.insert(0, msg)
                    show_problems_window()
            elif isinstance(entry, Sleep):
                print(entry.__class__.__name__, r['keys_repr_of_chord_made_by_the_user'])
                sleep()
            break

def sleep():
    global is_waiting_release_all_pressed_keys
    global is_sleeping
    
    print('Sleeping...')
    is_sleeping = True

    # disable keyboard hooks (do not supress keys anymore) and release keys being hold:
    keyboard.unhook_all()
    release_all_keys_being_hold()
    # hide cdics:
    for cdict in DICTIONARIES:
        GUI_PROCESS_PROXY.send(HideChordDict(cdict))
    GUI_PROCESS_PROXY.send(HideProblemsWindow())
    GUI_PROCESS_PROXY.send(HideKeysDataWindow())
    GUI_PROCESS_PROXY.send(HideActiveChordDictNameWidget())
    GUI_PROCESS_PROXY.send(HidePressedKeysWidget())
    # listen for WAKE_UP_HOTKEYS:
    for hotkey in WAKE_UP_HOTKEYS:
        if isinstance(hotkey, NonSuppressedHotkey):
            pass # process_non_watched_key_event() will take care of watch this hotkey
        else:
            keyboard.add_hotkey(hotkey, wake_up, args=(), suppress=True, trigger_on_release=True)
    keyboard.hook(process_non_watched_key_event) # watch the `NonSuppressedHotkey`s
    print('Sleeping done!')

def wake_up():
    print('Waking up...')
    global is_waiting_release_all_pressed_keys
    global active_chord_dict
    global is_sleeping
    global pressed_keys_repr

    is_sleeping = False
    keyboard.unhook_all() # should unhook all WAKE_UP_HOTKEYS
    is_waiting_release_all_pressed_keys = True # Waiting for the keys that were pressed during the ‘Wake Up Hotkey’ to be released
    activate(active_chord_dict)
    if pressed_keys_repr: GUI_PROCESS_PROXY.send(UpdatePressedKeysWidget(pressed_keys_repr))
    print('Wake up done!')

def show_error(title: str | None = None, message: str | None = None):
    root = tk.Tk()
    root.withdraw()  # This hides the main window
    messagebox.showerror(title, message)
    root.quit()

def show_message(title: str | None = None, message: str | None = None):
    root = tk.Tk()
    root.withdraw()  # This hides the main window
    messagebox.showinfo(title, message)
    root.quit()

def tap(entry: Tap):
    keyboard.press_and_release(entry.target_key)

def release_all_keys_being_hold_only_until_the_next_key_tap():
    global holding_keys
    keys_to_release = [key for key in holding_keys if holding_keys[key]]
    for key in keys_to_release: # release all keys being hold_only_until_the_next_key_tap
        keyboard.release(key)
        del holding_keys[key]
    GUI_PROCESS_PROXY.send(UpdateHoldindKeysWidget(holding_keys))

def process_non_watched_key_event(ev: keyboard.KeyboardEvent):
    """ Ignores the event if it belongs to a key present in the `active_chord_dict` and the program is sleeping, otherwise processes the event. """

    global active_chord_dict
    global is_sleeping

    r = basic_processing_of_key_event(ev)

    print('GLOBAL')

    if not is_sleeping:
        # ignore `ev` if its key is watched (the watched keys will be processed in `process_watched_key_event()`):
        if ev.scan_code in active_chord_dict.all_watched_keys: return
        if ev.name and str(ev.name).lower() in active_chord_dict.all_watched_keys: return
        if ev.name and ev.name in active_chord_dict.all_watched_keys: return

    if not is_sleeping:
        if ev.event_type == 'up':
            release_all_keys_being_hold_only_until_the_next_key_tap() # was a key tap of a non watched key
            repress_key_if_needed(str(ev.name).lower()) # Se a key liberada no event deve ficar sendo pressionada pelo OneHandTyper, voltar a segurá-la
    
    if is_sleeping and r: # `NonSuppressedHotkey`s inside WAKE_UP_HOTKEYS should be checked by this method
        hotkeys_to_check = [x.hotkey for x in WAKE_UP_HOTKEYS if isinstance(x, NonSuppressedHotkey)]
        for hotkey in hotkeys_to_check:
            keys = set(hotkey.split('+'))
            if areEquivalentChords(keys, r["keys_repr_of_chord_made_by_the_user"]):
                wake_up()
                break

def install_hooks_that_are_independent_of_chord_dicts():
    keyboard.hook(process_non_watched_key_event)
    
def activate(cdict: ChordDict):
    global active_chord_dict
    
    #unhook previous active_chord_dict:
    keyboard.unhook_all()
    install_hooks_that_are_independent_of_chord_dicts() # reinstall these hooks

    #define and activate new active_chord_dict cdict:
    active_chord_dict = cdict
    for watchkey in cdict.all_watched_keys:
        try:
            keyboard.hook_key(watchkey, process_watched_key_event, suppress=True)
        except Exception as ex:
            trace = '\n        > ' + '\n        > '.join([line for line in traceback.format_exc().splitlines()])
            entries = [entry for entry in cdict.entries if watchkey in (entry.chord_keys() | entry.mirrored_chord_keys())]
            msg = f'> The dictionary "{cdict.name}" contains {len(entries)} ' \
                f'{"entry with an" if len(entries) == 1 else "entries with"} invalid ' \
                f'{"chord" if len(entries) == 1 else "chords"}:' + \
                f'\n    > ' + f'\n    > '.join([str(entry) for entry in entries]) + \
                f'\n    > The problem is that the ' \
                f'{"chord" if len(entries) == 1 else "chords"} of ' \
                f'{"this entry contains" if len(entries) == 1 else "these entries contain"}' \
                f' the invalid key "{watchkey}" {ex}:{trace}'

            if not msg in problems:
                problems.insert(0, msg)
                show_problems_window()

    GUI_PROCESS_PROXY.send(ShowAndUpdateActiveChordDictNameWidget(cdict.name))

def repress_key_if_needed(key):
    global holding_keys
    # Se a key deve ficar sendo pressionada pelo OneHandTyper, voltar a segurá-la:
    if key in holding_keys and holding_keys[key] == False:
        print('Repressionar tecla segurada ', key)
        keyboard.press(key)

def cleanup(systray = None):
    global is_terminating
    global GUI_PROCESS_PROXY
    
    if __name__ == '__main__' and not is_terminating: # is_terminating avoids systray.shutdown() running cleanup()'s code multiple times
        is_terminating = True
        GUI_PROCESS_PROXY.send(FinishGUIProcess())
        keyboard.unhook_all()
        release_all_keys_being_hold()
        GUI_PROCESS_PROXY.join()
        print('OneHandTyper finished.')
        # sys.exit(0) # todas as threads devem ser finalizadas antes de chamar sys.exit(0)

def release_all_keys_being_hold():
    for key_being_hold in holding_keys:
        keyboard.release(key_being_hold)
    holding_keys.clear()
    GUI_PROCESS_PROXY.send(UpdateHoldindKeysWidget(holding_keys))

def restart(systray):
    try:
        systray.shutdown()
    except Exception as ex:
        print('Exception durante systray.shutdown() dentro de restart(): ', ex)
        cleanup()
    os.execv(sys.executable, ['python'] + [f'"{arg}"' for arg in sys.argv])

if __name__ == '__main__':
    is_it_being_executed_by_the_executable: bool = getattr(sys, 'frozen', False)
    freeze_support()
    print('Running from executable!' if is_it_being_executed_by_the_executable else 'Running from the command line or IDE!')
    start(is_it_being_executed_by_the_executable)