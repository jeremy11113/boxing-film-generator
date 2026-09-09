#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Boxing Film Generator - GUI Launcher
A user-friendly interface to generate women's boxing films
"""

import sys
import os
from pathlib import Path
import json
from typing import Optional

try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, scrolledtext
    from tkinter import font as tkFont
except ImportError:
    print("Error: tkinter not found. Please install Python with tkinter support.")
    sys.exit(1)

import threading
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from src.generators.screenplay_generator import ScreenplayGenerator
    from src.generators.character_generator import CharacterGenerator
    from src.generators.scene_generator import SceneGenerator
    from src.visual_style import VISUAL_STYLE_PRESETS
    from config.settings import settings
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure all dependencies are installed: pip install -r requirements.txt")
    sys.exit(1)


class BoxingFilmGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Boxing Film Generator - Windows Edition")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Set style
        self.setup_styles()
        
        # Create GUI
        self.creating_gui = True
        self.create_widgets()
        self.creating_gui = False
        
        # Generator objects
        self.screenplay_gen = None
        self.character_gen = None
        self.scene_gen = None
        self.is_generating = False
        
        # Initialize generators
        self.initialize_generators()
    
    def setup_styles(self):
        """Configure visual styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Define colors
        bg_color = "#2b2b2b"
        fg_color = "#ffffff"
        accent_color = "#ff6b6b"
        
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color)
        style.configure('TLabelframe', background=bg_color, foreground=fg_color)
        style.configure('TLabelframe.Label', background=bg_color, foreground=accent_color)
        style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'), foreground=accent_color)
        style.configure('Subtitle.TLabel', font=('Helvetica', 10), foreground="#cccccc")
        
    def create_widgets(self):
        """Create GUI widgets"""
        # Main container with scrollbar
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="🎬 Boxing Film Generator", style='Header.TLabel')
        title_label.pack(anchor=tk.W)
        
        subtitle_label = ttk.Label(header_frame, text="Create professional women's boxing films from AI prompts", style='Subtitle.TLabel')
        subtitle_label.pack(anchor=tk.W)
        
        # Prompt Section
        prompt_frame = ttk.LabelFrame(main_frame, text="📝 Film Prompt", padding=10)
        prompt_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        ttk.Label(prompt_frame, text="Enter your story idea:").pack(anchor=tk.W, pady=(0, 5))
        
        self.prompt_text = tk.Text(prompt_frame, height=5, width=80, wrap=tk.WORD)
        self.prompt_text.pack(fill=tk.BOTH, expand=True)
        self.prompt_text.insert(tk.END, "Two rival female boxers face off in a championship match...")
        
        # Visual Style Section
        style_frame = ttk.LabelFrame(main_frame, text="🎨 Visual Style", padding=10)
        style_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(style_frame, text="Choose the visual aesthetic:").pack(anchor=tk.W, pady=(0, 10))
        
        # Create style buttons
        styles_grid = ttk.Frame(style_frame)
        styles_grid.pack(fill=tk.X)
        
        self.selected_style = tk.StringVar(value="stylized_sexy")
        
        styles = [
            ("✨ Stylized Sexy", "stylized_sexy"),
            ("🌅 Cinematic Glamorous", "cinematic_glamorous"),
            ("🏆 Athletic Professional", "athletic_professional"),
            ("🌙 Moody Intense", "moody_intense"),
            ("💫 Intimate Close", "intimate_close"),
            ("⭐ Bright Showcase", "bright_showcase"),
        ]
        
        for i, (label, value) in enumerate(styles):
            row = i // 2
            col = i % 2
            rb = ttk.Radiobutton(
                styles_grid,
                text=label,
                variable=self.selected_style,
                value=value
            )
            rb.grid(row=row, column=col, sticky=tk.W, padx=5, pady=5)
        
        # Style description
        self.style_description = ttk.Label(
            style_frame,
            text=self.get_style_description("stylized_sexy"),
            wraplength=800,
            justify=tk.LEFT
        )
        self.style_description.pack(anchor=tk.W, pady=(10, 0))
        
        # Bind style change
        for widget in styles_grid.winfo_children():
            if isinstance(widget, ttk.Radiobutton):
                self.root.bind('<Button-1>', self.update_style_description)
        
        # Output Directory
        output_frame = ttk.LabelFrame(main_frame, text="📁 Output Location", padding=10)
        output_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.output_path = tk.StringVar(value=str(Path.home() / "BoxingFilms"))
        
        ttk.Label(output_frame, text="Save generated films to:").pack(anchor=tk.W, pady=(0, 5))
        
        path_frame = ttk.Frame(output_frame)
        path_frame.pack(fill=tk.X)
        
        ttk.Entry(path_frame, textvariable=self.output_path, state='readonly').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(path_frame, text="Browse", command=self.browse_output_dir).pack(side=tk.RIGHT)
        
        # Generate Button
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.generate_button = ttk.Button(
            button_frame,
            text="🚀 Generate Film",
            command=self.generate_film
        )
        self.generate_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.cancel_button = ttk.Button(
            button_frame,
            text="Stop",
            command=self.cancel_generation,
            state=tk.DISABLED
        )
        self.cancel_button.pack(side=tk.LEFT)
        
        ttk.Button(button_frame, text="Open Output Folder", command=self.open_output_folder).pack(side=tk.RIGHT)
        
        # Status/Output
        output_frame = ttk.LabelFrame(main_frame, text="📊 Generation Log", padding=10)
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            height=8,
            width=80,
            state=tk.DISABLED
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        self.log_message("Ready to generate films! Enter a prompt and click 'Generate Film'.")
    
    def get_style_description(self, style_key: str) -> str:
        """Get description for a style"""
        if style_key in VISUAL_STYLE_PRESETS:
            return VISUAL_STYLE_PRESETS[style_key].description
        return ""
    
    def update_style_description(self, event=None):
        """Update style description when selection changes"""
        if not self.creating_gui:
            description = self.get_style_description(self.selected_style.get())
            self.style_description.config(text=description)
    
    def initialize_generators(self):
        """Initialize AI generators"""
        try:
            self.log_message("Initializing generators...")
            self.screenplay_gen = ScreenplayGenerator()
            self.character_gen = CharacterGenerator()
            self.scene_gen = SceneGenerator()
            self.log_message("✓ Generators ready")
        except Exception as e:
            self.log_message(f"✗ Error initializing generators: {e}")
            messagebox.showerror("Initialization Error", f"Failed to initialize generators: {e}")
    
    def browse_output_dir(self):
        """Browse for output directory"""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_path.set(directory)
    
    def log_message(self, message: str):
        """Add message to output log"""
        self.output_text.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.output_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.root.update()
    
    def generate_film(self):
        """Generate film in background thread"""
        prompt = self.prompt_text.get("1.0", tk.END).strip()
        
        if not prompt:
            messagebox.showwarning("Empty Prompt", "Please enter a film prompt.")
            return
        
        if not settings.openai_api_key:
            messagebox.showerror(
                "Missing API Key",
                "OpenAI API key not found.\n\nPlease:\n1. Open .env file\n2. Add your API key: OPENAI_API_KEY=sk-..."
            )
            return
        
        # Disable UI during generation
        self.is_generating = True
        self.generate_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)
        
        # Run generation in background thread
        thread = threading.Thread(
            target=self._generate_in_background,
            args=(prompt, self.selected_style.get(), self.output_path.get())
        )
        thread.daemon = True
        thread.start()
    
    def _generate_in_background(self, prompt: str, style: str, output_dir: str):
        """Background thread for film generation"""
        try:
            output_path = Path(output_dir) / datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path.mkdir(parents=True, exist_ok=True)
            
            self.log_message(f"🎬 Starting generation...")
            self.log_message(f"Style: {VISUAL_STYLE_PRESETS[style].name}")
            
            # Step 1: Generate Screenplay
            self.log_message("📝 Generating screenplay...")
            screenplay_data = self.screenplay_gen.generate_screenplay(prompt, style)
            screenplay = screenplay_data['screenplay']
            
            screenplay_path = output_path / "screenplay.md"
            with open(screenplay_path, 'w') as f:
                f.write(screenplay)
            self.log_message(f"✓ Screenplay saved")
            
            # Step 2: Generate Characters
            self.log_message("👯 Generating character profiles...")
            characters = self.character_gen.generate_characters(screenplay)
            
            characters_path = output_path / "characters.json"
            with open(characters_path, 'w') as f:
                json.dump(characters, f, indent=2)
            self.log_message(f"✓ {len(characters)} characters generated")
            
            # Step 3: Break Down Scenes
            self.log_message("🎬 Breaking down scenes...")
            scenes = self.scene_gen.breakdown_scenes(screenplay, style)
            
            scenes_path = output_path / "scenes.json"
            with open(scenes_path, 'w') as f:
                json.dump(scenes, f, indent=2)
            self.log_message(f"✓ {len(scenes)} scenes created")
            
            # Step 4: Generate Video Prompts
            self.log_message("🎥 Creating video generation prompts...")
            video_prompts = []
            for scene in scenes:
                lead_character = characters[0] if characters else None
                enhanced_prompt = self.scene_gen.enhance_scene_video_prompt(scene, style, lead_character)
                video_prompts.append({
                    "scene_number": scene.get('scene_number'),
                    "scene_title": scene.get('title'),
                    "video_prompt": enhanced_prompt
                })
            
            prompts_path = output_path / "video_prompts.json"
            with open(prompts_path, 'w') as f:
                json.dump(video_prompts, f, indent=2)
            self.log_message(f"✓ Video prompts ready for Runway ML")
            
            self.log_message("")
            self.log_message("="*60)
            self.log_message("✅ GENERATION COMPLETE!")
            self.log_message("="*60)
            self.log_message(f"Output saved to: {output_path}")
            self.log_message("")
            self.log_message("Files created:")
            self.log_message("  📄 screenplay.md - Full screenplay")
            self.log_message("  👥 characters.json - Character profiles")
            self.log_message("  🎬 scenes.json - Scene breakdown")
            self.log_message("  🎥 video_prompts.json - For Runway ML")
            self.log_message("")
            self.log_message("Next: Use video_prompts.json with Runway ML to generate videos")
            
            messagebox.showinfo(
                "Generation Complete",
                f"Film generated successfully!\n\nSaved to:\n{output_path}"
            )
            
        except Exception as e:
            self.log_message(f"✗ Error: {e}")
            messagebox.showerror("Generation Failed", f"Error during generation: {e}")
        
        finally:
            self.is_generating = False
            self.generate_button.config(state=tk.NORMAL)
            self.cancel_button.config(state=tk.DISABLED)
    
    def cancel_generation(self):
        """Cancel generation (placeholder)"""
        self.log_message("Generation cancelled by user")
        self.is_generating = False
        self.generate_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)
    
    def open_output_folder(self):
        """Open output folder in Windows Explorer"""
        output_dir = Path(self.output_path.get())
        output_dir.mkdir(parents=True, exist_ok=True)
        
        import subprocess
        subprocess.Popen(f'explorer "{output_dir}"')


def main():
    root = tk.Tk()
    app = BoxingFilmGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
