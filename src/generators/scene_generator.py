import openai
import json
from typing import Dict, List, Optional
from config.settings import settings
from src.prompts.system_prompts import SCENE_BREAKDOWN_PROMPT
from src.visual_style import get_visual_style_prompt, get_character_visual_description, VISUAL_STYLE_PRESETS

class SceneGenerator:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
    
    def breakdown_scenes(self, screenplay: str, visual_style: str = "cinematic_glamorous") -> List[Dict]:
        """
        Break down screenplay into individual scenes with visual descriptions and style integration.
        """
        visual_style_prompt = get_visual_style_prompt(visual_style)
        
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

INCORPORATE THIS VISUAL STYLE INTO ALL SCENE DESCRIPTIONS:
{visual_style_prompt}

Screenplay:
{screenplay}

Format as JSON array of scene objects.
Ensure video generation prompts include detailed visual direction based on the specified style.
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
                scenes = json.loads(json_str)
                
                # Add visual style metadata to each scene
                for scene in scenes:
                    scene['visual_style'] = visual_style
                    scene['style_preset'] = VISUAL_STYLE_PRESETS.get(visual_style).name if visual_style in VISUAL_STYLE_PRESETS else "Custom"
                
                return scenes
        except json.JSONDecodeError:
            pass
        
        return []
    
    def enhance_scene_video_prompt(self, scene: Dict, visual_style: str = "cinematic_glamorous", character_data: Optional[Dict] = None) -> str:
        """
        Create an enhanced video generation prompt with full visual style details.
        """
        visual_style_prompt = get_visual_style_prompt(visual_style)
        
        base_prompt = scene.get('video_generation_prompt', scene.get('description', ''))
        
        character_section = ""
        if character_data:
            character_section = f"\n\nCHARACTER VISUAL DETAILS:\n{get_character_visual_description(character_data, visual_style)}"
        
        enhanced_prompt = f"""
SCENE VIDEO GENERATION PROMPT:

{base_prompt}

APPLY THIS VISUAL STYLE:
{visual_style_prompt}

SCENE SPECIFICS:
- Location: {scene.get('location', 'Arena')}
- Time: {scene.get('time_of_day', 'Day')}
- Atmosphere: {scene.get('atmosphere', 'Professional')}
- Camera Angles: {', '.join(scene.get('camera_angles', ['Dynamic']))}
- Sound Design: {scene.get('sound_design', 'Professional arena audio')}{character_section}

CREATE A VIDEO THAT:
1. Matches the visual style precisely
2. Showcases athletic excellence and confidence
3. Uses sophisticated cinematography
4. Maintains professional and tasteful presentation
5. Emphasizes movement, power, and visual appeal
6. Incorporates the specified lighting, color grading, and framing
"""
        
        return enhanced_prompt
    
    def get_available_styles(self) -> Dict[str, str]:
        """
        Return available visual style presets.
        """
        return {
            name: preset.description 
            for name, preset in VISUAL_STYLE_PRESETS.items()
        }
