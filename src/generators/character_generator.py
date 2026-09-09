import openai
import json
from typing import Dict, List
from config.settings import settings
from src.prompts.system_prompts import CHARACTER_SYSTEM_PROMPT

class CharacterGenerator:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
    
    def generate_characters(self, screenplay: str, num_characters: int = 5) -> List[Dict]:
        """
        Extract and generate detailed character profiles from screenplay.
        """
        prompt = f"""
Based on this screenplay, create {num_characters} detailed character profiles for the main characters.

Screenplay excerpt:
{screenplay[:2000]}...

Generate detailed profiles in JSON format with fields:
- name
- age
- background
- personality_traits
- fighting_style
- appearance
- motivations
- fears
- character_arc
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": CHARACTER_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000,
        )
        
        try:
            # Extract JSON from response
            response_text = response.choices[0].message.content
            # Find JSON in response
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass
        
        return []
