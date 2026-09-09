import asyncio
import json
import click
from pathlib import Path
from src.generators.screenplay_generator import ScreenplayGenerator
from src.generators.character_generator import CharacterGenerator
from src.generators.scene_generator import SceneGenerator
from src.video.video_composer import VideoComposer
from src.visual_style import VISUAL_STYLE_PRESETS
from config.settings import settings

class BoxingFilmGenerator:
    def __init__(self):
        self.screenplay_gen = ScreenplayGenerator()
        self.character_gen = CharacterGenerator()
        self.scene_gen = SceneGenerator()
        self.video_composer = VideoComposer()
    
    def generate_film(self, prompt: str, output_dir: str = None, visual_style: str = "cinematic_glamorous"):
        """
        Generate complete film: screenplay, characters, scenes, and videos.
        visual_style: One of 'athletic_professional', 'cinematic_glamorous', 'moody_intense', 
                     'intimate_close', 'bright_showcase', 'stylized_sexy'
        """
        output_dir = output_dir or settings.output_dir
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Validate visual style
        if visual_style not in VISUAL_STYLE_PRESETS:
            print(f"⚠️  Visual style '{visual_style}' not found. Available styles:")
            for style_name in VISUAL_STYLE_PRESETS.keys():
                print(f"   - {style_name}")
            visual_style = "cinematic_glamorous"
            print(f"   Using default: {visual_style}\n")
        
        style_preset = VISUAL_STYLE_PRESETS.get(visual_style)
        
        print(f"🎬 Generating women's boxing film from prompt...")
        print(f"📸 Visual Style: {style_preset.name}")
        print(f"Prompt: {prompt}\n")
        
        # Step 1: Generate Screenplay
        print("📝 Step 1: Generating screenplay with visual direction...")
        screenplay_data = self.screenplay_gen.generate_screenplay(prompt, visual_style)
        screenplay = screenplay_data['screenplay']
        
        screenplay_path = output_path / "screenplay.md"
        with open(screenplay_path, 'w') as f:
            f.write(screenplay)
        print(f"✅ Screenplay saved to {screenplay_path}")
        print(f"   Style: {screenplay_data['style_preset']}\n")
        
        # Step 2: Generate Characters
        print("👯 Step 2: Generating character profiles...")
        characters = self.character_gen.generate_characters(screenplay)
        
        characters_path = output_path / "characters.json"
        with open(characters_path, 'w') as f:
            json.dump(characters, f, indent=2)
        print(f"✅ Characters saved to {characters_path}")
        print(f"   Generated {len(characters)} characters\n")
        
        # Step 3: Break Down Scenes
        print("🎬 Step 3: Breaking down scenes with visual styling...")
        scenes = self.scene_gen.breakdown_scenes(screenplay, visual_style)
        
        scenes_path = output_path / "scenes.json"
        with open(scenes_path, 'w') as f:
            json.dump(scenes, f, indent=2)
        print(f"✅ Scenes saved to {scenes_path}")
        print(f"   Broken down into {len(scenes)} scenes")
        print(f"   All scenes include {style_preset.name} visual styling\n")
        
        # Step 4: Generate Enhanced Video Prompts
        print("🎥 Step 4: Creating enhanced video generation prompts...")
        video_prompts = []
        for scene in scenes:
            lead_character = characters[0] if characters else None
            enhanced_prompt = self.scene_gen.enhance_scene_video_prompt(scene, visual_style, lead_character)
            video_prompts.append({
                "scene_number": scene.get('scene_number'),
                "scene_title": scene.get('title'),
                "video_prompt": enhanced_prompt
            })
        
        prompts_path = output_path / "video_prompts.json"
        with open(prompts_path, 'w') as f:
            json.dump(video_prompts, f, indent=2)
        print(f"✅ Video generation prompts saved to {prompts_path}\n")
        
        # Step 5: Generate Videos (Optional - requires API keys)
        print("🎥 Step 5: Video generation setup...")
        if settings.runway_api_key or settings.pika_api_key:
            print("   Generating scene videos (this may take a while)...")
            try:
                scene_videos = asyncio.run(self.video_composer.generate_scene_videos(scenes))
                videos_path = output_path / "videos_manifest.json"
                with open(videos_path, 'w') as f:
                    json.dump(scene_videos, f, indent=2)
                print(f"✅ Video generation complete: {videos_path}\n")
            except Exception as e:
                print(f"⚠️  Video generation failed: {e}")
                print("   (This is optional - continue without videos)\n")
        else:
            print("⚠️  No video API keys configured")
            print("   Set RUNWAY_API_KEY or PIKA_API_KEY in .env to generate videos")
            print("   You can still use the video_prompts.json with Runway or Pika manually\n")
        
        # Summary
        print("="*60)
        print("🎬 FILM GENERATION COMPLETE")
        print("="*60)
        print(f"Output directory: {output_path}")
        print(f"Visual Style: {style_preset.name}")
        print(f"\nGenerated files:")
        print(f"  📄 screenplay.md - Full screenplay with visual direction")
        print(f"  👥 characters.json - Character profiles with visual details")
        print(f"  🎬 scenes.json - Scene breakdown with visual styling")
        print(f"  🎥 video_prompts.json - Enhanced video generation prompts")
        if (output_path / "videos_manifest.json").exists():
            print(f"  📹 videos_manifest.json - Generated video manifest")
        print(f"\nNext steps:")
        print(f"  1. Review screenplay.md for story structure")
        print(f"  2. Use video_prompts.json with Runway ML or Pika Labs")
        print(f"  3. Generate videos from the enhanced prompts")
        print(f"  4. Compose final video with ffmpeg or video editing software")
        print(f"\nTo use with Runway ML:")
        print(f"  - Copy prompts from video_prompts.json")
        print(f"  - Paste into Runway's text-to-video interface")
        print(f"  - Videos will be generated with {style_preset.name} aesthetic")

@click.command()
@click.option('--prompt', '-p', required=True, help='The prompt for film generation')
@click.option('--output', '-o', default=None, help='Output directory')
@click.option('--style', '-s', default='cinematic_glamorous', 
              help='Visual style preset (athletic_professional, cinematic_glamorous, moody_intense, intimate_close, bright_showcase, stylized_sexy)')
def main(prompt: str, output: str, style: str):
    """
    Generate a women's boxing film from a single prompt.
    
    Example:
        python src/main.py -p "Two rival boxers compete in championship match" -s stylized_sexy
    """
    generator = BoxingFilmGenerator()
    generator.generate_film(prompt, output, style)

if __name__ == "__main__":
    main()
