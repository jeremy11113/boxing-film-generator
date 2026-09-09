import asyncio
from typing import List, Dict
from src.video.video_api_client import VideoAPIClient

class VideoComposer:
    """
    Composes individual scene videos into a complete film.
    """
    
    def __init__(self):
        self.api_client = VideoAPIClient()
        self.generated_videos = []
    
    async def generate_scene_videos(self, scenes: List[Dict]) -> List[Dict]:
        """
        Generate videos for all scenes.
        """
        tasks = []
        
        for scene in scenes:
            video_prompt = scene.get('video_generation_prompt', scene.get('description', ''))
            duration = scene.get('duration', 4)
            
            task = self.api_client.generate_scene_video(video_prompt, duration)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        scene_videos = []
        for scene, video_url in zip(scenes, results):
            scene_videos.append({
                'scene_number': scene.get('scene_number'),
                'scene_title': scene.get('title'),
                'video_url': video_url,
                'duration': scene.get('duration', 4)
            })
        
        return scene_videos
    
    def compose_final_video(self, scene_videos: List[Dict]) -> Dict:
        """
        Metadata for composing videos together.
        In production, this would use ffmpeg or similar to stitch videos.
        """
        return {
            'scenes': scene_videos,
            'total_duration': sum(s.get('duration', 4) for s in scene_videos),
            'status': 'ready_for_composition',
            'notes': 'Use ffmpeg or similar to concatenate video files'
        }
