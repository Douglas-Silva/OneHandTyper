' Create an instance of the WScript.Shell object, which provides access to the Windows shell
Set WshShell = CreateObject("WScript.Shell")

' Run the batch file "OneHandTyper.bat" with hidden window
' chr(34) is used to add double quotes around the file path to handle any spaces in the path
' The second parameter (0) specifies that the window should be hidden
WshShell.Run chr(34) & ".\OneHandTyper.bat" & chr(34), 0

' Release the WshShell object, freeing up system resources
Set WshShell = Nothing
