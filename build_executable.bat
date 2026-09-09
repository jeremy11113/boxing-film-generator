# Build standalone executable for Boxing Film Generator
# Run this script to create a Windows .exe file

echo off
CLS
echo.
echo ========================================
echo   Boxing Film Generator - Build Wizard
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python and try again.
    pause
    exit /b 1
)

echo Checking for PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

echo.
echo Building executable...
echo This may take 2-3 minutes...
echo.

REM Build the executable
pyinstaller --onefile --windowed --name "BoxingFilmGenerator" --icon icon.ico gui_launcher.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   BUILD COMPLETE!
echo ========================================
echo.
echo Your executable is ready:
echo   dist\BoxingFilmGenerator.exe
echo.
echo You can now:
echo   1. Move BoxingFilmGenerator.exe to your Desktop
echo   2. Double-click to run (no Python needed!)
echo   3. Share with others
echo.
pause
