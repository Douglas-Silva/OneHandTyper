@echo off
REM The `@echo off` command turns off the display of the command itself in the command prompt.
REM It makes the script output cleaner by not showing the commands being executed.

REM The command below starts PowerShell.
REM Add -NoExit if you want to keep the PowerShell window open after the script finishes executing.
REM Example: `powershell.exe -NoExit -Command "& {cd '%~dp0'; .\.venv\Scripts\Activate.ps1; .\.venv\Scripts\python.exe src\main.py}"`.
REM -Command specifies that the following string is a command to be executed by PowerShell.

REM `cd '%~dp0';` changes the directory to the location of the batch file.
REM %~dp0 is a batch parameter that expands to the drive and path of the script, ensuring that the subsequent commands run in the correct directory.

REM `.\.venv\Scripts\Activate.ps1;` activates the Python virtual environment.
REM It runs the PowerShell script to activate the virtual environment located in the .venv folder.

REM `.\.venv\Scripts\python.exe src\main.py` runs the Python script.
REM It executes the Python script located at `src/main.py` using the Python interpreter from the virtual environment.
REM The Python interpreter from the virtual environment is located at `.\.venv\Scripts\python.exe`.

powershell.exe -NoExit -Command "& {cd '%~dp0'; .\.venv\Scripts\Activate.ps1; .\.venv\Scripts\python.exe src\main.py}"