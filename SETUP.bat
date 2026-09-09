@echo off
REM ============================================
REM Boxing Film Generator - Quick Setup
REM ============================================
REM This script sets everything up for you
REM Just double-click and wait!

CLS
echo.
echo ============================================
echo   BOXING FILM GENERATOR - SETUP
echo ============================================
echo.
echo This will set up the app on your computer.
echo (This only needs to run once)
echo.

REM Check Python
echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python not found!
    echo.
    echo Please install Python first:
    echo 1. Go to https://www.python.org/downloads
    echo 2. Download Python 3.11 or newer
    echo 3. IMPORTANT: Check "Add Python to PATH"
    echo 4. Click Install
    echo 5. Run this file again
    echo.
    pause
    exit /b 1
)

echo OK - Python found
echo.

REM Create virtual environment
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating...
call venv\Scripts\activate.bat

echo Installing packages...
pip install -r requirements.txt >nul 2>&1

if errorlevel 1 (
    echo ERROR during installation
    pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo ============================================
echo   SETUP COMPLETE!
echo ============================================
echo.
echo Next steps:
echo 1. Open the .env file (in this folder)
echo 2. Paste your OpenAI API key
echo 3. Save the file
echo 4. Run 'Start App.bat'
echo.
echo Get free API key:
echo https://platform.openai.com/api-keys
echo.
pause
