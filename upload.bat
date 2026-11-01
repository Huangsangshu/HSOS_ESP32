@echo off
setlocal

REM ==================================================
REM  HSOS_ESP32S3 upload script (ampy) - continuous
REM  Usage : upload.bat [COMx]   (default: COM9)
REM  Note  : close serial monitor (putty) before run
REM
REM  Watchdog was REMOVED from the firmware code, so
REM  uploads can run back-to-back safely:
REM    put all files (no reset between), then reset
REM  once at the end to boot the new code.
REM ==================================================

set PORT=%~1
if "%PORT%"=="" set PORT=COM9
set BAUD=115200
set SRC=%~dp0

echo.
echo Target port : %PORT%
echo Baud rate   : %BAUD%
echo Source dir  : %SRC%
echo Upload mode : continuous (put all, reset once)
echo.

REM ---- check ampy ----
where ampy >nul 2>nul
if errorlevel 1 (
    echo [ERROR] ampy not found!
    echo         install with:  pip install adafruit-ampy
    pause
    exit /b 1
)

REM ---- check key local files ----
if not exist "%SRC%main.py" (
    echo [ERROR] main.py not found. Run script from project root.
    pause
    exit /b 1
)
if not exist "%SRC%screens\timeset.py" (
    echo [ERROR] screens\timeset.py not found.
    pause
    exit /b 1
)
if not exist "%SRC%HSUIFONT48.bin" (
    echo [ERROR] HSUIFONT48.bin not found.
    pause
    exit /b 1
)

REM ---- cleanup old single-file screens ----
echo [0/18] Clean old files ...
ampy --port %PORT% --baud %BAUD% rm /screens.py 2>nul
if errorlevel 1 echo [WARN] rm /screens.py failed (already removed?)
ampy --port %PORT% --baud %BAUD% rm /timeedit.py 2>nul
if errorlevel 1 echo [WARN] rm /timeedit.py failed (already removed?)
ampy --port %PORT% --baud %BAUD% mkdir /screens 2>nul
if errorlevel 1 echo [WARN] mkdir /screens failed (already exists?)

REM ---- upload all files (no reset between) ----
echo [1/18] main.py
ampy --port %PORT% --baud %BAUD% put "%SRC%main.py" /main.py || goto :error

echo [2/18] app.py
ampy --port %PORT% --baud %BAUD% put "%SRC%app.py" /app.py || goto :error

echo [3/18] hardware.py
ampy --port %PORT% --baud %BAUD% put "%SRC%hardware.py" /hardware.py || goto :error

echo [4/18] state.py
ampy --port %PORT% --baud %BAUD% put "%SRC%state.py" /state.py || goto :error

echo [5/18] system.py
ampy --port %PORT% --baud %BAUD% put "%SRC%system.py" /system.py || goto :error

echo [6/18] sdcard.py
ampy --port %PORT% --baud %BAUD% put "%SRC%sdcard.py" /sdcard.py || goto :error

echo [7/18] timeutil.py
ampy --port %PORT% --baud %BAUD% put "%SRC%timeutil.py" /timeutil.py || goto :error

echo [8/18] ui.py
ampy --port %PORT% --baud %BAUD% put "%SRC%ui.py" /ui.py || goto :error

echo [9/18] screens\__init__.py
ampy --port %PORT% --baud %BAUD% put "%SRC%screens\__init__.py" /screens/__init__.py || goto :error

echo [10/18] screens\mainscreen.py
ampy --port %PORT% --baud %BAUD% put "%SRC%screens\mainscreen.py" /screens/mainscreen.py || goto :error

echo [11/18] screens\mainmenu.py
ampy --port %PORT% --baud %BAUD% put "%SRC%screens\mainmenu.py" /screens/mainmenu.py || goto :error

echo [12/18] screens\setting.py
ampy --port %PORT% --baud %BAUD% put "%SRC%screens\setting.py" /screens/setting.py || goto :error

echo [13/18] screens\calendar.py
ampy --port %PORT% --baud %BAUD% put "%SRC%screens\calendar.py" /screens/calendar.py || goto :error

echo [14/18] screens\about.py
ampy --port %PORT% --baud %BAUD% put "%SRC%screens\about.py" /screens/about.py || goto :error

echo [15/18] screens\power.py
ampy --port %PORT% --baud %BAUD% put "%SRC%screens\power.py" /screens/power.py || goto :error

echo [16/18] screens\timeset.py
ampy --port %PORT% --baud %BAUD% put "%SRC%screens\timeset.py" /screens/timeset.py || goto :error

echo [17/18] HSUIFONT14.bin
ampy --port %PORT% --baud %BAUD% put "%SRC%HSUIFONT14.bin" /HSUIFONT14.bin || goto :error

echo [18/18] HSUIFONT48.bin
ampy --port %PORT% --baud %BAUD% put "%SRC%HSUIFONT48.bin" /HSUIFONT48.bin || goto :error

echo.
echo [done] All files uploaded. Resetting board ...
ampy --port %PORT% --baud %BAUD% reset
%SystemRoot%\System32\ping.exe -n 11 127.0.0.1 >nul

echo.
echo ============================================
echo  Upload done! Files on board:
echo ============================================
ampy --port %PORT% --baud %BAUD% ls /
echo.
echo  /screens files on board:
ampy --port %PORT% --baud %BAUD% ls /screens

echo.
echo  Restarting board to run new code ...
ampy --port %PORT% --baud %BAUD% reset
%SystemRoot%\System32\ping.exe -n 9 127.0.0.1 >nul
pause
exit /b 0

:error
echo.
echo [ERROR] Upload failed! Check:
echo        1. COM port (see Device Manager)
echo        2. serial port in use by another app
echo        3. board connected and in MicroPython mode
echo.
echo  Files already uploaded are kept.
echo  Re-run this script to continue.
pause
exit /b 1
