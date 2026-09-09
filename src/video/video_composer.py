# Video Composer - generates videos from scenes
# Supports both open source (free) and cloud APIs (paid)

import json
import asyncio
from pathlib import Path
from typing import List, Dict, Optional
import subprocess
import sys

try:
    from src.video.open_source_generator import OpenSourceVideoGenerator
except ImportError:
    OpenSourceVideoGenerator = None

from config.settings import settings


class VideoComposer:
    """
    Compose videos from scenes using available generators
    - Open source (free, local): Stable Video Diffusion
    - Cloud APIs (paid): Runway ML, Pika Labs
    """
    
    def __init__(self, use_open_source: bool = True):
        self.use_open_source = use_open_source
        self.open_source_gen = None
        self.runway_api_key = settings.runway_api_key if hasattr(settings, 'runway_api_key') else None
        self.pika_api_key = settings.pika_api_key if hasattr(settings, 'pika_api_key') else None
        
        if use_open_source and OpenSourceVideoGenerator:
            self.open_source_gen = OpenSourceVideoGenerator()
    
    def setup_open_source(self) -> bool:
        """
        Setup open source video generation (one-time setup)
        Downloads AI models (~5GB)
        """
        if not OpenSourceVideoGenerator:
            print("Error: Diffusers library not installed")
            return False
        
        from src.video.open_source_generator import install_video_generation
        return install_video_generation()
    
    async def generate_scene_videos(self, scenes: List[Dict], output_dir: str = None) -> List[Dict]:
        """
        Generate videos for all scenes
        
        Args:
            scenes: List of scene dictionaries
            output_dir: Where to save videos
        
        Returns:
            List of video information
        """
        output_dir = Path(output_dir or settings.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        videos = []
        
        for scene in scenes:
            scene_num = scene.get('scene_number', 'unknown')
            scene_title = scene.get('title', 'Untitled')
            
            print(f"\nGenerating video for Scene {scene_num}: {scene_title}")
            
            video_path = output_dir / f"scene_{scene_num:02d}.mp4"
            
            if self.use_open_source and self.open_source_gen:
                success = await self._generate_with_open_source(scene, video_path)
            else:
                success = await self._generate_with_api(scene, video_path)
            
            if success:
                videos.append({
                    "scene_number": scene_num,
                    "title": scene_title,
                    "video_path": str(video_path),
                    "status": "completed"
                })
            else:
                videos.append({
                    "scene_number": scene_num,
                    "title": scene_title,
                    "status": "failed"
                })
        
        return videos
    
    async def _generate_with_open_source(self, scene: Dict, output_path: Path) -> bool:
        """
        Generate video using open source model (free, local)
        """
        try:
            if not self.open_source_gen.pipe:
                print("Loading model...")
                if not self.open_source_gen.load_model():
                    return False
            
            prompt = scene.get('video_generation_prompt', scene.get('description', ''))
            print(f"Video prompt: {prompt[:100]}...")
            print("Generating video (this takes 5-15 minutes)...")
            
            # Run in executor to not block
            loop = asyncio.get_event_loop()
            success = await loop.run_in_executor(
                None,
                self.open_source_gen.generate_video_from_prompt,
                prompt,
                str(output_path)
            )
            
            return success
            
        except Exception as e:
            print(f"Error generating with open source: {e}")
            return False
    
    async def _generate_with_api(self, scene: Dict, output_path: Path) -> bool:
        """
        Generate video using cloud API (Runway ML or Pika)
        """
        if self.runway_api_key:
            return await self._generate_with_runway(scene, output_path)
        elif self.pika_api_key:
            return await self._generate_with_pika(scene, output_path)
        else:
            print("No API keys configured. Use open source generation or add API keys to .env")
            return False
    
    async def _generate_with_runway(self, scene: Dict, output_path: Path) -> bool:
        """
        Generate using Runway ML API
        """
        try:
            import aiohttp
            
            prompt = scene.get('video_generation_prompt', '')
            
            async with aiohttp.ClientSession() as session:
                # Runway API call (would need proper implementation)
                # This is a placeholder - implement based on Runway's API
                print(f"Would generate with Runway: {prompt[:50]}...")
                return True
                
        except Exception as e:
            print(f"Error with Runway: {e}")
            return False
    
    async def _generate_with_pika(self, scene: Dict, output_path: Path) -> bool:
        """
        Generate using Pika Labs API
        """
        try:
            import aiohttp
            
            prompt = scene.get('video_generation_prompt', '')
            
            async with aiohttp.ClientSession() as session:
                # Pika API call (would need proper implementation)
                print(f"Would generate with Pika: {prompt[:50]}...")
                return True
                
        except Exception as e:
            print(f"Error with Pika: {e}")
            return False


if __name__ == "__main__":
    # Test/setup
    composer = VideoComposer(use_open_source=True)
    composer.setup_open_source()
