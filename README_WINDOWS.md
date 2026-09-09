# 🎬 Boxing Film Generator - Windows Edition

Generate professional women's boxing films from a single AI prompt with visual style control.

## Quick Start (5 minutes)

### 1. Download & Extract
- Clone or download this repository
- Extract to a folder on your computer

### 2. Run Setup
Double-click: `setup.bat`

This will:
- ✅ Check Python installation
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Create `.env` file

### 3. Add API Keys
1. Open `.env` in Notepad
2. Get your OpenAI API key from: https://platform.openai.com/api-keys
3. Paste it next to `OPENAI_API_KEY=`
4. Save the file

### 4. Generate Your First Film
Double-click: `run_windows.bat`

Or in Command Prompt:
```bash
python src/main.py -p "Two female boxers fight for championship glory" -s stylized_sexy
```

## What You Get

After running, you'll get:

📄 **screenplay.md** - Full screenplay with visual direction  
👥 **characters.json** - Detailed character profiles  
🎬 **scenes.json** - Scene-by-scene breakdown  
🎥 **video_prompts.json** - Ready for Runway ML or Pika Labs  

## Visual Styles

Choose how your film looks:

| Style | Look | Best For |
|-------|------|----------|
| **stylized_sexy** | Dramatic lighting, bold makeup, strategic framing | High-impact visuals ⭐ |
| **cinematic_glamorous** | Golden hour, warm tones, intimate close-ups | Romantic/dramatic |
| **athletic_professional** | Arena lighting, full-body showcase | Sports focus |
| **moody_intense** | Dark lighting, high contrast | Psychological depth |
| **intimate_close** | Warm, flattering lighting | Personal connection |
| **bright_showcase** | Well-lit, vibrant colors | Dynamic energy |

## Usage Examples

```bash
# Sexy glamorous style
python src/main.py -p "Rival boxers in championship match" -s stylized_sexy

# Professional athletic style
python src/main.py -p "Underdog boxer rises to fame" -s athletic_professional

# Cinematic drama
python src/main.py -p "Two friends become fierce competitors" -s cinematic_glamorous
```

## Generate Videos on Runway ML

1. Go to https://runwayml.com/
2. Sign in or create account
3. New Project → Gen-3 Text to Video
4. Copy a prompt from `video_prompts.json`
5. Paste into Runway → Generate
6. Download video

## Troubleshooting

**"Python not found"**
- Install from python.org/downloads
- Restart your computer after installation
- Make sure "Add Python to PATH" is checked

**"Module not found" error**
- Double-check you activated virtual environment
- Look for `(venv)` at start of command line
- Run: `pip install -r requirements.txt` again

**"API key error"**
- Open `.env` in Notepad
- Check your API key is correct
- No spaces before/after the `=` sign
- Save and try again

**Videos won't generate**
- Make sure Runway API key is in `.env`
- Or manually use `video_prompts.json` on Runway website
- Videos still generate even without API key setup

See `WINDOWS_SETUP.md` for detailed troubleshooting.

## Project Structure

```
boxing-film-generator/
├── setup.bat              ← Run this first!
├── run_windows.bat        ← Run this to generate films
├── .env                   ← Add your API keys here
├── requirements.txt       ← Python dependencies
├── src/
│   ├── main.py           ← Main generator script
│   ├── visual_style.py   ← Visual style definitions
│   └── generators/       ← AI modules
├── config/
│   ��── settings.py       ← Configuration
└── output/               ← Generated films go here
```

## Next Steps

1. **Customize prompts** - Try different story ideas
2. **Experiment with styles** - See how different aesthetics look
3. **Generate on Runway** - Create actual videos
4. **Edit together** - Combine scenes in Windows Video Editor or DaVinci Resolve
5. **Share** - Upload to social media or streaming platforms

## Requirements

- Windows 10 or 11
- Python 3.10+ (download from python.org)
- 4GB+ RAM (8GB recommended)
- API keys for:
  - OpenAI (required) - https://platform.openai.com/
  - Runway ML (optional, for automatic video generation) - https://runwayml.com/

## Tips for Best Results

✨ **Story Tips:**
- Be specific about characters and settings
- Include emotional beats and conflicts
- Describe technical boxing sequences
- Set clear beginning, middle, end

✨ **Visual Tips:**
- Use `stylized_sexy` for maximum visual impact
- `cinematic_glamorous` for romantic/dramatic tone
- Mix different styles for different scenes
- Adjust camera directions in prompts

✨ **Video Tips:**
- Keep video prompts 100-200 words
- Specific details → better results
- Test different Runway generation settings
- Combine short clips in video editor

## Resources

- 📖 Full Setup Guide: `WINDOWS_SETUP.md`
- 🎥 Runway ML: https://runwayml.com/
- 🔑 OpenAI API: https://platform.openai.com/
- 🎬 Video Editor: https://www.davinciresolve.com/ (free)

## License

MIT - Use for personal projects

---

**Ready to create? Run `setup.bat` now! 🥊🎬**
