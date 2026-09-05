@echo off
title NV001 Launcher
color 0a
:menu
cls
echo ==============================================
echo             NV001 INTELLIGENCE
echo ==============================================
echo.
echo Please select a startup mode:
echo.
echo [1] Web Dashboard (Advanced UI)
echo [2] Desktop GUI (Tkinter)
echo [3] Terminal (CLI Mode)
echo [4] Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto web
if "%choice%"=="2" goto gui
if "%choice%"=="3" goto terminal
if "%choice%"=="4" goto exit

goto menu

:web
cls
echo Starting NV001 in Web Dashboard mode...
echo (Opening http://127.0.0.1:8000 in your browser)
start http://127.0.0.1:8000
.\.venv\Scripts\python.exe -m app.main --web
pause
goto menu

:gui
cls
echo Starting NV001 in Desktop GUI mode...
.\.venv\Scripts\python.exe -m app.main --gui
pause
goto menu

:terminal
cls
echo Starting NV001 in Terminal mode...
.\.venv\Scripts\python.exe -m app.main
pause
goto menu

:exit
exit
