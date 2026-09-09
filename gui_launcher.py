#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Boxing Film Generator - Windows App with Video Generation
Now with automatic video generation using open source AI!
"""

import sys
import os
from pathlib import Path
import json
from datetime import datetime
import threading

# Add project to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, scrolledtext
except ImportError:
    print("Error: tkinter not found")
    sys.exit(1)

try:
    from src.generators.screenplay_generator import ScreenplayGenerator
    from src.generators.character_generator import CharacterGenerator
    from src.generators.scene_generator import SceneGenerator
    from src.video.video_composer import VideoComposer
    from src.visual_style import VISUAL_STYLE_PRESETS
    from config.settings import settings
except ImportError as e:
    print(f"Error: {e}")
    sys.exit(1)


class BoxingFilmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Boxing Film Generator - Full Edition")
        self.root.geometry("1000x900")
        self.root.iconbitmap(default='')  # Remove default icon
        
        # Dark theme
        self.root.config(bg='#1a1a1a')
        style = ttk.Style()
        style.theme_use('clam')
        
        # Create app
        self.create_ui()
        self.init_generators()
        self.is_generating = False
        self.generate_videos = tk.BooleanVar(value=True)
        
    def create_ui(self):
        """Create the user interface"""
        
        # Main container
        main = ttk.Frame(self.root, style='Main.TFrame')
        main.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # TITLE
        title_frame = ttk.Frame(main)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title = tk.Label(
            title_frame,
            text="🎬 BOXING FILM GENERATOR - FULL EDITION",
            font=('Arial', 20, 'bold'),
            fg='#ff6b6b',
            bg='#1a1a1a'
        )
        title.pack(anchor=tk.W)
        
        subtitle = tk.Label(
            title_frame,
            text="Create complete boxing films with AI - screenplay, characters, scenes, AND videos!",
            font=('Arial', 10),
            fg='#cccccc',
            bg='#1a1a1a'
        )
        subtitle.pack(anchor=tk.W)
        
        # PROMPT SECTION
        prompt_label = tk.Label(
            main,
            text="📝 What's your film about?",
            font=('Arial', 12, 'bold'),
            fg='#ffffff',
            bg='#1a1a1a'
        )
        prompt_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.prompt_text = tk.Text(
            main,
            height=4,
            width=100,
            font=('Arial', 10),
            bg='#2b2b2b',
            fg='#ffffff',
            insertbackground='#ff6b6b',
            relief=tk.FLAT,
            borderwidth=1
        )
        self.prompt_text.pack(fill=tk.X, pady=(0, 15))
        self.prompt_text.insert(tk.END, "Two rival female boxers face off in a championship match...")
        
        # STYLE SECTION
        style_label = tk.Label(
            main,
            text="🎨 Choose the look:",
            font=('Arial', 12, 'bold'),
            fg='#ffffff',
            bg='#1a1a1a'
        )
        style_label.pack(anchor=tk.W, pady=(0, 10))
        
        style_frame = ttk.Frame(main)
        style_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.selected_style = tk.StringVar(value="stylized_sexy")
        
        styles = [
            ("✨ Sexy & Dramatic", "stylized_sexy"),
            ("🌅 Glamorous & Warm", "cinematic_glamorous"),
            ("🏆 Athletic & Professional", "athletic_professional"),
            ("🌙 Moody & Intense", "moody_intense"),
        ]
        
        for label, value in styles:
            rb = tk.Radiobutton(
                style_frame,
                text=label,
                variable=self.selected_style,
                value=value,
                font=('Arial', 10),
                fg='#ffffff',
                bg='#1a1a1a',
                activebackground='#1a1a1a',
                activeforeground='#ff6b6b',
                selectcolor='#2b2b2b',
                highlightthickness=0
            )
            rb.pack(anchor=tk.W, pady=3)
        
        # VIDEO GENERATION OPTION
        video_frame = ttk.Frame(main)
        video_frame.pack(fill=tk.X, pady=(0, 15))
        
        video_label = tk.Label(
            video_frame,
            text="🎥 Generate Videos:",
            font=('Arial', 12, 'bold'),
            fg='#ffffff',
            bg='#1a1a1a'
        )
        video_label.pack(anchor=tk.W, pady=(0, 5))
        
        video_cb = tk.Checkbutton(
            video_frame,
            text="Automatically generate videos (takes 5-15 min per video) - FREE using AI on your computer!",
            variable=self.generate_videos,
            font=('Arial', 10),
            fg='#00dd00',
            bg='#1a1a1a',
            activebackground='#1a1a1a',
            activeforeground='#00dd00',
            selectcolor='#2b2b2b',
            highlightthickness=0
        )
        video_cb.pack(anchor=tk.W)
        
        # API KEY CHECK
        api_frame = ttk.Frame(main)
        api_frame.pack(fill=tk.X, pady=(0, 15))
        
        if settings.openai_api_key:
            api_status = tk.Label(
                api_frame,
                text="✓ OpenAI API Key Configured",
                font=('Arial', 10),
                fg='#00dd00',
                bg='#1a1a1a'
            )
        else:
            api_status = tk.Label(
                api_frame,
                text="✗ No API Key - Open .env file and add your key",
                font=('Arial', 10),
                fg='#ff6b6b',
                bg='#1a1a1a'
            )
        api_status.pack(anchor=tk.W)
        
        # BUTTONS
        button_frame = ttk.Frame(main)
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.gen_btn = tk.Button(
            button_frame,
            text="🚀  GENERATE COMPLETE FILM",
            font=('Arial', 12, 'bold'),
            bg='#ff6b6b',
            fg='#ffffff',
            padx=20,
            pady=10,
            relief=tk.FLAT,
            cursor='hand2',
            command=self.generate
        )
        self.gen_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = tk.Button(
            button_frame,
            text="⏹ STOP",
            font=('Arial', 10, 'bold'),
            bg='#666666',
            fg='#ffffff',
            padx=15,
            pady=10,
            relief=tk.FLAT,
            state=tk.DISABLED,
            command=self.stop
        )
        self.stop_btn.pack(side=tk.LEFT)
        
        # OUTPUT LOG
        log_label = tk.Label(
            main,
            text="📊 Generation Log:",
            font=('Arial', 12, 'bold'),
            fg='#ffffff',
            bg='#1a1a1a'
        )
        log_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.log = scrolledtext.ScrolledText(
            main,
            height=12,
            width=100,
            font=('Arial', 9),
            bg='#0a0a0a',
            fg='#00dd00',
            insertbackground='#ff6b6b',
            relief=tk.FLAT,
            borderwidth=1,
            state=tk.DISABLED
        )
        self.log.pack(fill=tk.BOTH, expand=True)
        
        self.print_log("Ready to create your complete boxing film!")
        self.print_log("")
        self.print_log("With video generation checked:")
        self.print_log("  1. AI writes your screenplay")
        self.print_log("  2. Creates character profiles")
        self.print_log("  3. Breaks down all scenes")
        self.print_log("  4. GENERATES ACTUAL VIDEOS (5-15 min each)")
        self.print_log("")
        self.print_log("Need a free API key?")
        self.print_log("Go to: https://platform.openai.com/api-keys")
        
    def init_generators(self):
        """Initialize AI generators"""
        try:
            self.screenplay_gen = ScreenplayGenerator()
            self.character_gen = CharacterGenerator()
            self.scene_gen = SceneGenerator()
            self.video_composer = VideoComposer(use_open_source=True)
            self.print_log("✓ Generators ready")
        except Exception as e:
            self.print_log(f"✗ Error: {e}")
            messagebox.showerror("Error", f"Failed to initialize: {e}")
    
    def print_log(self, msg):
        """Print to log"""
        self.log.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log.insert(tk.END, f"[{timestamp}] {msg}\n")
        self.log.see(tk.END)
        self.log.config(state=tk.DISABLED)
        self.root.update()
    
    def generate(self):
        """Generate film"""
        prompt = self.prompt_text.get("1.0", tk.END).strip()
        
        if not prompt:
            messagebox.showwarning("Oops!", "Please enter what your film is about.")
            return
        
        if not settings.openai_api_key:
            messagebox.showerror(
                "Missing API Key",
                "Open the .env file in this folder and add your OpenAI API key.\n\n"
                "Get a free key at: https://platform.openai.com/api-keys"
            )
            return
        
        if self.generate_videos.get():
            response = messagebox.askyesno(
                "Video Generation",
                "Video generation takes 5-15 minutes per scene.\n\n"
                "This will use FREE AI on your computer.\n\n"
                "Continue?"
            )
            if not response:
                return
        
        self.is_generating = True
        self.gen_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.print_log("\n" + "="*60)
        self.print_log("STARTING COMPLETE FILM GENERATION...")
        
        thread = threading.Thread(
            target=self._generate_thread,
            args=(prompt, self.selected_style.get(), self.generate_videos.get())
        )
        thread.daemon = True
        thread.start()
    
    def _generate_thread(self, prompt, style, gen_videos):
        """Generate in background"""
        try:
            output_dir = Path.home() / "BoxingFilms" / datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Screenplay
            self.print_log("📝 Writing screenplay...")
            screenplay_data = self.screenplay_gen.generate_screenplay(prompt, style)
            screenplay = screenplay_data['screenplay']
            (output_dir / "screenplay.md").write_text(screenplay)
            self.print_log("   ✓ Screenplay complete")
            
            # Characters
            self.print_log("👯 Creating characters...")
            characters = self.character_gen.generate_characters(screenplay)
            (output_dir / "characters.json").write_text(json.dumps(characters, indent=2))
            self.print_log(f"   ✓ {len(characters)} characters created")
            
            # Scenes
            self.print_log("🎬 Breaking down scenes...")
            scenes = self.scene_gen.breakdown_scenes(screenplay, style)
            (output_dir / "scenes.json").write_text(json.dumps(scenes, indent=2))
            self.print_log(f"   ✓ {len(scenes)} scenes")
            
            # Video Prompts
            self.print_log("🎥 Creating video prompts...")
            video_prompts = []
            for scene in scenes:
                lead = characters[0] if characters else None
                enhanced = self.scene_gen.enhance_scene_video_prompt(scene, style, lead)
                video_prompts.append({
                    "scene_number": scene.get('scene_number'),
                    "scene_title": scene.get('title'),
                    "video_prompt": enhanced
                })
            (output_dir / "video_prompts.json").write_text(json.dumps(video_prompts, indent=2))
            self.print_log("   ✓ Video prompts created")
            
            # Generate Videos
            if gen_videos and self.is_generating:
                self.print_log("\n🎥 GENERATING VIDEOS (This will take a while...)")
                self.print_log(f"   {len(scenes)} scenes to generate")
                self.print_log("   Estimated time: 5-15 minutes per video")
                self.print_log("")
                
                try:
                    import asyncio
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    videos = loop.run_until_complete(
                        self.video_composer.generate_scene_videos(scenes, str(output_dir))
                    )
                    
                    (output_dir / "videos_manifest.json").write_text(json.dumps(videos, indent=2))
                    
                    for video_info in videos:
                        if video_info['status'] == 'completed':
                            self.print_log(f"   ✓ Scene {video_info['scene_number']} video complete")
                        else:
                            self.print_log(f"   ✗ Scene {video_info['scene_number']} failed")
                    
                except Exception as e:
                    self.print_log(f"\n   ✗ Video generation error: {e}")
                    self.print_log("   (But your screenplay, characters, and scenes are ready!)")
            
            self.print_log("\n" + "="*60)
            self.print_log("✓ FILM GENERATION COMPLETE!")
            self.print_log("="*60)
            self.print_log(f"Saved to: {output_dir}")
            self.print_log("\nFiles created:")
            self.print_log("  📄 screenplay.md")
            self.print_log("  👥 characters.json")
            self.print_log("  🎬 scenes.json")
            self.print_log("  🎥 video_prompts.json")
            if gen_videos:
                self.print_log("  🎥 videos_manifest.json (video info)")
                self.print_log("  🎥 scene_*.mp4 (actual videos!)")
            
            messagebox.showinfo("Success!", f"Film generated!\n\n{output_dir}")
            
            # Open folder
            import subprocess
            subprocess.Popen(f'explorer "{output_dir}"')
            
        except Exception as e:
            self.print_log(f"\n✗ ERROR: {e}")
            messagebox.showerror("Error", f"Generation failed:\n{e}")
        
        finally:
            self.is_generating = False
            self.gen_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
    
    def stop(self):
        """Stop generation"""
        self.is_generating = False
        self.print_log("\n⏹ Generation stopped")
        self.gen_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = BoxingFilmApp(root)
    root.mainloop()
