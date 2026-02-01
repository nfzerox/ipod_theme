@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

REM Create list of language folders
set /a count=0
for /d %%L in ("Languages\SilverDB.*.LE") do (
    set /a count+=1
    set "lang[!count!]=%%~nxL"
)

REM Display menu
echo Select languages for packaging:
for /L %%i in (1,1,!count!) do (
    echo   %%i^) !lang[%%i]!
)

set /a all_index=!count! + 1
echo   !all_index!^) All languages

REM Get user input
set /p selection="Enter numbers separated by spaces: "

REM Check if "all" selected
echo %selection% | findstr /C:"!all_index!" >nul
if not errorlevel 1 (
    echo Packaging all languages...
    for /L %%i in (1,1,!count!) do (
        echo Packaging !lang[%%i]!...
        "silverutil\target\release\silverutil.exe" create "Languages\!lang[%%i]!" "Languages\!lang[%%i]!.bin2"
    )
    pause
    exit /b 0
)

REM Process individual selections
for %%n in (%selection%) do (
    if %%n LEQ !count! if %%n GEQ 1 (
        echo Packaging !lang[%%n]!...
        "silverutil\target\release\silverutil.exe" create "Languages\!lang[%%n]!" "Languages\!lang[%%n]!.bin2"
    )
)
pause