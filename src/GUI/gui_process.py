import queue
import time
import tkinter as tk
from tkinter import TclError, ttk
from multiprocessing import Process, Queue
from abc import ABC, abstractmethod
from typing import Iterable, TypeVar, Callable

from classes import ChordDict
from GUI.gui_factories import create_floating_widget, create_problems_window, create_keys_data_window

R = TypeVar("R")  # Type variable for the return type

class _GUIState:
    def __init__(self):
        self.chord_dict_windows: dict[str, tk.Tk] = {}
        """ `dict[chord_dict_name, chord_dict_window]` """
        self.holding_keys_widget: tk.Tk | None = None
        """ A window with method `set_text(new_text: str)` """
        self.pressed_keys_widget: tk.Tk | None = None
        """ A window with method `set_text(new_text: str)` """
        self.active_chord_dict_name_widget: tk.Tk | None = None
        """ A window with method `set_text(new_text: str)` """
        self.problems_window: tk.Tk | None = None
        """ A window with method `set_problems(problems: list[str])` """
        self.keys_data_window: tk.Tk | None = None
        """ A window with method `prepend_key_data(line: str)` """

class GUICommand(ABC):
    pass

class FinishGUIProcess(GUICommand):
    pass

class ExecutableGUICommand(GUICommand):
    @abstractmethod
    def execute(self, gui_state: _GUIState):
        pass

class UpdateHoldindKeysWidget(ExecutableGUICommand):

    def __init__(self, holding_keys: dict[str, bool]):
        self.holding_keys = holding_keys
        """ `dict[target_key_being_hold, hold_only_until_the_next_key_tap]` """

    def execute(self, gui_state: _GUIState):
        holding_keys_str = self.holding_keys_to_str()
        print(f'UpdateHoldindKeysWidget with "{holding_keys_str}"')

        if not self.holding_keys:
            if gui_state.holding_keys_widget:
                try:
                    print('gui_state.holding_keys_widget.withdraw() ...')
                    gui_state.holding_keys_widget.withdraw()
                    gui_state.holding_keys_widget.set_text('')
                    print('gui_state.holding_keys_widget.withdraw() done!')
                except TclError as ex:
                    print(f'Exception when doing the withdraw() of the window of the holding_keys_widget:', ex.__class__, ex)
                    gui_state.holding_keys_widget = None
            return # do nothing, widget is already not visible

        # if holding keys:

        def create_widget_in_GUIState():
            w = create_floating_widget(holding_keys_str, y=35)
            setattr(gui_state, 'holding_keys_widget', w)
            return w

        widget = make_window_visible(lambda: gui_state.holding_keys_widget, lambda: setattr(gui_state, 'holding_keys_widget', None), create_widget_in_GUIState)

        widget.set_text(holding_keys_str)

    def holding_keys_to_str(self):
        return ' '.join([key if self.holding_keys[key] else f'[{key}]' for key in self.holding_keys])
    
class UpdatePressedKeysWidget(ExecutableGUICommand): # TODO very duplicated with UpdateHoldindKeysWidget
    """ updates the widget that shows the keys that the user is pressing now. """

    def __init__(self, pressed_keys: list[str]):
        self.pressed_keys = pressed_keys

    def execute(self, gui_state: _GUIState):
        pressed_keys_str = self.pressed_keys_to_str()
        print(f'UpdatePressedKeysWidget with "{pressed_keys_str}"')

        if not self.pressed_keys:
            if gui_state.pressed_keys_widget:
                try:
                    # print('gui_state.pressed_keys_widget.withdraw() ...')
                    gui_state.pressed_keys_widget.withdraw()
                    gui_state.pressed_keys_widget.set_text('')
                    # print('gui_state.pressed_keys_widget.withdraw() done!')
                except TclError as ex:
                    # print(f'Exception when doing the withdraw() of the window of the pressed_keys_widget:', ex.__class__, ex)
                    gui_state.pressed_keys_widget = None
            return # do nothing, widget is already not visible

        # if pressed keys:

        def create_widget_in_GUIState():
            w = create_floating_widget(pressed_keys_str, y=70, text_fill="yellow")
            setattr(gui_state, 'pressed_keys_widget', w)
            return w

        widget = make_window_visible(lambda: gui_state.pressed_keys_widget, lambda: setattr(gui_state, 'pressed_keys_widget', None), create_widget_in_GUIState)

        widget.set_text(pressed_keys_str)

    def pressed_keys_to_str(self):
        return ' '.join([key for key in self.pressed_keys])
    
class HidePressedKeysWidget(ExecutableGUICommand):

    def execute(self, gui_state: _GUIState):
        print(f'HidePressedKeysWidget')
        hide_window(lambda: gui_state.pressed_keys_widget, lambda: setattr(gui_state, 'pressed_keys_widget', None))

class ShowAndUpdateActiveChordDictNameWidget(ExecutableGUICommand):

    def __init__(self, active_chord_dict_name: str):
        self.active_chord_dict_name = active_chord_dict_name

    def execute(self, gui_state: _GUIState):
        print(f'UpdateActiveChordDictNameWidget with "{self.active_chord_dict_name}"')

        def create_widget_in_GUIState():
            w = create_floating_widget(self.active_chord_dict_name, width=150)
            setattr(gui_state, 'active_chord_dict_name_widget', w)
            return w

        widget = make_window_visible(lambda: gui_state.active_chord_dict_name_widget, lambda: setattr(gui_state, 'active_chord_dict_name_widget', None), create_widget_in_GUIState)

        widget.set_text(self.active_chord_dict_name)

class HideActiveChordDictNameWidget(ExecutableGUICommand):

    def execute(self, gui_state: _GUIState):
        print(f'HideActiveChordDictNameWidget')
        hide_window(lambda: gui_state.active_chord_dict_name_widget, lambda: setattr(gui_state, 'active_chord_dict_name_widget', None))
    
def hide_window(get_window_from_GUIState: Callable[[], tk.Tk | None], del_window_from_GUIState: Callable[[], None]):
    window = get_window_from_GUIState()
    if window:
        try:
            # print('doing withdraw() over the window...')
            window.withdraw()
            # print('withdraw() done!')
        except TclError as ex:
            print(f'Exception when doing the withdraw() of window:', ex.__class__, ex)
            del_window_from_GUIState()
    # else do nothing, windown is already not visible

class ShowAndUpdateProblemsWindow(ExecutableGUICommand):

    def __init__(self, problems: list[str]):
        self.problems = problems

    def execute(self, gui_state: _GUIState):
        print(f'UpdateProblemsWindow with {len(self.problems)} problems')

        problems_or_no_problems = lambda: self.problems if self.problems else ['No problems to show :)']

        def create_window_in_GUIState():
            w = create_problems_window(problems_or_no_problems())
            setattr(gui_state, 'problems_window', w)
            return w

        window = make_window_visible(lambda: gui_state.problems_window, lambda: setattr(gui_state, 'problems_window', None), create_window_in_GUIState)

        window.set_problems(problems_or_no_problems())
        window.deiconify()
        window.focus_force()

class HideProblemsWindow(ExecutableGUICommand):

    def execute(self, gui_state: _GUIState):
        print(f'HideProblemsWindow')
        hide_window(lambda: gui_state.problems_window, lambda: setattr(gui_state, 'problems_window', None))

class UpdateKeysDataWindowIfVisible(ExecutableGUICommand):
    
    def __init__(self, new_key_data: str):
        self.new_key_data = new_key_data

    def execute(self, gui_state: _GUIState):
        # print(f'UpdateKeysDataWindowIfVisible with {self.new_key_data}')

        window = get_window_if_visible(lambda: gui_state.keys_data_window)
        if not window: return

        window.prepend_key_data(self.new_key_data)
        window.deiconify()
        window.focus_force()

class ShowKeysDataWindowIfNotVisible(ExecutableGUICommand):

    def execute(self, gui_state: _GUIState):
        print(f'ShowKeysDataWindowIfNotVisible')

        window = get_window_if_visible(lambda: gui_state.keys_data_window)
        if window: return # alread visible

        def create_window_in_GUIState():
            w = create_keys_data_window()
            setattr(gui_state, 'keys_data_window', w)
            return w

        make_window_visible(lambda: gui_state.keys_data_window, lambda: setattr(gui_state, 'keys_data_window', None), create_window_in_GUIState)

class HideKeysDataWindow(ExecutableGUICommand):

    def execute(self, gui_state: _GUIState):
        print(f'HideKeysDataWindow')
        hide_window(lambda: gui_state.keys_data_window, lambda: setattr(gui_state, 'keys_data_window', None))

def get_window_if_visible(get_window_from_GUIState: Callable[[], tk.Tk | None]):
    window = get_window_from_GUIState()
    if not window: return None
    try:
        if not window.winfo_exists(): return None
        if not window.winfo_viewable(): return None
        return window
    except TclError as ex:
        print(f'Exception when doing the winfo_exists/winfo_viewable of a window:', ex.__class__, ex)
    return None

def make_window_visible(get_window_from_GUIState: Callable[[], tk.Tk | None], del_window_from_GUIState: Callable[[], None], create_window_in_GUIState: Callable[[], R]):
    window = get_window_from_GUIState()
    if window:
        try:
            if window.winfo_exists():
                if not window.winfo_viewable():
                    window.deiconify()
                # else: nothing to do, the window is alread visible
                return window
            else:
                del_window_from_GUIState()
                return create_window_in_GUIState() # recreate window since it does not exists anymore
        except TclError as ex:
            print(f'Exception when doing the winfo_exists/winfo_viewable/deiconify() of a window:', ex.__class__, ex)
            del_window_from_GUIState()
            return create_window_in_GUIState() # recreate window since it does not exists anymore
    else:
        return create_window_in_GUIState() # (re)create window since it does not exists yet/anymore

class ShowChordDict(ExecutableGUICommand):

    def __init__(self, cdict: ChordDict):
        self.cdict = cdict

    def execute(self, gui_state: _GUIState):
        print(f'ShowChordDict "{self.cdict.name}"...')

        make_window_visible(lambda: gui_state.chord_dict_windows[self.cdict.name] if self.cdict.name in gui_state.chord_dict_windows else None, lambda: gui_state.chord_dict_windows.pop(self.cdict.name), lambda: gui_state.chord_dict_windows.update({self.cdict.name: self.create_window_for_cdict()}) )

        print(f'ShowChordDict "{self.cdict.name}" done!')

    def create_window_for_cdict(self): # TODO: move to gui_factories.py
        window = tk.Tk()
        window.title(self.cdict.name)
        window.geometry('600x400')
            
        # Create the treeview
        table = ttk.Treeview(window, columns = ('action', 'chord', 'mirrored_chord') if self.cdict.mirrorChords else ('action', 'chord'), show='headings')
        table.heading('action', text='Action')
        table.heading('chord', text='Chord')
        # Set the minimum width for the first column (column '#0')
        table.column(0, width=400)
        table.column(1, width=100)
        if self.cdict.mirrorChords:
            table.heading('mirrored_chord', text='Mirrored Chord')
            table.column(2, width=100)
        table.pack(fill='both', expand=True)

        for entry in self.cdict.entries:
            action = entry.action_to_str()
            chord = entry.chord
            table.insert(parent='', index=tk.END, values = (action, chord, entry.mirrored_chord) if self.cdict.mirrorChords else (action, chord))

        window.deiconify()
        window.focus_force()
            
        return window

class HideChordDict(ExecutableGUICommand):

    def __init__(self, cdict: ChordDict):
        self.cdict = cdict

    def execute(self, gui_state: _GUIState):
        print(f'HideChordDict "{self.cdict.name}"...')
        if self.cdict.name in gui_state.chord_dict_windows:
            window = gui_state.chord_dict_windows[self.cdict.name]
            try:
                window.withdraw()
            except TclError as ex:
                print(f'Exception when doing the withdraw() of the window of the ChordDict "{self.cdict.name}":', ex.__class__, ex)
                del gui_state.chord_dict_windows[self.cdict.name]
        print(f'HideChordDict "{self.cdict.name}" done!')

class ToggleChordDict(ExecutableGUICommand):

    def __init__(self, cdict: ChordDict):
        self.cdict = cdict

    def execute(self, gui_state: _GUIState):

        should_show = False
        if self.cdict.name in gui_state.chord_dict_windows:
            window = gui_state.chord_dict_windows[self.cdict.name]
            try:
                if window.winfo_exists():
                    if window.winfo_viewable():
                        should_show = False # cdict window is already being show, so, should hide it
                    else:
                        should_show = True # cdict window is not being show, so, should show it
                else:
                    del gui_state.chord_dict_windows[self.cdict.name]
                    should_show = True # cdict window is not being show, so, should show it
            except TclError as ex:
                print(f'Exception when doing the winfo_exists/winfo_viewable() of the window of the ChordDict "{self.cdict.name}":', ex.__class__, ex)
                del gui_state.chord_dict_windows[self.cdict.name]
                should_show = True # probaly cdict window is not being show, so, should show it
        else:
            should_show = True # probaly cdict window is not being show, so, should show it

        if should_show:
            ShowChordDict(self.cdict).execute(gui_state)
        else:
            HideChordDict(self.cdict).execute(gui_state)

class GUIProcessProxy:

    def __init__(self, gui_process: Process, gui_queue: Queue):
        self._gui_queue = gui_queue
        self._gui_process = gui_process

    def send(self, gui_command: GUICommand):
        self._gui_queue.put(gui_command)

    def join(self):
        self._gui_process.join()


def init_GUIProcess():
    gui_queue = Queue()

    # Create a separate process for the GUI
    gui_process = Process(target=_gui_process, args=(gui_queue,))
    gui_process.start()
    
    return GUIProcessProxy(gui_process, gui_queue)
    

def _gui_process(gui_queue):
    print('GUI Process started.')

    process_tk = tk.Tk()
    process_tk.withdraw()

    gui_state: _GUIState = _GUIState()

    def check_gui_queue_for_next_command():
        
        should_finish = False
        try:
            command: GUICommand = gui_queue.get_nowait()
            if isinstance(command, FinishGUIProcess):
                print('Finishing GUI...')
                try:
                    process_tk.quit()
                except Exception as ex:
                    print(f'Exception when finishing GUI process: ', ex)
                should_finish = True
                print('GUI Finished!')
            elif isinstance(command, ExecutableGUICommand):
                command.execute(gui_state)
            else:
                raise f"Unknow Command {command} of class {command.__class__}!"
        except queue.Empty:
            pass
        if not should_finish:
            process_tk.after(100, check_gui_queue_for_next_command)

    process_tk.after(1000, check_gui_queue_for_next_command)

    process_tk.mainloop()

    print('GUI Process finished.')