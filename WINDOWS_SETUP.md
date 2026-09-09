# Windows Setup Guide - Boxing Film Generator

## Prerequisites

Before you start, make sure you have:
- Windows 10 or Windows 11
- At least 4GB RAM (8GB+ recommended)
- Python 3.10 or newer
- Git installed

## Step 1: Install Python

1. Download Python from https://www.python.org/downloads/
2. Click on "Download Python 3.11" (or latest 3.x version)
3. **IMPORTANT**: Check the box "Add Python to PATH" during installation
4. Click "Install Now"
5. Wait for installation to complete

### Verify Python Installation:

Open Command Prompt (press `Win + R`, type `cmd`, press Enter):

```bash
python --version
pip --version
```

You should see version numbers printed (e.g., "Python 3.11.0").

## Step 2: Install Git

1. Download from https://git-scm.com/download/win
2. Run the installer
3. Click "Next" through the installation (defaults are fine)
4. Finish installation

## Step 3: Clone the Repository

Open Command Prompt and run:

```bash
git clone https://github.com/jeremy11113/boxing-film-generator.git
cd boxing-film-generator
```

## Step 4: Create Python Virtual Environment

A virtual environment keeps dependencies isolated. In Command Prompt:

```bash
python -m venv venv
```

This creates a `venv` folder in your project.

## Step 5: Activate Virtual Environment

**On Windows Command Prompt:**
```bash
venv\Scripts\activate
```

**On Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

You should see `(venv)` appear at the start of your command line.

## Step 6: Install Dependencies

With the virtual environment active, run:

```bash
pip install -r requirements.txt
```

This will take 2-5 minutes depending on your internet speed.

## Step 7: Set Up Environment Variables

1. Copy the example file:
```bash
copy .env.example .env
```

2. Open `.env` in Notepad or your favorite text editor

3. Add your API keys:
   - Get OpenAI key from: https://platform.openai.com/api-keys
   - Get Runway key from: https://www.runwayml.com/

4. Save the file

### Example .env file:
```
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4
RUNWAY_API_KEY=your-runway-key-here
OUTPUT_DIR=./output
VIDEO_QUALITY=high
```

## Step 8: Create Output Directory

The generator will create this automatically, but you can pre-create it:

```bash
mkdir output
```

## Step 9: Test Installation

Run this command to verify everything works:

```bash
python -c "import openai; print('✅ OpenAI installed'); from config.settings import settings; print('✅ Config loaded')"
```

You should see checkmarks if everything is set up correctly.

## Step 10: Generate Your First Film

Now you're ready! Run:

```bash
python src/main.py -p "Two female boxers in an intense championship match" -s stylized_sexy
```

### Command Explanation:
- `-p` = your prompt/story idea
- `-s` = visual style (stylized_sexy, cinematic_glamorous, etc.)

### Available Styles:
- `stylized_sexy` - Dramatic lighting, strategic framing
- `cinematic_glamorous` - Golden hour, warm tones
- `athletic_professional` - Professional arena lighting
- `moody_intense` - Dark, dramatic atmosphere
- `intimate_close` - Warm, flattering close-ups
- `bright_showcase` - Well-lit athletic form

## Output Files

After running, check the `output` folder for:

- `screenplay.md` - Full screenplay
- `characters.json` - Character profiles
- `scenes.json` - Scene breakdown
- `video_prompts.json` - **Use these with Runway ML** ⭐

## Troubleshooting

### "python is not recognized"
- Python wasn't added to PATH. Reinstall Python and **check "Add Python to PATH"**
- Or use: `python.exe` full path
- Restart Command Prompt after Python installation

### "venv\\Scripts\\activate" doesn't work
- Try: `venv\Scripts\activate.bat`
- Or in PowerShell: `.\venv\Scripts\Activate.ps1`

### "ModuleNotFoundError: No module named 'openai'"
- Virtual environment not activated (should see `(venv)` in command line)
- Run: `pip install -r requirements.txt` again

### Permission Denied Error
- Close any antivirus software temporarily
- Run Command Prompt as Administrator (right-click → Run as administrator)

### "OpenAI API key not found"
- Check `.env` file exists in project root
- Verify `OPENAI_API_KEY=sk-...` is set correctly
- No spaces around the `=` sign

## Using Generated Prompts with Runway ML

1. Go to https://runwayml.com/
2. Sign in with your account
3. Click "Create New Project" → "Gen-3 Text to Video"
4. Copy a prompt from `video_prompts.json`
5. Paste into Runway's text prompt box
6. Adjust duration (typically 4-8 seconds)
7. Click "Generate"
8. Download the video

## Next Steps

1. **Experiment with prompts** - Try different story ideas
2. **Test different visual styles** - Each creates a different aesthetic
3. **Generate videos on Runway** - Use the video_prompts.json
4. **Combine videos** - Use Windows Video Editor or DaVinci Resolve to stitch scenes together

## Resources

- OpenAI Documentation: https://platform.openai.com/docs
- Runway ML: https://www.runwayml.com/
- Python Virtual Environments: https://docs.python.org/3/tutorial/venv.html

## Getting Help

- Check GitHub Issues: https://github.com/jeremy11113/boxing-film-generator/issues
- Review error messages carefully - they often indicate the exact problem
- Make sure all API keys are correct (copy-paste to avoid typos)

---

**You're all set! Start creating amazing boxing films! 🎬🥊**
