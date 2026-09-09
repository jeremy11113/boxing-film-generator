@echo off
REM Windows batch file to run Boxing Film Generator easily

echo.
echo ========================================
echo   Boxing Film Generator - Windows Start
echo ========================================
echo.

REM Check if venv exists
if not exist venv (
    echo Creating Python virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Check if .env exists
if not exist .env (
    echo.
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and add your API keys.
    echo.
    pause
    exit /b 1
)

REM Show available styles
echo Available visual styles:
echo   - stylized_sexy
echo   - cinematic_glamorous
echo   - athletic_professional
echo   - moody_intense
echo   - intimate_close
echo   - bright_showcase
echo.

REM Get user input
set /p prompt="Enter your film prompt: "
set /p style="Enter visual style (default: stylized_sexy): "

if "%style%"=="" set style=stylized_sexy

echo.
echo Generating film...
echo.

REM Run the generator
python src/main.py -p "%prompt%" -s %style%

echo.
echo Generation complete! Check the 'output' folder for results.
echo.
pause
