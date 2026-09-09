@echo off
REM Automated setup script for Windows

echo.
echo ========================================
echo   Boxing Film Generator - Setup Wizard
echo ========================================
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from python.org/downloads
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo ✓ Python found
echo.

REM Create virtual environment
echo Creating Python virtual environment...
if not exist venv (
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
echo This may take a few minutes...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo Make sure you have internet connection
    pause
    exit /b 1
)

echo.
echo ✓ Dependencies installed
echo.

REM Setup .env
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo ✓ .env file created
    echo.
    echo NEXT STEPS:
    echo 1. Open .env in Notepad
    echo 2. Add your OpenAI API key (get from platform.openai.com/api-keys)
    echo 3. Add your Runway API key (optional, for video generation)
    echo 4. Save the file
    echo.
    echo Then run: python src/main.py -p "Your prompt" -s stylized_sexy
) else (
    echo ✓ .env file already configured
)

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo To generate a film, use:
echo   python src/main.py -p "your prompt" -s stylized_sexy
echo.
echo Or run: run_windows.bat
echo.
pause
