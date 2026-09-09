import asyncio
import json
import click
from pathlib import Path
from src.generators.screenplay_generator import ScreenplayGenerator
from src.generators.character_generator import CharacterGenerator
from src.generators.scene_generator import SceneGenerator
from src.video.video_composer import VideoComposer
from config.settings import settings

class BoxingFilmGenerator:
    def __init__(self):
        self.screenplay_gen = ScreenplayGenerator()
        self.character_gen = CharacterGenerator()
        self.scene_gen = SceneGenerator()
        self.video_composer = VideoComposer()
    
    def generate_film(self, prompt: str, output_dir: str = None):
        """
        Generate complete film: screenplay, characters, scenes, and videos.
        """
        output_dir = output_dir or settings.output_dir
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        print(f"🎬 Generating women's boxing film from prompt...")
        print(f"Prompt: {prompt}\n")
        
        # Step 1: Generate Screenplay
        print("📝 Step 1: Generating screenplay...")
        screenplay = self.screenplay_gen.generate_screenplay(prompt)
        
        screenplay_path = output_path / "screenplay.md"
        with open(screenplay_path, 'w') as f:
            f.write(screenplay)
        print(f"✅ Screenplay saved to {screenplay_path}\n")
        
        # Step 2: Generate Characters
        print("👯 Step 2: Generating character profiles...")
        characters = self.character_gen.generate_characters(screenplay)
        
        characters_path = output_path / "characters.json"
        with open(characters_path, 'w') as f:
            json.dump(characters, f, indent=2)
        print(f"✅ Characters saved to {characters_path}")
        print(f"   Generated {len(characters)} characters\n")
        
        # Step 3: Break Down Scenes
        print("🎬 Step 3: Breaking down scenes...")
        scenes = self.scene_gen.breakdown_scenes(screenplay)
        
        scenes_path = output_path / "scenes.json"
        with open(scenes_path, 'w') as f:
            json.dump(scenes, f, indent=2)
        print(f"✅ Scenes saved to {scenes_path}")
        print(f"   Broken down into {len(scenes)} scenes\n")
        
        # Step 4: Generate Videos (Optional - requires API keys)
        print("🎥 Step 4: Video generation setup...")
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
            print("   Set RUNWAY_API_KEY or PIKA_API_KEY in .env to generate videos\n")
        
        # Summary
        print("="*50)
        print("🎬 FILM GENERATION COMPLETE")
        print("="*50)
        print(f"Output directory: {output_path}")
        print(f"\nGenerated files:")
        print(f"  📄 screenplay.md - Full screenplay")
        print(f"  👥 characters.json - Character profiles")
        print(f"  🎬 scenes.json - Scene breakdown")
        if (output_path / "videos_manifest.json").exists():
            print(f"  🎥 videos_manifest.json - Video generation manifest")
        print(f"\nNext steps:")
        print(f"  1. Review screenplay.md")
        print(f"  2. Refine characters and scenes as needed")
        print(f"  3. Run video generation with proper API keys")
        print(f"  4. Compose final video with ffmpeg or video editing software")

@click.command()
@click.option('--prompt', '-p', required=True, help='The prompt for film generation')
@click.option('--output', '-o', default=None, help='Output directory')
def main(prompt: str, output: str):
    """
    Generate a women's boxing film from a single prompt.
    """
    generator = BoxingFilmGenerator()
    generator.generate_film(prompt, output)

if __name__ == "__main__":
    main()
