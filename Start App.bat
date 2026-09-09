@echo off
REM ============================================
REM Boxing Film Generator - Start App
REM ============================================
REM This runs your boxing film generator app

CLS

REM Check if setup was done
if not exist venv (
    echo ERROR: Setup not complete!
    echo.
    echo Please run SETUP.bat first
    echo.
    pause
    exit /b 1
)

REM Activate and run
call venv\Scripts\activate.bat
python gui_launcher.py
