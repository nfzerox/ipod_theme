@echo off
setlocal enabledelayedexpansion

REM Go to the script directory
cd /d "%~dp0"
cd silverutil
cargo build --release
cd ..

REM Define languages as an array using set
set LANG[1]=ar_SA
set LANG[2]=ca_ES
set LANG[3]=cs_CZ
set LANG[4]=da_DK
set LANG[5]=de_DE
set LANG[6]=el_GR
set LANG[7]=en_GB
set LANG[8]=es_ES
set LANG[9]=fi_FI
set LANG[10]=fr_FR
set LANG[11]=he_IL
set LANG[12]=hr_HR
set LANG[13]=hu_HU
set LANG[14]=id_ID
set LANG[15]=it_IT
set LANG[16]=ja_JP
set LANG[17]=ko_KR
set LANG[18]=ms_MY
set LANG[19]=nl_NL
set LANG[20]=no_NO
set LANG[21]=pl_PL
set LANG[22]=pt_BR
set LANG[23]=pt_PT
set LANG[24]=ro_RO
set LANG[25]=ru_RU
set LANG[26]=sk_SK
set LANG[27]=sv_SE
set LANG[28]=th_TH
set LANG[29]=tr_TR
set LANG[30]=uk_UA
set LANG[31]=vi_VN
set LANG[32]=zh_CN
set LANG[33]=zh_HK
set LANG[34]=zh_TW

set LANG_COUNT=34

REM Display menu
echo Select languages to unpack:
for /L %%i in (1,1,%LANG_COUNT%) do (
    echo   %%i^) !LANG[%%i]!
)

set /a ALL_INDEX=%LANG_COUNT% + 1
echo   %ALL_INDEX%^) All languages

REM Get user input
set /p SELECTION="Enter numbers separated by spaces: "

REM Check if "All" was selected
for %%n in (%SELECTION%) do (
    if %%n == %ALL_INDEX% (
        echo Unpacking all languages...
        for /L %%i in (1,1,%LANG_COUNT%) do (
            echo Unpacking !LANG[%%i]!...
            "silverutil\target\release\silverutil.exe" extract "Languages\SilverDB.!LANG[%%i]!.LE.bin" "Languages\SilverDB.!LANG[%%i]!.LE"
        )
        pause
        exit /b 0
    )
)

REM Extract selected languages
for %%n in (%SELECTION%) do (
    if %%n LEQ %LANG_COUNT% if %%n GEQ 1 (
        set LANG_INDEX=%%n
        echo Unpacking !LANG[%LANG_INDEX%]!...
        "silverutil\target\release\silverutil.exe" extract "Languages\SilverDB.!LANG[%LANG_INDEX%]!.LE.bin" "Languages\SilverDB.!LANG[%LANG_INDEX%]!.LE"
    )
)
pause