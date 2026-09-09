import openai
from typing import Dict, List, Optional
from src.prompts.system_prompts import get_boxing_film_prompt
from src.visual_style import get_visual_style_prompt, VISUAL_STYLE_PRESETS
from config.settings import settings

class ScreenplayGenerator:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
    
    def generate_screenplay(self, prompt: str, visual_style: str = "cinematic_glamorous") -> Dict[str, str]:
        """
        Generate a full screenplay from a single prompt with visual style integration.
        Returns dict with screenplay and visual direction.
        """
        system_prompt = get_boxing_film_prompt(prompt)
        visual_style_prompt = get_visual_style_prompt(visual_style)
        
        # Combine prompts for better visual consistency
        combined_system_prompt = f"""{system_prompt}

VISUAL STYLE GUIDANCE:
{visual_style_prompt}

Incorporate this visual style direction into your screenplay descriptions, 
action lines, and scene directions to ensure the screenplay is written 
with these cinematographic elements in mind.
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": combined_system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=4000,
        )
        
        screenplay_text = response.choices[0].message.content
        
        return {
            "screenplay": screenplay_text,
            "visual_style": visual_style,
            "style_preset": VISUAL_STYLE_PRESETS.get(visual_style).name if visual_style in VISUAL_STYLE_PRESETS else "Custom",
            "visual_direction": visual_style_prompt
        }
    
    def refine_screenplay(self, screenplay: str, feedback: str, visual_style: str = "cinematic_glamorous") -> str:
        """
        Refine screenplay based on user feedback while maintaining visual style.
        """
        visual_style_prompt = get_visual_style_prompt(visual_style)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": f"""You are an expert screenwriter specializing in women's boxing films.
Refine and improve the given screenplay based on feedback while maintaining this visual style:

{visual_style_prompt}

Ensure all refinements maintain the visual aesthetic and cinematographic direction."""
                },
                {
                    "role": "user",
                    "content": f"Original Screenplay:\n{screenplay}\n\nFeedback:\n{feedback}"
                }
            ],
            temperature=0.7,
            max_tokens=4000,
        )
        
        return response.choices[0].message.content
    
    def get_available_styles(self) -> Dict[str, str]:
        """
        Return available visual style presets and their descriptions.
        """
        return {
            name: preset.description 
            for name, preset in VISUAL_STYLE_PRESETS.items()
        }
