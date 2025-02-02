@echo off
setlocal enabledelayedexpansion

:: Create the duplicatePics folder if it doesn't exist
if not exist "duplicatePics" mkdir "duplicatePics"

:: Loop through files that have (1) or (2) in their name
for %%F in (*"(1)"* *"(2)"*) do (
    set "filename=%%~nF"
    
    :: Remove the (1) or (2) part from the filename
    set "basefilename=!filename:(1)=!"
    set "basefilename=!basefilename:(2)=!"
    
    echo Searching for duplicates of "!basefilename!*"
    
    :: Move all matching files to duplicatePics
    for %%D in ("!basefilename!*") do (
        move "%%D" "duplicatePics\"
    )
)

echo Done!
pause