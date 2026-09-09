#!/usr/bin/env python
# Create a simple icon for the application
# If PIL is available, creates a nice icon
# Otherwise uses a placeholder

from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
    
    # Create a 256x256 icon
    img = Image.new('RGB', (256, 256), color='#2b2b2b')
    draw = ImageDraw.Draw(img)
    
    # Draw boxing glove symbol
    # Simple red boxing glove shape
    draw.ellipse([50, 50, 150, 150], fill='#ff6b6b', outline='#ffffff', width=3)
    draw.rectangle([60, 140, 140, 200], fill='#ff6b6b', outline='#ffffff', width=3)
    
    # Add film reel symbols
    draw.ellipse([170, 50, 220, 100], fill='#ffffff', outline='#ff6b6b', width=2)
    draw.ellipse([180, 60, 210, 90], fill='#2b2b2b')
    
    # Save as .ico
    icon_path = Path(__file__).parent / 'icon.ico'
    img.save(icon_path)
    print(f"✓ Icon created: {icon_path}")
    
except ImportError:
    print("PIL not installed, skipping icon generation")
    print("You can use any .ico file as icon.ico")
