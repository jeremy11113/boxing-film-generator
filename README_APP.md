# Boxing Film Generator - Windows App

## Quick Start (3 steps)

### Step 1: Setup
Double-click: **SETUP.bat**
- Wait for it to finish (2-3 minutes)
- You'll see "SETUP COMPLETE!"

### Step 2: Add Your API Key
1. Open **.env** file (in this folder)
2. Find the line: `OPENAI_API_KEY=`
3. Go to https://platform.openai.com/api-keys
4. Copy your key
5. Paste it after the `=` (no quotes needed)
6. Save the file

Example:
```
OPENAI_API_KEY=sk-proj-abc123xyz...
```

### Step 3: Run App
Double-click: **Start App.bat**
- App opens in a new window
- Type your film idea
- Pick the look you want
- Click **GENERATE FILM**

## What You Get

After generation, you'll have:
- `screenplay.md` - Your full story
- `characters.json` - Character details
- `scenes.json` - Scene breakdown
- `video_prompts.json` - For making actual videos

## Making Videos

After you have the prompts:

1. Go to https://runwayml.com/
2. Sign up (free)
3. Create new "Gen-3 Text to Video" project
4. Copy a prompt from `video_prompts.json`
5. Paste into Runway
6. Click "Generate"
7. Download your video!

## Troubleshooting

**"Python not found"**
- Install from https://python.org/downloads
- Run SETUP.bat again

**"API Key error"**
- Open .env file
- Make sure your key is there
- No spaces or quotes
- Save and restart

**App won't start**
- Run SETUP.bat again
- Make sure .env has your API key

## That's It!

You're all set. Just:
1. **SETUP.bat** (once)
2. **Start App.bat** (every time)
3. Enter your story
4. Click **GENERATE FILM**

Enjoy! 🎬🥊
