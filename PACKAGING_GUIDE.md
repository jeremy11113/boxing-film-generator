# Windows Packaging Guide

## Two Ways to Package:

### Option 1: GUI Application (Recommended)

Create a beautiful Windows application with a graphical interface.

```bash
# 1. Install PyInstaller
pip install pyinstaller

# 2. Build the executable
python build_executable.bat

# Or manually:
pyinstaller --onefile --windowed --name "BoxingFilmGenerator" gui_launcher.py

# The .exe will be in: dist/BoxingFilmGenerator.exe
```

**Result:** A standalone .exe file that:
- ✅ Has a modern GUI interface
- ✅ Doesn't need Python installed
- ✅ Can be copied to any Windows computer
- ✅ Can be pinned to Start Menu or Desktop

### Option 2: Command Line Executable

For terminal/advanced users:

```bash
pyinstaller --onefile --console --name "boxing-generator" src/main.py
```

## Creating Desktop Shortcut

```bash
python create_shortcut.py
```

This creates a shortcut on your Desktop to run the app.

## Distribution

Once you have the .exe:

1. **Share the executable** - Just copy `BoxingFilmGenerator.exe` to others
2. **Create installer** - Use NSIS to create a proper installer
3. **Upload to GitHub Releases** - Release page for easy download

## Requirements for Users

Users running the .exe only need:
- Windows 10/11
- OpenAI API key (get free credits at platform.openai.com)
- Internet connection (for API calls)

They do NOT need:
- Python installed ✓
- Git ✓
- Command line knowledge ✓

## API Keys Setup for Users

1. Run BoxingFilmGenerator.exe
2. If API key missing, app will show error with instructions
3. User needs to:
   - Get free OpenAI API key from platform.openai.com/api-keys
   - Create `.env` file in same folder as exe
   - Add: `OPENAI_API_KEY=sk-...`
   - Restart app

## Next Steps

1. Run `build_executable.bat` to create the .exe
2. Test on your laptop
3. Share with others or upload to GitHub Releases

## Troubleshooting

**"PyInstaller not found"**
- Run: `pip install pyinstaller`

**"Icon not found"**
- You need icon.ico in project folder
- Remove `--icon icon.ico` from command if missing

**"App won't start"**
- Check if .env file exists in same folder as .exe
- Make sure OPENAI_API_KEY is set
- Run from Command Prompt to see error messages

## Making it Easier for Users

Create a simple README for distribution:

```
Boxing Film Generator - Windows Edition

1. Download BoxingFilmGenerator.exe
2. Download .env.example, rename to .env
3. Add your OpenAI API key to .env
4. Put .env in same folder as .exe
5. Double-click BoxingFilmGenerator.exe
6. Enter your prompt and click Generate!

Get free API key: https://platform.openai.com/api-keys
```
