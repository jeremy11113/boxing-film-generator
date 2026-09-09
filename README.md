# AI Women's Boxing Film Generator

An AI-powered screenplay and video generator that creates women's boxing films from a single prompt. Generates high-quality video content similar to Higgsfield's style.

## Features

- **Single Prompt Generation**: Input one prompt and generate full screenplay
- **AI Screenplay Writing**: Uses LLM to create dialogue, scenes, and narrative
- **Video Generation**: Creates visual scenes using text-to-video AI
- **Character Development**: Auto-generates boxer profiles and backstories
- **Scene Composition**: Intelligent scene breakdown and composition

## Tech Stack

- **LLM**: OpenAI GPT-4 or Claude for screenplay generation
- **Video Generation**: Runway ML, Pika Labs, or similar for video creation
- **Backend**: Python with FastAPI
- **Frontend**: React (optional for UI)

## Project Structure

```
boxing-film-generator/
├── src/
│   ├── generators/
│   │   ├── screenplay_generator.py
│   │   ├── character_generator.py
│   │   └── scene_generator.py
│   ├── video/
│   │   ├── video_composer.py
│   │   └── video_api_client.py
│   ├── prompts/
│   │   └── system_prompts.py
│   └── main.py
├── config/
│   └── settings.py
├── tests/
├── requirements.txt
└── .env.example
```

## Quick Start

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables (API keys)
4. Run: `python src/main.py --prompt "your boxing film prompt"`

## Usage

```bash
python src/main.py --prompt "A young female boxer from the streets fights her way to the championship"
```

Output:
- screenplay.md
- scene_breakdown.json
- character_profiles.json
- video_frames/

## API Keys Required

- OpenAI API key
- Runway ML API key (or alternative video generation API)

## License

MIT
