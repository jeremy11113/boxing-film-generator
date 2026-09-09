import aiohttp
import asyncio
from typing import Optional, Dict
from config.settings import settings

class VideoAPIClient:
    """
    Base class for video generation APIs.
    Supports Runway ML, Pika Labs, and other text-to-video services.
    """
    
    def __init__(self):
        self.runway_key = settings.runway_api_key
        self.pika_key = settings.pika_api_key
    
    async def generate_video_runway(self, prompt: str, duration: int = 4) -> Optional[str]:
        """
        Generate video using Runway ML API.
        Returns video URL.
        """
        if not self.runway_key:
            raise ValueError("Runway API key not configured")
        
        url = "https://api.runwayml.com/v1/generations"
        headers = {
            "Authorization": f"Bearer {self.runway_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gen3",
            "prompt": prompt,
            "duration": duration,
            "frames": duration * settings.framerate
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get('video_url') or data.get('id')
                    else:
                        print(f"Runway API error: {resp.status}")
                        return None
            except Exception as e:
                print(f"Error calling Runway API: {e}")
                return None
    
    async def generate_video_pika(self, prompt: str, duration: int = 4) -> Optional[str]:
        """
        Generate video using Pika Labs API.
        Returns video URL.
        """
        if not self.pika_key:
            raise ValueError("Pika API key not configured")
        
        # Pika Labs implementation
        print(f"Generating with Pika: {prompt}")
        # TODO: Implement Pika API integration
        return None
    
    async def generate_scene_video(self, scene_description: str, duration: int = 4) -> Optional[str]:
        """
        Generate video for a scene from description.
        Tries Runway first, falls back to Pika.
        """
        try:
            video_url = await self.generate_video_runway(scene_description, duration)
            if video_url:
                return video_url
        except:
            pass
        
        try:
            video_url = await self.generate_video_pika(scene_description, duration)
            if video_url:
                return video_url
        except:
            pass
        
        return None
