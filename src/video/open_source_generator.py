# Open Source Video Generation for Boxing Film Generator
# Uses Stable Video Diffusion - completely free, runs on your computer

import torch
import numpy as np
from pathlib import Path
from PIL import Image
import subprocess
import sys

try:
    from diffusers import StableVideoDiffusionPipeline
except ImportError:
    pass


class OpenSourceVideoGenerator:
    """
    Generate videos using open source models (Stable Video Diffusion)
    Completely free - runs on your computer
    """
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = None
        self.model_name = "stabilityai/stable-video-diffusion-img2vid-xt"
        
    def check_requirements(self) -> bool:
        """Check if all required packages are installed"""
        required = ['torch', 'diffusers', 'transformers', 'PIL']
        missing = []
        
        for package in required:
            try:
                __import__(package)
            except ImportError:
                missing.append(package)
        
        return len(missing) == 0, missing
    
    def install_requirements(self):
        """Install required packages"""
        packages = [
            'torch',
            'diffusers>=0.21.0',
            'transformers>=4.30',
            'accelerate',
            'safetensors',
        ]
        
        for package in packages:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    def load_model(self):
        """Load the video generation model"""
        print(f"Loading model on {self.device}...")
        print("This may take 1-2 minutes on first run...")
        
        try:
            self.pipe = StableVideoDiffusionPipeline.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16,
                variant="fp16"
            )
            self.pipe.enable_attention_slicing()
            self.pipe = self.pipe.to(self.device)
            print("✓ Model loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def generate_video_from_image(self, image_path: str, output_path: str, num_frames: int = 25) -> bool:
        """
        Generate video from an image
        Takes 5-15 minutes depending on your computer
        
        Args:
            image_path: Path to input image
            output_path: Where to save the video
            num_frames: Number of frames (25 = ~1 second at 25fps)
        """
        if not self.pipe:
            print("Model not loaded. Call load_model() first.")
            return False
        
        try:
            print(f"Generating video from image...")
            print(f"This will take 5-15 minutes depending on your computer...")
            
            image = Image.open(image_path).convert("RGB")
            image = image.resize((576, 1024))  # Model's input size
            
            # Generate frames
            frames = self.pipe(
                image,
                num_frames=num_frames,
                num_inference_steps=25,
            ).frames[0]
            
            # Save as video
            self._save_frames_as_video(frames, output_path)
            print(f"✓ Video saved to {output_path}")
            return True
            
        except Exception as e:
            print(f"Error generating video: {e}")
            return False
    
    def generate_video_from_prompt(self, prompt: str, output_path: str) -> bool:
        """
        Generate video from text prompt using text-to-image then image-to-video
        Requires additional model (takes longer)
        """
        print("Generating image from prompt first...")
        print("(This requires an additional model)")
        
        try:
            from diffusers import DPMSolverMultistepScheduler
            from diffusers import StableDiffusionPipeline
            
            # First: Text to Image
            print(f"Step 1: Creating image from prompt...")
            text_to_img = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                torch_dtype=torch.float16,
            ).to(self.device)
            
            image = text_to_img(prompt, height=576, width=1024).images[0]
            temp_image = Path(output_path).parent / "temp_frame.png"
            image.save(temp_image)
            
            # Second: Image to Video
            print(f"Step 2: Generating video from image...")
            success = self.generate_video_from_image(str(temp_image), output_path)
            
            # Cleanup
            temp_image.unlink()
            return success
            
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def _save_frames_as_video(self, frames, output_path: str, fps: int = 25):
        """
        Save frames as MP4 video using ffmpeg
        """
        try:
            import cv2
        except ImportError:
            print("Installing opencv-python for video saving...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python"])
            import cv2
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert frames to numpy array if needed
        if not isinstance(frames, np.ndarray):
            frames = np.array([np.array(f) for f in frames])
        
        # Write video
        height, width = frames[0].shape[:2]
        writer = cv2.VideoWriter(
            str(output_path),
            cv2.VideoWriter_fourcc(*'mp4v'),
            fps,
            (width, height)
        )
        
        for frame in frames:
            writer.write(frame)
        writer.release()


def install_video_generation():
    """
    One-time setup for video generation
    Call this once to download and prepare everything
    """
    print("\n" + "="*60)
    print("SETTING UP VIDEO GENERATION")
    print("="*60)
    print()
    print("This will download the AI models (~5GB)")
    print("This only needs to happen ONCE")
    print()
    print("Continue? (This takes 10-30 minutes)")
    response = input("Type 'yes' to continue: ").strip().lower()
    
    if response != 'yes':
        print("Setup cancelled")
        return False
    
    gen = OpenSourceVideoGenerator()
    
    # Check and install requirements
    has_all, missing = gen.check_requirements()
    if not has_all:
        print(f"Installing missing packages: {missing}")
        gen.install_requirements()
    
    # Load model (downloads it)
    success = gen.load_model()
    
    if success:
        print("\n" + "="*60)
        print("✓ VIDEO GENERATION SETUP COMPLETE!")
        print("="*60)
        print()
        print("You can now generate videos!")
        print("Each video takes 5-15 minutes to generate.")
        print()
        return True
    else:
        print("\nSetup failed. Check error messages above.")
        return False


if __name__ == "__main__":
    install_video_generation()
