#!/usr/bin/env python
# Simple script to create a Windows shortcut to the GUI

import os
import sys
from pathlib import Path

try:
    from win32com.client import Dispatch
except ImportError:
    print("Installing pywin32...")
    os.system("pip install pywin32")
    from win32com.client import Dispatch

print("Creating shortcut...")

# Get paths
project_dir = Path(__file__).parent
gui_launcher = project_dir / "gui_launcher.py"
python_exe = sys.executable

# Create shortcut on Desktop
desktop = Path.home() / "Desktop"
shortcut_path = desktop / "Boxing Film Generator.lnk"

shell = Dispatch("WScript.Shell")
shortcut = shell.CreateShortcut(str(shortcut_path))
shortcut.TargetPath = python_exe
shortcut.Arguments = f'"{gui_launcher}"'
shortcut.WorkingDirectory = str(project_dir)
shortcut.IconLocation = str(project_dir / "icon.ico")
shortcut.save()

print(f"✓ Shortcut created on Desktop: {shortcut_path}")
print(f"  Double-click to run the Boxing Film Generator!")
