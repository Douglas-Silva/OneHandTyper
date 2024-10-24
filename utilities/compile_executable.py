import PyInstaller.__main__
import os

# ! Run this file only when the virtual environment is active in the console.

# command in the console to run this file: 
# .venv\Scripts\python.exe utilities\compile_executable.py

# If the message below appears while you are running this file, you will need to type "y" and press "Enter" to continue. But keep in mind that the files "...\dist\Executable\_internal\dictionaries.py" and "...\dist\Executable\_internal\keyboard_layout.py" will be deleted, so it might be a good idea to back them up before continuing.
# WARNING: The output directory "...\dist\Executable" and ALL ITS CONTENTS will be REMOVED! Continue? (y/N)


PyInstaller.__main__.run([
    'src/main.py',
    # '--onefile',
    '--name', 'Executable',
    '--noconsole',
    '--add-data', 'src/dictionaries.py;.',
    '--add-data', 'src/keyboard_layout.py;.',
    '--hidden-import', 'pkg_resources',
    '--hidden-import', 'infi.systray',
    '--hidden-import', 'setuptools',
    '--hidden-import', '_socket',
    '--hidden-import', 'select',
    '--hidden-import', 'pyexpat',
    '--collect-submodules', 'xml.parsers.expat',
    '--hidden-import', 'xml.parsers.expat',
    '--collect-all', 'infi.systray',
    '--distpath', 'dist/'
])

# Rename the executable after generating it:
if os.path.exists('dist/Executable/Executable.exe'):
    os.rename('dist/Executable/Executable.exe', 'dist/Executable/OneHandTyper.exe')
