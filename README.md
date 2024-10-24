## About this program
*OneHandTyper* allows you to **type and make keyboard shortcuts using just one hand**, either your left or right hand. This program could probably also be used to remap the keyboard (including experimental keyboards) and perhaps even be used for stenography.

The current version probably only works on Windows operating system.

## What is it like to type using this program?
You will often need to press multiple keys together (chord) to enter a single key. There are editable dictionaries (`dictionaries.py`) that allow you to define which chord triggers which key. For example, pressing `A+F` causes the `B` key to be typed.
> You can quickly get a feel for what it's like to type using this program by opening the `proof of concept\index.html` file in your browser.

> Please note that your experience using this program may be completely different if you modify the dictionaries. For example, you can create a dictionary that mirrors the other half of the keyboard while the space bar is held down (for example, pressing the `F` key activates the `F` key, but pressing `F+SPACE` activates the `J` key instead).

> Currently, the dictionaries in this program are set to work with the `ABNT2` keyboard, which has the `ç` key. You can change this in the `dictionaries.py` file (see below about this) by changing the tuple `('a', 'ç')` in the `MIRRORS` property. To change this in the `proof of concept\index.html` file, change the values ​​of the `newKey` (change `.replace('a', 'ç')`) and `keysToIgnore` (change `'ç'`) properties. There may be more keys that you will need to adjust for your keyboard layout.

## How to run this program
1. Click the green "Code" button on this page and then click "Download ZIP";
![Buttons to Download The Program](<images/download ZIP.jpg>)
2. Find and extract the downloaded ZIP file;
3. Optional step: rename the extracted folder (the folder that contains the `src` folder, the `OneHandTyper.bat` file, the `README.md` file, etc.) to `OneHandTyper` and place it in the permanent location where you want it to be (maybe inside the programs folder);
4. Double click on the file `dist\Executable\OneHandTyper.exe` (that is, the `OneHandTyper.exe` file that is inside the `Executable` folder that is inside the `dist` folder).
    > You can [create a shortcut](https://www.youtube.com/watch?v=HzrA3A3GrPQ) to the file `OneHandTyper.exe` and place this shortcut on the desktop or wherever you want. You can place it, for example, in the startup folder so that this program starts up together with Windows.


> If for some reason the above steps do not work, you can try running the program using the `Advanced Execution` steps below.

## Advanced Execution
1. Install `Python 3` (download the installer [here](https://www.python.org/), this [video](https://www.youtube.com/watch?v=28eLP22SMTA) can help you install it correctly);
    - DO NOT add Python to the `PATH`;
        - By doing this, you prevent programs on your computer that use a different version of Python obtained through PATH from stopping working;
    - Use the installer to install `pip` (*Package Installer for Python*) along with Python;
    - Copy the path where Python will be installed and paste it into Notepad, as you will need this path later.
        - It will probably be installed in the path `C:\Users\<your-name>\AppData\Local\Programs\Python\Python<version-number>\python.exe`;
        - For example, on my computer Python `3.12.5` was installed in the path `C:\Users\dougl\AppData\Local\Programs\Python\Python312\python.exe`.
2. Open the Windows console (`Windows+R`, type `cmd` and press `Enter`), use the `cd` command to navigate to the program folder (the one that contains the `src` folder and the `README.md` file, and which you may have renamed to `OneHandTyper` as suggested), making a command like `cd "path/to/OneHandTyper"` (note that the path is written in quotes);
![cd command](<images/cd command.jpg>)

3. Now, you will run a command to create a `Virtual Environment` in the program folder (This [video](https://www.youtube.com/watch?v=KxvKCSwlUv8) may help you understand what this is). In this command, you will use the Python installation path that you saved in Notepad (this path must be written in quotes if there are spaces in it) forming a command like `C:\Users\<your-name>\AppData\Local\Programs\Python\Python<version-number>\python.exe -m venv .venv`;
![Command to create virtual environment](<images/create virtual environment.jpg>)
If the command works, a folder called `.venv` will be created inside the program folder.

4. Now you need to run a command that **activates** the virtual environment in the console. The exact command to activate the virtual environment depends on your operating system and which console you are using. When you successfully activate the virtual environment, you will see `(.venv)` (note that it is written in parentheses) appear before the program path in the console. Try the following commands to activate the virtual environment:
    - `.venv\Scripts\activate.bat` (cmd.exe in Windows);
    - `.venv\bin\activate.bat` (Linux);
    - `.venv\Scripts\Activate.ps1` (PowerShell in Windows);
    - `.venv\bin\Activate.ps1`;
    - `source .venv\Scripts\activate` or `source .venv\bin\activate` (Git Bash / Linux / Mac);
![Command to activate virtual environment](<images/activate virtual environment.jpg>)

5. The final preparation step is to install the project dependencies in the virtual environment. To do this, run the `pip install -r requirements.txt` command and after it finishes, run the `pip install -r requirements-dev.txt` command (this will be useful for regenerating the executable `dist\Executable\OneHandTyper.exe` if necessary).
- WARNING: Always be sure to run these `pip install` commands while the console has the virtual environment activated, simply check if `(.venv)` appears before the program path in the console, something like `(.venv) path\to\OneHandTyper>` instead of just `path\to\OneHandTyper>`.
![Commands to install requirements](<images/install requirements.jpg>)

6. You can now run the program in the console using the `.venv\Scripts\python.exe src\main.py` command, as long as the virtual environment is activated in the console.
![Command to run the program](<images/run the program.jpg>)

7. When you want to start the program without typing commands in the console, double-click the file named `OneHandTyper.vbs` or the file named `OneHandTyper.bat`.
    > Using `OneHandTyper.bat` causes the console to remain open while using the program. You can see more information about what is happening in the program in the open console, this can be useful for troubleshooting.

    > You can [create a shortcut](https://www.youtube.com/watch?v=HzrA3A3GrPQ) to the file `OneHandTyper.vbs` and place this shortcut on your desktop or in another folder. You can place it, for example, in the startup folder so that this program starts up together with Windows.

### Running the program through PowerShell
Open `PowerShell` in the program folder (the folder containing the files `OneHandTyper.vbs` and `OneHandTyper.bat`) and try running the following commands:

1. `.venv/Scripts/Activate.ps1`
2. `.venv/Scripts/python.exe src/main.py`

In the context of the image below, the folder containing the files `OneHandTyper.vbs` and `OneHandTyper.bat` is called `OneHandTyper`, and it also contains the folders `.venv` and `src`. Here's how the above commands are executed in PowerShell:
![PowerShell commands to activate the virtual environment and run the program](<images/PowerShell OneHandTyper.jpg>)

#### To open Powershell in a specific folder in Windows:
- Right-click on that folder while holding `SHIFT`, Then select from the context menu the option that allows you to open PowerShell "here"; or
- With the folder open in Windows File Explorer, click on the `File` tab in the File Explorer (top left corner), then click on the option to open PowerShell; or
- With the folder open in Windows File Explorer, change the folder path to `powershell` and press `Enter`:
![Open PowerShell from File Explorer](<images/powershell File Explorer.jpg>) or
- Make the keyboard shortcut `Windows+X` and select open PowerShell from the menu that appears, then, use the `cd` command to navigate to the desired folder:
![PowerShell cd command](<images/PowerShell cd command.jpg>)

## Generating executable again
You may want to regenerate the `dist\Executable\OneHandTyper.exe` executable if it is not working or if you modify the program in the `src` folder and want the changes to be applied to the executable.

To be able to generate the executable again, you must have already performed the steps in the `Advanced Execution` section above.

1. Open the Windows console (`Windows+R`, type `cmd` and press `Enter`), use the `cd` command to navigate to the program folder (the one that contains the `src` folder and the `README.md` file, and which you may have renamed to `OneHandTyper` as suggested), making a command like `cd "path/to/OneHandTyper"` (note that the path is written in quotes);
![cd command](<images/cd command.jpg>)

2. Now you need to run a command that **activates** the virtual environment in the console. The exact command to activate the virtual environment depends on your operating system and which console you are using. When you successfully activate the virtual environment, you will see `(.venv)` (note that it is written in parentheses) appear before the program path in the console. Try the following commands to activate the virtual environment:
    - `.venv\Scripts\activate.bat` (cmd.exe in Windows);
    - `.venv\bin\activate.bat` (Linux);
    - `.venv\Scripts\Activate.ps1` (PowerShell in Windows);
    - `.venv\bin\Activate.ps1`;
    - `source .venv\Scripts\activate` or `source .venv\bin\activate` (Git Bash / Linux / Mac);
![Command to activate virtual environment](<images/activate virtual environment.jpg>)

3. To generate the executable again, you will need to run the file `utilities\compile_executable.py`. You can run this file via the command `.venv\Scripts\python.exe utilities\compile_executable.py`;
![Command to compile executable](<images/run compile_executable.jpg>)
    - If the message `WARNING: The output directory "...\dist\Executable" and ALL ITS CONTENTS will be REMOVED! Continue? (y/N)` appears while you are running the command, you will need to type `y` and press `Enter` to continue. But keep in mind that the files `dist\Executable\_internal\dictionaries.py` and `dist\Executable\_internal\keyboard_layout.py` will be deleted, so it might be a good idea to back them up before continuing.


## Help and Documentation
Please see the issues in this project for help, create a new issue if necessary. You can help by answering other users' questions.

This project does not have good documentation yet. See the file `reqs and tasks.txt` to get an idea of ​​the functionality of this program.

### Basic usage
This program adds an icon to your system tray. You can right-click on this icon to see more options, or double-click on it to trigger the first option. This program also displays widgets on the screen, which you can resize and reposition.

One of the widgets shows the name of the currently active dictionary. This widget is displayed all the time while the program is not sleeping.

Another widget shows the keys that the program is holding down for you: you can make the program hold keys for you, such as the `ctrl` key, the `alt` key, the `shift` key, etc., by simply performing the keyboard chord of the corresponding `Hold` action. For example, if you trigger the `Hold('tab', 'ctrl')` action (the program holds `ctrl` when `tab` is pressed) once, the program will hold the `ctrl` key until the next key is pressed, but if you trigger this action twice (such as pressing `tab` twice in a row) the program will hold the `ctrl` key until you trigger the action a third time. This works especially well for holding `shift` (`Hold('caps lock', 'shift')`) since pressing `caps lock` once only capitalizes the next letter, while pressing `caps lock` twice in a row causes the shift key to be held, capitalizing everything that follows.

> Tip: You can use the `ToggleActiveChordDictWindow` chord defined in the `dictionaries.py` file (by default `a+d+f`) to show or hide the window that shows the chords you can make for the currently active dictionary and what each of them does. So, just try pressing the `a+d+f` keys at the same time!

### Adjusting and configuring the program
The files `dictionaries.py` and `keyboard_layout.py` are intended to be user-changeable. I recommend using `VSCode` to edit them and also to back them up, as changing them may cause the program to stop working and you may need to restore them to the previous version. Advanced users can clone the project using `GIT` and use it to version these files.
- If you are running the program through the `OneHandTyper.exe` executable, the files to edit are `dist\Executable\_internal\dictionaries.py` and `dist\Executable\_internal\keyboard_layout.py`, as these are the files that the executable loads. But if you are running the program through the command line with `.venv\Scripts\python.exe src\main.py`, the `OneHandTyper.bat` file, the `OneHandTyper.vbs` file, or through `VSCode`, the files to edit are `src\dictionaries.py` and `src\keyboard_layout.py`;
- Note: When you regenerate the executable, the `dist\Executable\_internal\dictionaries.py` and `dist\Executable\_internal\keyboard_layout.py` files are replaced with copies of the `src\dictionaries.py` and `src\keyboard_layout.py` files.
> Tip: After editing one of these files and saving it, you can make the keyboard chord to `Restart` the program so that these changes take effect.

#### dictionaries.py
The `dictionaries.py` file allows you to define multiple dictionaries (`ChordDict`) and switch between them using chords (`ActivateChordDict`). You can define chords to call Python functions (`FunctionCall`), to hold down keys (`Hold`), to end the program (`Quit`), to restart it (`Restart`), to write texts (`Write`), to press and release keys (`Tap`), etc.

Each Dictionary has the `mirrorChords` property, which you can set to `True` or `False`. When you set this property to `True`, for each chord in the dictionary a mirrored chord for the other hand can be automatically generated. For example, for `Hold('d+f+s', 'alt gr')` it can be automatically generated `Hold('k+j+l', 'alt gr')`.

How does the program know that the key that mirrors the `f` key is the `j` key? How does it know that the key that mirrors the `d` key is the `k` key? How does it know that the key that mirrors the `s` key is the `l` key? These correspondences are defined in the `MIRROR` property list: `MIRROR: List[Tuple[str, str]] = [ ... ('s', 'l'), ('d', 'k'), ('f', 'j'), ... ]`.

You can define a list of Keyboard Shortcuts to wake up the program when it is sleeping. Any of these Keyboard Shortcuts will make the program wake up. These Keyboard Shortcuts must be defined inside the `WAKE_UP_HOTKEYS` property.

> Tip: if you are having difficulty knowing what name the program gives to a particular physical key in order to use that name when defining a chord, or a target key or keyboard shortcut to be pressed by the program, open the `Show Pressed Keys Data` window and press and hold that key for a few seconds. Its name should appear both in that window and in a widget that displays the key's name in yellow letters. The name that appears in the widget can be used when defining a chord, while the name that appears in the `Show Pressed Keys Data` window can be used when defining a target key or keyboard shortcut for the program to press.

#### keyboard_layout.py
If the program is not recognizing your chords correctly, you may need to edit the `keyboard_layout.py` file to make it understand your keyboard layout.
- The program window called `Show Pressed Keys Data` can help you configure this file, as can the `utilities\utility_to_generate_key_aliases.py` file and the widget that appears when you hold down a key and shows the name of that key.
- When you press a physical key on your keyboard, the program receives an event, this event contains data describing the key pressed. However, the event data may be different depending on whether the modifiers (`ctrl`, `shift`, `caps lock`, `alt gr`, `num lock`, etc.) were active or not when the key was pressed. Open the `Show Pressed Keys Data` window and press the same physical key multiple times with different modifiers activated, to see how the received event data is different for each event depending on the active modifiers.
- Because the events for the same physical key can be different depending on which modifiers are active, this can confuse the program into thinking that different events correspond to different physical keys, when in reality they correspond to the same physical key. The `keyboard_layout.py` file allows you to solve this problem by telling the program which events (event data, called `KeyEventData`) correspond to a given physical key. Basically, you give a name to the physical key (you can make up a name for it, but I recommend using its main label as the name) and list which events (`KeyEventData`) correspond to that key (in other words, which events can be emitted when that key is pressed).
- The name you invent for the physical key is called the `user_key_representation`. In the `dictionaries.py` file, you must use exactly this name when defining a chord that contains that key. Example: `KeyAliases('MyEqualKey', [ KeyEventData(scan_code=13, name='=', is_keypad=False), KeyEventData(scan_code=13, name='+', is_keypad=False), KeyEventData(scan_code=13, name='§', is_keypad=False) ])` -> `Tap('MyEqualKey+p', 'delete')` (press `=+p` to trigger `Delete`), but you can still set the target key or shortcut to be triggered as `Tap('a+b', '=')` normally (press `a+b` to trigger `=`);

### Maintenance of this repository
If you want to maintain this project in your own repository, please fork this project to your repository and please create an issue here with the link to your repository.

This project may no longer be maintained when you find it, so look for an issue where someone says they are maintaining a version of this project in their own repository.

## Known compatibility:
- Windows 10
- Python v3.12.5
- Python Modules:
    - [infi.systray](https://github.com/Infinidat/infi.systray) v0.1.12
    - [keyboard](https://github.com/boppreh/keyboard) v0.13.5 
    - [pyinstaller](https://pypi.org/project/pyinstaller/) v6.10.0

### License: MIT

God bless you.