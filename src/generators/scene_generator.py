import openai
import json
from typing import Dict, List
from config.settings import settings
from src.prompts.system_prompts import SCENE_BREAKDOWN_PROMPT

class SceneGenerator:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
    
    def breakdown_scenes(self, screenplay: str) -> List[Dict]:
        """
        Break down screenplay into individual scenes with visual descriptions.
        """
        prompt = f"""
Break down this screenplay into individual scenes. For each scene, provide:
- Scene number
- Title
- Location/Setting
- Time of day
- Visual atmosphere (mood, lighting, colors)
- Key actions/events
- Characters present
- Suggested camera angles
- Sound design notes
- Video generation prompt (description for AI video generation)

Screenplay:
{screenplay}

Format as JSON array of scene objects.
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": SCENE_BREAKDOWN_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=3000,
        )
        
        try:
            response_text = response.choices[0].message.content
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass
        
        return []
