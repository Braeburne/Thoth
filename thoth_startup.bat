@echo off
echo Starting Thoth script...

REM Navigate to the directory where Thoth.py is located
cd "C:\Users\ezbra\Documents\GitHub\Thoth"
echo Current directory: %cd%

REM Execute Thoth.py using Python within Windows Terminal
wt --profile "Command Prompt" -d "C:\Users\ezbra\Documents\GitHub\Thoth" python Thoth.py
echo Thoth.py executed.

REM Close the batch script window
exit

REM Optional: Pause to view any output/errors before closing
REM pause